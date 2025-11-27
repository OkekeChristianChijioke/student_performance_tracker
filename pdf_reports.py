# pdf_reports.py

from fpdf import FPDF
from typing import Dict, List


class StudentReportPDF(FPDF):
    def header(self):
        # Title at the top of every page
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Student Performance Report", ln=True, align="C")
        self.ln(5)


def generate_student_pdf(report_data: Dict, output_path: str) -> None:
    """
    Generate a simple PDF report for a single student.

    Expected keys in report_data:
    - name: str
    - student_class: str
    - subjects: List[Dict] with keys: name, score
    - total_score: float
    - average: float
    - class_average: float or None (optional, can be dummy for now)
    - days_present: int (optional)
    - days_absent: int (optional)
    - grade: str (e.g. "A")
    """

    pdf = StudentReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Basic info
    pdf.set_font("Helvetica", "", 12)

    pdf.cell(0, 8, f"Student Name : {report_data.get('name', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Class        : {report_data.get('student_class', 'N/A')}", ln=True)

    days_present = report_data.get("days_present")
    days_absent = report_data.get("days_absent")

    if days_present is not None and days_absent is not None:
        pdf.cell(0, 8, f"Days Present : {days_present}", ln=True)
        pdf.cell(0, 8, f"Days Absent  : {days_absent}", ln=True)

    pdf.cell(0, 8, f"Grade        : {report_data.get('grade', 'N/A')}", ln=True)
    pdf.ln(5)

    # Subjects table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 8, "Subject", border=1)
    pdf.cell(0, 8, "Score", border=1, ln=True)

    pdf.set_font("Helvetica", "", 12)
    subjects: List[Dict] = report_data.get("subjects", [])

    for subject in subjects:
        sub_name = subject.get("name", "")
        score = subject.get("score", "")
        pdf.cell(100, 8, str(sub_name), border=1)
        pdf.cell(0, 8, str(score), border=1, ln=True)

    pdf.ln(5)

    # Totals and averages
    total_score = report_data.get("total_score", 0)
    average = report_data.get("average", 0)
    class_average = report_data.get("class_average")

    pdf.cell(0, 8, f"Total Score        : {total_score:.2f}", ln=True)
    pdf.cell(0, 8, f"Student Average    : {average:.2f}", ln=True)

    if class_average is not None:
        pdf.cell(0, 8, f"Class Average      : {class_average:.2f}", ln=True)

    pdf.ln(5)

    # Optional comment
    comment = report_data.get("comment")
    if comment:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Teacher's Comment:", ln=True)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(0, 8, comment)

    # Save to file
    pdf.output(output_path)
    print(f"PDF report saved to {output_path}")
