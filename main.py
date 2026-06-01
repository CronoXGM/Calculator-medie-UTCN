"""
UTCN Grade Calculator - Entry point.

Orchestrates the full flow:
1. Welcome screen
2. Collect study year and specialization
3. Scrape courses from the UTCN curriculum PDF
4. Let user select subjects and enter grades
5. Calculate and display the weighted average
"""

import sys

from grade_calculator import calculate_weighted_harmonic_mean
from pdf_handler import scrape_subjects
from ui_handler import (
    clear_console,
    collect_grades,
    confirm_exit,
    display_error,
    display_results,
    display_welcome,
    get_specialization,
    get_study_year,
    select_subjects_interactive,
)


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        display_welcome()

        # Step 1: Collect user input
        study_year = get_study_year()
        specialization = get_specialization()

        clear_console()
        print(f"\nFetching curriculum for Year {study_year} - {specialization}...")
        print("This may take a moment.\n")

        # Step 2: Scrape the curriculum PDF
        courses = scrape_subjects(study_year, specialization)

        if not courses:
            display_error(
                "No courses could be extracted from the curriculum PDF. "
                "Please check your study year and specialization."
            )
            return 1

        clear_console()

        # Step 3: Subject selection
        selected_courses = select_subjects_interactive(courses)
        if not selected_courses:
            return 0

        # Step 4: Grade entry
        graded_courses = collect_grades(selected_courses)
        if not graded_courses:
            display_error("No grades were entered.")
            return 1

        # Step 5: Calculate and display results
        result = calculate_weighted_harmonic_mean(graded_courses)
        display_results(result)

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 0
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
