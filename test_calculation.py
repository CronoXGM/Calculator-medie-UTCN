"""Test script to verify grade calculation with user's Year 1 data."""
from models import Course
from grade_calculator import calculate_weighted_harmonic_mean

# Year 1 AU_EN data
courses_data = [
    ("Mathematical Analysis 1", 5, 8),
    ("Linear Algebra", 4, 8),
    ("Calculator Architecture", 5, 10),
    ("Linear Electronic Circuits", 5, 8),
    ("Computer Programming and Programming Language", 5, 9),
    ("Physics", 4, 8),
    ("English 1", 2, 10),
    ("Mathematical Analysis 2", 5, 8),
    ("Special Mathematics", 5, 9),
    ("Electrotechnics", 5, 5),
    ("Computer Aided Graphics", 5, 9),
    ("Applied Informatics", 3, 10),
    ("Chemistry", 3, 9),
    ("English 2", 2, 10),
    ("Sport", 2, 10),
]

# Create Course objects
courses = [Course(name=name, credits=credits, grade=grade)
           for name, credits, grade in courses_data]

# Calculate using the fixed method
result = calculate_weighted_harmonic_mean(courses)

print("=" * 60)
print("UTCN Grade Calculator - Test Results")
print("=" * 60)
print(f"\nTotal courses: {result['total_courses']}")
print(f"Total credits: {result['total_credits']}")
print(f"Passing courses: {result['passing_courses']}")
print(f"Failing courses: {result['failing_courses']}")
print(f"\n{'='*60}")
print(f"FINAL GRADE: {result['final_grade']}")
print(f"{'='*60}")

# Show detailed breakdown
print("\nDetailed breakdown:")
total_weighted = 0
total_creds = 0
for course in courses:
    weighted = course.grade * course.credits
    total_weighted += weighted
    total_creds += course.credits
    print(f"{course.name:45s} {course.grade:4.1f} × {course.credits:3.1f} = {weighted:6.2f}")

print(f"\n{'Total:':<45s} {' ':>4s}   {total_creds:3.1f} = {total_weighted:6.2f}")
print(f"\nCalculation: {total_weighted:.2f} / {total_creds:.1f} = {total_weighted/total_creds:.2f}")
