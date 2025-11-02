"""
User interface handling for the UTCN Grade Calculator.

Provides interactive CLI functionality using questionary for checkboxes.
"""
import os
import platform
from typing import List, Dict

import questionary
from questionary import Style

from models import Course


# Custom style for the questionary prompts
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Question mark color
    ('question', 'bold'),                # Question text
    ('answer', 'fg:#f44336 bold'),      # Answer color
    ('pointer', 'fg:#673ab7 bold'),     # Pointer color
    ('highlighted', 'fg:#673ab7 bold'), # Highlighted option
    ('selected', 'fg:#cc5454'),         # Selected checkbox
    ('separator', 'fg:#cc5454'),        # Separator
    ('instruction', ''),                 # Instruction text
    ('text', ''),                        # Plain text
    ('disabled', 'fg:#858585 italic')   # Disabled options
])


def clear_console():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def get_study_year() -> str:
    """
    Prompt user for study year with validation.

    Returns:
        Valid study year as string (1-4)
    """
    while True:
        year = questionary.text(
            "Enter your study year (1-4):",
            style=custom_style,
            validate=lambda text: text.strip().isdigit() and 1 <= int(text.strip()) <= 4
        ).ask()

        if year is None:  # User cancelled
            raise KeyboardInterrupt("User cancelled input")

        year = year.strip()
        if year.isdigit() and 1 <= int(year) <= 4:
            return year
        else:
            print("Please enter a number between 1 and 4.")


def get_specialization() -> str:
    """
    Prompt user for specialization with interactive selection.

    Returns:
        Valid specialization code
    """
    specialization = questionary.select(
        "Select your specialization:",
        choices=[
            "CTI (Calculatoare - Romanian)",
            "CTI_EN (Calculatoare - English)",
            "AU (Automatica - Romanian)",
            "AU_EN (Automatica - English)"
        ],
        style=custom_style
    ).ask()

    if specialization is None:  # User cancelled
        raise KeyboardInterrupt("User cancelled input")

    # Extract the code from the selection
    return specialization.split()[0]


def select_subjects_interactive(courses: List[Course]) -> List[Course]:
    """
    Display interactive checkboxes for subject selection.

    Args:
        courses: List of all available courses

    Returns:
        List of selected Course objects
    """
    if not courses:
        print("No courses available to select.")
        return []

    print("\n" + "="*70)
    print("SELECT SUBJECTS YOU ARE TAKING THIS SEMESTER")
    print("="*70)
    print("Use arrow keys to navigate, SPACE to select/deselect, ENTER to confirm\n")

    # Create choices with course display names
    choices = [
        questionary.Choice(
            title=course.display_name(),
            value=idx,
            checked=False  # None selected by default
        )
        for idx, course in enumerate(courses)
    ]

    selected_indices = questionary.checkbox(
        "Select subjects that you take and want to insert grade:",
        choices=choices,
        style=custom_style
    ).ask()

    if selected_indices is None:  # User cancelled
        raise KeyboardInterrupt("User cancelled selection")

    # Return the selected courses
    selected_courses = [courses[idx] for idx in selected_indices]

    if not selected_courses:
        print("\nNo subjects selected. Exiting...")
        return []

    print(f"\n✓ Selected {len(selected_courses)} subject(s)")
    return selected_courses


def collect_grades(courses: List[Course]) -> List[Course]:
    """
    Collect grades for the selected courses.

    Args:
        courses: List of selected Course objects

    Returns:
        List of Course objects with grades assigned
    """
    if not courses:
        return []

    print("\n" + "="*70)
    print("ENTER GRADES FOR SELECTED SUBJECTS")
    print("="*70)
    print("Enter grades from 0 to 10 (grades below 5 are failing)\n")

    graded_courses = []

    for course in courses:
        while True:
            grade_str = questionary.text(
                f"Grade for {course.name} ({course.credits} credits):",
                style=custom_style,
                validate=lambda text: _validate_grade(text)
            ).ask()

            if grade_str is None:  # User cancelled
                raise KeyboardInterrupt("User cancelled grade entry")

            try:
                grade = float(grade_str.strip())
                if 0 <= grade <= 10:
                    course.grade = grade
                    graded_courses.append(course)

                    # Provide feedback on the grade
                    if grade >= 5:
                        print(f"  ✓ Passing grade: {grade}")
                    else:
                        print(f"  ✗ Failing grade: {grade} (will lower your average)")
                    break
                else:
                    print("  Please enter a grade between 0 and 10.")
            except ValueError:
                print("  Please enter a valid number.")

    return graded_courses


def _validate_grade(text: str) -> bool:
    """
    Validate that the input is a valid grade (0-10).

    Args:
        text: Input text to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        grade = float(text.strip())
        return 0 <= grade <= 10
    except ValueError:
        return False


def display_results(result: Dict):
    """
    Display the final calculation results in a formatted way.

    Args:
        result: Dictionary containing calculation results
    """
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)

    print(f"\nTotal courses evaluated: {result['total_courses']}")
    print(f"  - Passing courses (≥ 5): {result['passing_courses']}")
    print(f"  - Failing courses (< 5): {result['failing_courses']}")
    print(f"\nTotal credits: {result['total_credits']}")

    print("\n" + "-"*70)
    print(f"WEIGHTED HARMONIC MEAN GRADE: {result['final_grade']:.2f}")
    print("-"*70)

    # Provide interpretation
    if result['final_grade'] >= 5:
        print(f"\n✓ Your average is PASSING ({result['final_grade']:.2f} ≥ 5.00)")
    else:
        print(f"\n✗ Your average is FAILING ({result['final_grade']:.2f} < 5.00)")

    if result['failing_courses'] > 0:
        print(f"\n⚠ Warning: You have {result['failing_courses']} failing course(s)")
        print("  These courses significantly lower your weighted average.")

    print()


def display_welcome():
    """Display welcome message."""
    clear_console()
    print("="*70)
    print("UTCN GRADE CALCULATOR")
    print("Weighted Harmonic Mean Calculator for Semester Grades")
    print("="*70)
    print()


def display_error(message: str):
    """
    Display an error message.

    Args:
        message: Error message to display
    """
    print(f"\n✗ ERROR: {message}\n")


def confirm_exit() -> bool:
    """
    Ask user to confirm exit.

    Returns:
        True if user wants to exit, False otherwise
    """
    response = questionary.confirm(
        "Do you want to exit?",
        style=custom_style,
        default=False
    ).ask()

    return response if response is not None else True
