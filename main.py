"""
UTCN Grade Calculator - Main Entry Point

A modular application to calculate weighted harmonic mean grades
for UTCN (Technical University of Cluj-Napoca) students.

This application:
1. Scrapes course data from UTCN curriculum PDFs
2. Allows interactive subject selection via checkboxes
3. Collects grades for selected subjects
4. Calculates weighted harmonic mean with special handling for failing grades
"""
import sys
from typing import List

from models import Course
from pdf_handler import scrape_subjects
from grade_calculator import calculate_weighted_harmonic_mean
from ui_handler import (
    display_welcome,
    display_error,
    get_study_year,
    get_specialization,
    select_subjects_interactive,
    collect_grades,
    display_results,
    clear_console,
)


def main():
    """Main application entry point."""
    try:
        # Display welcome message
        display_welcome()

        # Step 1: Get user input for year and specialization
        print("Step 1: Enter your academic information\n")
        study_year = get_study_year()
        specialization = get_specialization()

        # Step 2: Scrape subjects from PDF
        print(f"\nStep 2: Fetching curriculum for Year {study_year}, {specialization}...")
        print("This may take a few moments...\n")

        courses = scrape_subjects(study_year, specialization)

        if not courses:
            display_error("No courses were found in the curriculum PDF.")
            display_error("Please check your year and specialization, or try again later.")
            return 1

        # Clear console to remove scrapy logs
        clear_console()
        display_welcome()
        print(f"✓ Successfully loaded {len(courses)} courses from curriculum\n")

        # Step 3: Let user select subjects they are taking
        print("Step 3: Select the subjects you are taking this semester\n")
        selected_courses = select_subjects_interactive(courses)

        if not selected_courses:
            print("\nNo subjects selected. Exiting...")
            return 0

        # Step 4: Collect grades for selected subjects
        print(f"\nStep 4: Enter grades for your {len(selected_courses)} selected subject(s)\n")
        graded_courses = collect_grades(selected_courses)

        if not graded_courses:
            display_error("No grades were entered.")
            return 1

        # Step 5: Calculate weighted harmonic mean
        print("\nStep 5: Calculating your weighted harmonic mean grade...\n")
        result = calculate_weighted_harmonic_mean(graded_courses)

        # Step 6: Display results
        display_results(result)

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting...")
        return 0
    except Exception as e:
        display_error(f"An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
