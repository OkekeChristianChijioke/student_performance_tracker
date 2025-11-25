# grades_utils.py

from typing import List

def calculate_average(scores: List[float]) -> float:
    """
    Calculate the average of a list of scores.
    Returns 0.0 if the list is empty.
    """
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def get_grade(score: float) -> str:
    """
    Return a letter grade based on the numeric score.
    Adjust the boundaries to match your school’s grading system.
    """
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    else:
        return "F"

def calculate_student_summary(name: str, scores: List[float]) -> dict:
    """
    Given a student's name and a list of scores,
    return a summary dictionary with:
    - name
    - scores
    - average
    - grade
    """
    avg = calculate_average(scores)
    grade = get_grade(avg)
    return {
        "name": name,
        "scores": scores,
        "average": avg,
        "grade": grade,
    }

def parse_scores_input(scores_str: str) -> List[float]:
    """
    Parse a comma-separated string of scores into a list of floats.
    Example input: '70, 65.5, 80'
    """
    parts = scores_str.split(",")
    scores: List[float] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        scores.append(float(part))
    return scores
