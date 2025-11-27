#student performance tracker v1
# main.py
from report_io import write_student_summaries_to_csv


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
from data_io import read_students_scores_from_csv


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
        for key, value in row.items():
            if key == "name":
                continue
            if value is None or value == "":
                continue
            score_values.append(float(value))

        if not score_values:
            print(f"No scores found for {name}. Skipping.")
            continue

        summary = calculate_student_summary(name, score_values)
        summaries.append(summary)

    return summaries


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


# ---------- MENU SYSTEM ----------

def print_menu():
    print("\n=== STUDENT PERFORMANCE TRACKER ===")
    print("1. Demo date utilities")
    print("2. Demo grading utilities")
    print("3. Enter a single student and scores")
    print("4. Process all students from CSV")
    print("5. Generate report CSV")
    print("6. Exit")


def main():
    while True:
        print_menu()
        choice = input("Choose an option (1–6): ").strip()

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
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")



if __name__ == "__main__":
    main()
