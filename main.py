#student performance tracker v1
# main.py
from report_io import write_student_summaries_to_csv
from pdf_reports import generate_student_pdf


from date_utils import (
    get_today_date,
    add_days_to_today,
    subtract_days_from_today,
    days_between_dates,
    calculate_age_in_days,
)
from grades_utils import (
    calculate_average,
    get_grade,
    calculate_student_summary,
    parse_scores_input,
)

from data_io import read_students_scores_from_csv, find_student_row_by_name


# ---------- DEMO / FEATURE FUNCTIONS ----------

def demo_dates():
    print("\n=== DATE UTILITIES DEMO ===")
    print("Today's date:", get_today_date())

    print("In 10 days it will be:", add_days_to_today(10))
    print("10 days ago it was:", subtract_days_from_today(10))

    d1 = "2025-12-25"
    d2 = "2025-11-21"
    print(f"Days between {d1} and {d2}:", days_between_dates(d1, d2))

    birthdate = "2000-05-17"
    print(f"If you were born on {birthdate}, you are {calculate_age_in_days(birthdate)} days old.")
    print()  # blank line


def demo_grades():
    print("\n=== GRADES UTILITIES DEMO ===")

    student_name = "John Doe"
    scores = [75, 68, 80, 72]

    summary = calculate_student_summary(student_name, scores)

    print(f"Student name: {summary['name']}")
    print(f"Scores: {summary['scores']}")
    print(f"Average: {summary['average']:.2f}")
    print(f"Grade: {summary['grade']}")
    print()


def interactive_single_student():
    print("\n=== SINGLE STUDENT INTERACTIVE INPUT ===")
    name = input("Enter student's name: ").strip()
    scores_str = input("Enter scores separated by commas (e.g. 70, 65, 80): ")

    try:
        scores = parse_scores_input(scores_str)
    except ValueError:
        print("One of the scores was not a valid number. Please try again.")
        return

    if not scores:
        print("No valid scores entered.")
        return

    summary = calculate_student_summary(name, scores)

    print("\n--- Student Summary ---")
    print(f"Name   : {summary['name']}")
    print(f"Scores : {summary['scores']}")
    print(f"Average: {summary['average']:.2f}")
    print(f"Grade  : {summary['grade']}")
    print()


def generate_single_student_pdf_interactive():
    print("\n=== GENERATE SINGLE STUDENT PDF REPORT ===")
    name = input("Enter student's full name: ").strip()
    student_class = input("Enter student's class (e.g. JS2A): ").strip()

    # For now we ask for days present/absent manually
    days_present_str = input("Enter number of days present (leave blank if unknown): ").strip()
    days_absent_str = input("Enter number of days absent (leave blank if unknown): ").strip()

    days_present = int(days_present_str) if days_present_str else None
    days_absent = int(days_absent_str) if days_absent_str else None

    # Enter subjects and scores
    print("Enter subjects and scores. Type 'done' as subject name when finished.")
    subjects = []
    total_score = 0.0

    while True:
        subject_name = input("Subject name (or 'done' to finish): ").strip()
        if subject_name.lower() == "done":
            break

        score_str = input(f"Score for {subject_name}: ").strip()
        try:
            score = float(score_str)
        except ValueError:
            print("Invalid score. Please enter a number.")
            continue

        subjects.append({"name": subject_name, "score": score})
        total_score += score

    if not subjects:
        print("No subjects entered. Cannot generate report.")
        return

    # Compute averages
    num_subjects = len(subjects)
    average = total_score / num_subjects

    # We can reuse get_grade for the overall average
    grade = get_grade(average)

    # For now, class_average is unknown; you can plug in real value later
    class_average = None

    # Optional teacher's comment
    comment = input("Enter teacher's comment (optional, press Enter to skip): ").strip()
    if not comment:
        comment = None

    report_data = {
        "name": name,
        "student_class": student_class,
        "days_present": days_present,
        "days_absent": days_absent,
        "subjects": subjects,
        "total_score": total_score,
        "average": average,
        "class_average": class_average,
        "grade": grade,
        "comment": comment,
    }

    # File name based on student name
    safe_name = name.replace(" ", "_")
    output_path = f"{safe_name}_report.pdf"

    generate_student_pdf(report_data, output_path)


