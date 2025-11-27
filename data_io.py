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


def find_student_row_by_name(filepath: str, name: str):
    """
    Find a student row in the CSV by exact name match (case-insensitive).
    Returns the row dict or None if not found.
    """
    rows = read_students_scores_from_csv(filepath)
    for row in rows:
        if row.get("name", "").strip().lower() == name.strip().lower():
            return row
    return None
