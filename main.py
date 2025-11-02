import os
import platform
import re
from io import BytesIO
from urllib.parse import quote

import pdfplumber
import scrapy
from scrapy.crawler import CrawlerProcess

# Global list to store courses extracted from the PDF.
scraped_courses = []


def clear_console():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


class CurriculumPDFSpider(scrapy.Spider):
    name = "curriculum_pdf"

    def __init__(self, study_year, specialization, **kwargs):
        """
        study_year: string representing a number from 1 to 4.
        specialization: one of the following: CTI, CTI_EN, AU, AU_EN.
        """
        self.study_year = study_year.strip()
        self.specialization = specialization.strip().upper()
        self.academic_year = (
            "2024-2025"  # Hardcoded academic year as per the URL pattern.
        )
        super().__init__(**kwargs)

    def start_requests(self):
        if self.specialization not in ["CTI", "CTI_EN", "AU", "AU_EN"]:
            self.logger.error(
                f"Invalid specialization: {self.specialization}. Must be CTI, CTI_EN, AU, or AU_EN."
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

        # Mapping from specialization to the string used in the URL.
        # For Automatica (AU/AU_EN), the mapping depends on the year:
        # - Year 1: Uses AIAIS (Automatică, Informatică Aplicată și Sisteme Inteligente)
        # - Years 2-4: Uses IS (Ingineria Sistemelor)
        if self.specialization == "AU":
            spec_value = "AIAIS_RO" if year_int == 1 else "IS_RO"
        elif self.specialization == "AU_EN":
            spec_value = "AIAIS_EN(eng)" if year_int == 1 else "IS_EN(eng)"
        elif self.specialization == "CTI":
            spec_value = "Calcro"
        else:  # CTI_EN
            spec_value = "Caleng(eng)"
        raw_url = (
            f"https://ac.utcluj.ro/files/Acasa/Site/documente/planuri_invatamant/"
            f"{self.academic_year}/{year_int}_L_{spec_value}_{self.academic_year}.pdf"
        )
        # Encode URL so that special characters (like parentheses) are handled.
        encoded_url = quote(raw_url, safe=":/")
        self.logger.info(f"Fetching PDF from: {encoded_url}")

        # Use headers to mimic a browser.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
            "Referer": "https://ac.utcluj.ro/planuri-de-invatamant.html",
        }
        yield scrapy.Request(
            encoded_url, callback=self.parse_pdf, headers=headers, dont_filter=True
        )

    def parse_pdf(self, response):
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
                        self.logger.info("Extracted table: " + str(table))
                        for row in table:
                            self.logger.info("Row: " + str(row))
                            # Clean each row: replace None with empty string and strip whitespace.
                            clean_row = [cell.strip() if cell else "" for cell in row]
                            if not any(clean_row):
                                continue  # Skip completely empty rows.

                            # Skip header rows or totals.
                            if ("CODUL" in clean_row[0].upper()) or (
                                "TOTAL" in clean_row[0].upper()
                            ):
                                continue

                            course_info = None
                            credits_str = None

                            # Depending on the table structure, choose the proper columns.
                            if len(clean_row) >= 9:
                                # For tables with 9 columns, assume:
                                # - Column 0: course code + subject name
                                # - Column 7: credits (as a string convertible to float)
                                course_info = clean_row[0]
                                credits_str = clean_row[7]
                            elif len(clean_row) >= 7:
                                # For tables with 7 columns, assume:
                                # - Column 0: course code + subject name
                                # - Column 5: credits
                                course_info = clean_row[0]
                                credits_str = clean_row[5]
                            else:
                                continue  # Unexpected format, skip row.

                            try:
                                credits_val = float(credits_str)
                            except ValueError:
                                self.logger.info(
                                    f"Skipping row due to credits conversion error: {clean_row}"
                                )
                                continue

                            courses.append(
                                {"course": course_info, "credits": credits_val}
                            )
        except Exception as e:
            self.logger.error(f"Error processing PDF: {e}")

        if courses:
            for course in courses:
                scraped_courses.append(course)
                yield course
        else:
            self.logger.error("No course data was extracted from the PDF.")


if __name__ == "__main__":
    sys.exit(main())