def get_summaries_from_csv(filepath: str):
    """
    Read students from a CSV and return a list of summary dicts.
    """
    try:
        students_rows = read_students_scores_from_csv(filepath)
    except FileNotFoundError:
        print(f"Could not find file: {filepath}")
        return []

    if not students_rows:
        print("No student data found in CSV.")
        return []

    summaries = []

    for row in students_rows:
        name = row.get("name", "Unknown").strip()

        # Collect all numeric scores from the row except 'name'
        score_values = []
        
        non_subject_fields = {"name", "class", "days_present", "days_absent"}

    for key, value in row.items():
        if key.lower() in non_subject_fields:
            continue

        try:
            score_values.append(float(value))
        except (ValueError, TypeError):
            continue

        if not score_values:
            print(f"No scores found for {name}. Skipping.")
            continue

        summary = calculate_student_summary(name, score_values)
        summaries.append(summary)

    return summaries


def show_subject_averages():
    print("\n=== SUBJECT AVERAGES FROM CSV ===")
    filepath = "students_scores.csv"

    try:
        students_rows = read_students_scores_from_csv(filepath)
    except FileNotFoundError:
        print(f"Could not find file: {filepath}")
        return

    if not students_rows:
        print("No student data found in CSV.")
        return

    # We will collect totals and counts per subject (i.e. per column except 'name')
    subject_totals = {}   # e.g. {"math": 210.0, "english": 195.0}
    subject_counts = {}   # e.g. {"math": 3, "english": 3}

    for row in students_rows:
        for key, value in row.items():
            if key.lower() == "name":
                # Skip the name column
                continue

            if value is None or value == "":
                # Skip empty cells
                continue

            try:
                score = float(value)
            except ValueError:
                # Skip any non-numeric value
                print(f"Warning: could not convert value '{value}' in column '{key}' to a number. Skipping.")
                continue

            # Initialize if seeing this subject for the first time
            if key not in subject_totals:
                subject_totals[key] = 0.0
                subject_counts[key] = 0

            subject_totals[key] += score
            subject_counts[key] += 1

    if not subject_totals:
        print("No numeric scores found for any subject.")
        return

    print("\n--- Subject Averages ---")
    for subject, total in subject_totals.items():
        count = subject_counts[subject]
        average = total / count if count > 0 else 0.0
        print(f"{subject}: {average:.2f}")
    print()


def show_class_summary():
    print("\n=== CLASS SUMMARY FROM CSV ===")
    filepath = "students_scores.csv"

    # Reuse our existing helper to get summaries
    summaries = get_summaries_from_csv(filepath)
    if not summaries:
        print("No student summaries available.")
        return

    # Number of students
    num_students = len(summaries)

    # Extract averages
    averages = [s["average"] for s in summaries]

    # Class average
    class_average = sum(averages) / num_students if num_students > 0 else 0.0

    # Best and worst students by average
    best_student = max(summaries, key=lambda s: s["average"])
    worst_student = min(summaries, key=lambda s: s["average"])

    print("\n--- Class Summary ---")
    print(f"Number of students : {num_students}")
    print(f"Class average      : {class_average:.2f}")
    print(f"Top student        : {best_student['name']} "
          f"({best_student['average']:.2f}, grade {best_student['grade']})")
    print(f"Lowest student     : {worst_student['name']} "
          f"({worst_student['average']:.2f}, grade {worst_student['grade']})")
    print()


def process_students_from_csv():
    print("\n=== PROCESSING STUDENTS FROM CSV ===")
    filepath = "students_scores.csv"

    summaries = get_summaries_from_csv(filepath)
    if not summaries:
        return

    for summary in summaries:
        print("\n--- Student Summary ---")
        print(f"Name   : {summary['name']}")
        print(f"Scores : {summary['scores']}")
        print(f"Average: {summary['average']:.2f}")
        print(f"Grade  : {summary['grade']}")
    print()


def generate_report_csv():
    print("\n=== GENERATE STUDENT REPORT CSV ===")
    input_filepath = "students_scores.csv"
    output_filepath = "students_report.csv"

    summaries = get_summaries_from_csv(input_filepath)
    if not summaries:
        print("No summaries generated. Report not created.")
        return

    write_student_summaries_to_csv(output_filepath, summaries)


