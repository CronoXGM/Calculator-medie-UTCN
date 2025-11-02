"""
Data models for the UTCN Grade Calculator.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    """
    Represents a university course with its credits and optional grade.

    Attributes:
        name: The course name
        credits: Number of ECTS credits for the course
        grade: The student's grade (0-10), None if not yet graded
    """
    name: str
    credits: float
    grade: Optional[float] = None

    def is_passing(self) -> bool:
        """
        Check if the course has a passing grade.

        Returns:
            True if grade >= 5, False otherwise or if no grade assigned
        """
        return self.grade is not None and self.grade >= 5

    def is_failing(self) -> bool:
        """
        Check if the course has a failing grade.

        Returns:
            True if grade is assigned and < 5, False otherwise
        """
        return self.grade is not None and self.grade < 5

    def has_grade(self) -> bool:
        """
        Check if a grade has been assigned to this course.

        Returns:
            True if grade is not None, False otherwise
        """
        return self.grade is not None

    def __str__(self) -> str:
        """String representation of the course."""
        grade_str = f"Grade: {self.grade}" if self.grade is not None else "No grade"
        return f"{self.name} ({self.credits} credits) - {grade_str}"

    def display_name(self) -> str:
        """
        Get a formatted display name for UI purposes.

        Returns:
            Formatted string with course name and credits
        """
        return f"{self.name} ({self.credits} credits)"
