"""
Grade calculation logic for UTCN courses.

Implements weighted arithmetic mean (standard grade average):
- Formula: (grade1 × credits1 + grade2 × credits2 + ...) / total_credits
- All selected courses are included in the calculation
- Unselected courses: Not included in calculation
"""
from typing import List, Dict
from models import Course


def calculate_weighted_harmonic_mean(courses: List[Course]) -> Dict:
    """
    Calculate the weighted arithmetic mean of course grades.

    Formula: (grade1 × credits1 + grade2 × credits2 + ...) / total_credits

    This is the standard weighted average used by most universities.

    Args:
        courses: List of Course objects with grades assigned

    Returns:
        Dictionary containing:
        - final_grade: The calculated weighted arithmetic mean
        - total_credits: Total credits for selected courses
        - passing_courses: Number of passing courses
        - failing_courses: Number of failing courses
        - total_courses: Total number of courses included
    """
    if not courses:
        return {
            "final_grade": 0.0,
            "total_credits": 0.0,
            "passing_courses": 0,
            "failing_courses": 0,
            "total_courses": 0,
        }

    # Filter courses to only include those with valid credits
    valid_courses = [c for c in courses if c.has_grade() and c.credits > 0]

    if not valid_courses:
        return {
            "final_grade": 0.0,
            "total_credits": 0.0,
            "passing_courses": 0,
            "failing_courses": 0,
            "total_courses": 0,
        }

    # Separate passing and failing courses for statistics
    passing_courses = [c for c in valid_courses if c.is_passing()]
    failing_courses = [c for c in valid_courses if c.is_failing()]

    # Calculate total credits
    total_credits = sum(c.credits for c in valid_courses)

    # Calculate weighted arithmetic mean: sum(grade × credits) / total_credits
    weighted_grade_sum = sum(c.grade * c.credits for c in valid_courses)

    if total_credits == 0:
        final_grade = 0.0
    else:
        final_grade = weighted_grade_sum / total_credits

    return {
        "final_grade": round(final_grade, 2),
        "total_credits": total_credits,
        "passing_courses": len(passing_courses),
        "failing_courses": len(failing_courses),
        "total_courses": len(valid_courses),
    }


def filter_selected_courses(courses: List[Course], selected_indices: List[int]) -> List[Course]:
    """
    Filter courses to only include those selected by the user.

    Args:
        courses: List of all available courses
        selected_indices: List of indices of selected courses

    Returns:
        List of Course objects that were selected
    """
    selected = []
    for idx in selected_indices:
        if 0 <= idx < len(courses):
            selected.append(courses[idx])
    return selected