def build_report_data_from_row(row, filepath: str, comment: str | None = None):
    """
    Given a CSV row for a single student, build the report_data dict
    expected by generate_student_pdf().
    """
    # Build subjects list from all columns except 'name'
    subjects = []
    total_score = 0.0

    non_subject_fields = {"name", "class", "days_present", "days_absent"}

    for key, value in row.items():
        if key.lower() in non_subject_fields:
            continue

        if value is None or value == "":
            continue

        try:
            score = float(value)
        except ValueError:
            print(f"Warning: could not convert value '{value}' for subject '{key}'. Skipping.")
            continue

        subjects.append({"name": key, "score": score})
        total_score += score

    if not subjects:
        return None  # caller should handle

    num_subjects = len(subjects)
    average = total_score / num_subjects
    grade = get_grade(average)

    # Extract class and attendance from CSV
    student_class = row.get("class", "N/A")

    days_present = row.get("days_present")
    days_absent = row.get("days_absent")

    try:
        days_present = int(days_present) if days_present is not None else None
    except ValueError:
        days_present = None

    try:
        days_absent = int(days_absent) if days_absent is not None else None
    except ValueError:
        days_absent = None


    # Compute overall class average using existing summaries
    summaries = get_summaries_from_csv(filepath)
    if summaries:
        class_averages = [s["average"] for s in summaries]
        class_average = sum(class_averages) / len(class_averages)
    else:
        class_average = None

    report_data = {
        "name": row.get("name", "Unknown"),
        "student_class": student_class,
        "days_present": days_present,
        "days_absent": days_absent,
        "subjects": subjects,
        "total_score": total_score,
        "average": average,
        "class_average": class_average,
        "grade": grade,
        "comment": comment,
    }

    return report_data


def generate_student_pdf_from_csv():
    print("\n=== GENERATE STUDENT PDF REPORT FROM CSV ===")
    filepath = "students_scores.csv"

    student_name = input("Enter student's full name (as in CSV): ").strip()
    if not student_name:
        print("No name entered.")
        return

    try:
        row = find_student_row_by_name(filepath, student_name)
    except FileNotFoundError:
        print(f"Could not find file: {filepath}")
        return

    if row is None:
        print(f"Student '{student_name}' not found in {filepath}.")
        return

    comment = input("Enter teacher's comment for this student (optional, Enter to skip): ").strip()
    if not comment:
        comment = None

    report_data = build_report_data_from_row(row, filepath, comment=comment)
    if report_data is None:
        print("No valid subjects/scores found for this student. Cannot generate report.")
        return

    safe_name = report_data["name"].replace(" ", "_")
    output_path = f"{safe_name}_report.pdf"

    generate_student_pdf(report_data, output_path)


def generate_pdfs_for_all_students_from_csv():
    print("\n=== GENERATE PDF REPORTS FOR ALL STUDENTS FROM CSV ===")
    filepath = "students_scores.csv"

    try:
        students_rows = read_students_scores_from_csv(filepath)
    except FileNotFoundError:
        print(f"Could not find file: {filepath}")
        return

    if not students_rows:
        print("No student data found in CSV.")
        return

    # Ask once for a common teacher comment (optional)
    common_comment = input(
        "Enter a common teacher's comment for all students (optional, Enter to skip): "
    ).strip()
    if not common_comment:
        common_comment = None

    count_generated = 0

    for row in students_rows:
        name = row.get("name", "Unknown").strip()
        if not name:
            print("Skipping a row with no name.")
            continue

        report_data = build_report_data_from_row(row, filepath, comment=common_comment)
        if report_data is None:
            print(f"Skipping {name}: no valid subjects/scores.")
            continue

        safe_name = name.replace(" ", "_")
        output_path = f"{safe_name}_report.pdf"

        generate_student_pdf(report_data, output_path)
        count_generated += 1

    print(f"\nFinished generating {count_generated} PDF report(s).")



# ---------- MENU SYSTEM ----------

def print_menu():
    print("\n=== STUDENT PERFORMANCE TRACKER ===")
    print("1. Demo date utilities")
    print("2. Demo grading utilities")
    print("3. Enter a single student and scores")
    print("4. Process all students from CSV")
    print("5. Generate report CSV")
    print("6. Show subject averages from CSV")
    print("7. Show class summary from CSV")
    print("8. Generate PDF report for one student (interactive)")
    print("9. Generate PDF report for one student (from CSV)")
    print("10. Generate PDF reports for ALL students (from CSV)")
    print("11. Exit")



def main():
    while True:
        print_menu()
        choice = input("Choose an option (1–11): ").strip()

        if choice == "1":
            demo_dates()
        elif choice == "2":
            demo_grades()
        elif choice == "3":
            interactive_single_student()
        elif choice == "4":
            process_students_from_csv()
        elif choice == "5":
            generate_report_csv()
        elif choice == "6":
            show_subject_averages()
        elif choice == "7":
            show_class_summary()
        elif choice == "8":
            generate_single_student_pdf_interactive()
        elif choice == "9":
            generate_student_pdf_from_csv()
        elif choice == "10":
            generate_pdfs_for_all_students_from_csv()
        elif choice == "11":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 11.")


if __name__ == "__main__":
    main()
