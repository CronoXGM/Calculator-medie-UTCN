"""
PDF scraping and parsing functionality for UTCN curriculum documents.
"""
import re
from io import BytesIO
from urllib.parse import quote
from typing import List

import pdfplumber
import scrapy
from scrapy.crawler import CrawlerProcess

from models import Course


# Global list to store courses extracted from the PDF.
_scraped_courses = []


class CurriculumPDFSpider(scrapy.Spider):
    """
    Scrapy spider to download and parse UTCN curriculum PDFs.
    """
    name = "curriculum_pdf"

    def __init__(self, study_year, specialization, **kwargs):
        """
        Initialize the spider with study parameters.

        Args:
            study_year: String representing a number from 1 to 4
            specialization: One of CTI, CTI_EN, AU, AU_EN
        """
        self.study_year = study_year.strip()
        self.specialization = specialization.strip().upper()
        self.academic_year = "2024-2025"  # Hardcoded academic year
        super().__init__(**kwargs)

    def start_requests(self):
        """Generate the initial request to download the PDF."""
        # Mapping from specialization to URL string
        spec_map = {
            "CTI": "Calcro",
            "CTI_EN": "Caleng(eng)",
            "AU": "AIA_RO",
            "AU_EN": "AIA_EN(eng)",
        }

        if self.specialization not in spec_map:
            self.logger.error(
                f"Invalid specialization: {self.specialization}. "
                "Must be CTI, CTI_EN, AU, or AU_EN."
            )
            return

        try:
            year_int = int(self.study_year)
            if year_int < 1 or year_int > 4:
                self.logger.error("Study year must be between 1 and 4.")
                return
        except ValueError:
            self.logger.error("Study year must be an integer.")
            return

        spec_value = spec_map[self.specialization]
        raw_url = (
            f"https://ac.utcluj.ro/files/Acasa/Site/documente/planuri_invatamant/"
            f"{self.academic_year}/{year_int}_L_{spec_value}_{self.academic_year}.pdf"
        )
        # Encode URL to handle special characters (like parentheses)
        encoded_url = quote(raw_url, safe=":/")
        self.logger.info(f"Fetching PDF from: {encoded_url}")

        # Use headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/115.0 Safari/537.36",
            "Referer": "https://ac.utcluj.ro/planuri-de-invatamant.html",
        }
        yield scrapy.Request(
            encoded_url, callback=self.parse_pdf, headers=headers, dont_filter=True
        )

    def parse_pdf(self, response):
        """
        Parse the downloaded PDF and extract course information.

        Args:
            response: The Scrapy response containing the PDF data
        """
        self.logger.info("PDF downloaded. Extracting table data using pdfplumber...")
        pdf_file = BytesIO(response.body)
        courses = []

        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if not tables:
                        continue

                    for table in tables:
                        for row in table:
                            # Clean each row: replace None with empty string and strip
                            clean_row = [cell.strip() if cell else "" for cell in row]
                            if not any(clean_row):
                                continue  # Skip completely empty rows

                            # Skip header rows or totals
                            if ("CODUL" in clean_row[0].upper()) or (
                                "TOTAL" in clean_row[0].upper()
                            ):
                                continue

                            course_info = None
                            credits_str = None

                            # Choose proper columns based on table structure
                            if len(clean_row) >= 9:
                                # Tables with 9 columns:
                                # - Column 0: course code + subject name
                                # - Column 7: credits
                                course_info = clean_row[0]
                                credits_str = clean_row[7]
                            elif len(clean_row) >= 7:
                                # Tables with 7 columns:
                                # - Column 0: course code + subject name
                                # - Column 5: credits
                                course_info = clean_row[0]
                                credits_str = clean_row[5]
                            else:
                                continue  # Unexpected format, skip row

                            try:
                                credits_val = float(credits_str)
                            except ValueError:
                                self.logger.debug(
                                    f"Skipping row due to credits conversion error: {clean_row}"
                                )
                                continue

                            # Remove leading course code (e.g., "1.00 ") from name
                            course_name = re.sub(r"^\d+(\.\d+)?\s+", "", course_info)

                            courses.append(
                                {"course": course_name, "credits": credits_val}
                            )
        except Exception as e:
            self.logger.error(f"Error processing PDF: {e}")

        if courses:
            for course in courses:
                _scraped_courses.append(course)
                yield course
        else:
            self.logger.error("No course data was extracted from the PDF.")


def scrape_subjects(study_year: str, specialization: str) -> List[Course]:
    """
    Scrape subjects from the UTCN curriculum PDF.

    Args:
        study_year: Study year (1-4)
        specialization: Specialization code (CTI, CTI_EN, AU, AU_EN)

    Returns:
        List of Course objects extracted from the PDF
    """
    global _scraped_courses
    _scraped_courses = []  # Reset the global list

    # Run the spider
    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "INFO",
        }
    )
    process.crawl(
        CurriculumPDFSpider, study_year=study_year, specialization=specialization
    )
    process.start()  # This will block until the spider finishes

    # Convert scraped data to Course objects
    courses = [
        Course(name=item["course"], credits=item["credits"])
        for item in _scraped_courses
    ]

    return courses
