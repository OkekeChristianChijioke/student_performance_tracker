# Student Performance Tracker

A simple Python project for tracking student performance using dates, grades, and CSV files.

This project is part of my learning journey towards becoming a professional Software Engineer. It demonstrates how to structure a Python project with reusable modules, basic data processing, and Git/GitHub version control.

---

## Features

- **Date utilities**
  - Get today’s date
  - Add or subtract days from today
  - Calculate days between two dates
  - Calculate age in days from a given birthdate

- **Grading utilities**
  - Calculate the average of a list of scores
  - Convert numeric averages into letter grades (A–F)
  - Generate a summary for each student (name, scores, average, grade)

- **CSV support**
  - Read student names and scores from a CSV file
  - Compute average and grade for each student
  - Display a simple text-based summary for every student

---

## Project Structure

```text
student_performance_tracker/
├── data_io.py           # Functions for reading data from CSV files
├── date_utils.py        # Helper functions for working with dates
├── grades_utils.py      # Helper functions for calculating averages and grades
├── main.py              # Entry point: demos, interactive mode, and CSV processing
├── students_scores.csv  # Sample data file with student scores
└── README.md            # Project description and instructions

