# data_io.py

import csv
from typing import List, Dict


def read_students_scores_from_csv(filepath: str) -> List[Dict[str, str]]:
    """
    Read student scores from a CSV file.
    Each row is returned as a dict with column names as keys.
    """
    students: List[Dict[str, str]] = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)
    return students
