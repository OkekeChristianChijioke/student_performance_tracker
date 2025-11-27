# report_io.py

from typing import List, Dict
import csv


def write_student_summaries_to_csv(filepath: str, summaries: List[Dict]) -> None:
    """
    Write a list of student summary dicts to a CSV file.

    Each summary dict should have at least:
    - name
    - scores
    - average
    - grade
    """
    if not summaries:
        print("No summaries to write.")
        return

    # Decide which fields to write to the CSV
    fieldnames = ["name", "average", "grade", "scores"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for summary in summaries:
            # Convert list of scores to a string for CSV
            scores_str = ", ".join(str(s) for s in summary.get("scores", []))

            row = {
                "name": summary.get("name", ""),
                "average": f"{summary.get('average', 0):.2f}",
                "grade": summary.get("grade", ""),
                "scores": scores_str,
            }
            writer.writerow(row)

    print(f"Report written to {filepath}")
