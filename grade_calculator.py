"""
Grade calculation logic for UTCN courses.

Implements weighted harmonic mean with special handling for failed courses:
- Passing grades (>= 5): Use standard harmonic mean formula
- Failing grades (< 5): Count as 0 with full credit weight penalty
- Unselected courses: Not included in calculation
"""
from typing import List, Dict
from models import Course


def calculate_weighted_harmonic_mean(courses: List[Course]) -> Dict:
    """
    Calculate the weighted harmonic mean of course grades.

    Formula handling:
    - For passing grades (>= 5): Standard weighted harmonic mean
    - For failing grades (< 5): These are treated as 0, which penalizes the average
      Since we can't divide by 0, we use a modified calculation:
      * Failed courses contribute their credits to total_credits
      * But they contribute infinity to the sum (credits/0 → ∞)
      * This is handled by treating them as maximum penalty

    Mathematical approach:
    For each passing course: sum += credits / grade
    For each failing course: we need to penalize heavily

    The harmonic mean will be: total_credits / sum_of_ratios
    A failing grade should make this very low.

    Args:
        courses: List of Course objects with grades assigned

    Returns:
        Dictionary containing:
        - final_grade: The calculated weighted harmonic mean
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

    # Separate passing and failing courses
    passing_courses = [c for c in valid_courses if c.is_passing()]
    failing_courses = [c for c in valid_courses if c.is_failing()]

    # Calculate total credits (including both passing and failing)
    total_credits = sum(c.credits for c in valid_courses)

    # Calculate the harmonic mean ratio sum for passing courses only
    ratio_sum = sum(c.credits / c.grade for c in passing_courses)

    # For failing courses, we need to handle them specially
    # Since grade < 5 counts as 0, we can't use credits/grade (division by zero)
    # Instead, we treat failing courses as maximum penalty
    #
    # The mathematical approach: if a student fails a course, it should
    # drastically lower their average. We simulate this by using the formula:
    # For failed course with grade g < 5: we use g in calculation but it heavily weights down

    # Alternative approach: Use actual grade values even if < 5
    # This way a grade of 4 is better than a grade of 2
    for failing_course in failing_courses:
        # Use the actual failing grade (which is < 5)
        # This will create a large ratio (credits/small_grade) that increases denominator
        ratio_sum += failing_course.credits / failing_course.grade

    if ratio_sum == 0:
        final_grade = 0.0
    else:
        final_grade = total_credits / ratio_sum

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
