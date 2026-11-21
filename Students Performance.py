import numpy as np
import pandas as pd
import os

# ==========================================
# 1. PROJECT FOLDER SETUP
# ==========================================

folder = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(folder, "student.csv")

# ==========================================
# 2. CREATE CSV IF FILE DOES NOT EXIST
# ==========================================

if not os.path.exists(csv_file):

    data = {
        "Name": ["Aman", "Rahul", "Priya", "Karan", "Neha",
                 "Rohit", "Anjali", "Vivek", "Sneha", "Arjun"],
        "Maths": [85, 72, 95, 60, 88, 45, 78, 67, 92, 55],
        "Python": [90, 68, 92, 65, 84, 55, 82, 73, 88, 60],
        "English": [78, 80, 89, 70, 91, 60, 85, 69, 95, 58],
        "Attendance": [92, 85, 98, 75, 96, 65, 88, 80, 94, 70]
    }

    pd.DataFrame(data).to_csv(csv_file, index=False)

# ==========================================
# 3. READ STUDENT DATA
# ==========================================

df = pd.read_csv(csv_file)

subjects = ["Maths", "Python", "English"]
required_columns = ["Name"] + subjects + ["Attendance"]

if df.empty:
    raise ValueError("Student CSV file is empty.")

if any(col not in df.columns for col in required_columns):
    raise ValueError("Please check column names in student.csv.")

for col in subjects + ["Attendance"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if df[required_columns].isnull().any().any():
    raise ValueError("Missing or invalid data found in student.csv.")

if not df[subjects + ["Attendance"]].apply(
    lambda col: col.between(0, 100).all()
).all():
    raise ValueError("Marks and attendance must be between 0 and 100.")

# ==========================================
# 4. DISPLAY STUDENT DATA
# ==========================================

print("\n========== STUDENT DATA ==========")
print(df.to_string(index=False))

print("\nTotal Students:", len(df))
print("Dataset Shape:", df.shape)

# ==========================================
# 5. CALCULATE TOTAL AND AVERAGE
# ==========================================

df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1).round(2)

# ==========================================
# 6. ASSIGN GRADES
# ==========================================

df["Grade"] = np.select(
    [
        df["Average"] >= 90,
        df["Average"] >= 80,
        df["Average"] >= 70,
        df["Average"] >= 60
    ],
    ["A", "B", "C", "D"],
    default="F"
)

# ==========================================
# 7. CALCULATE RESULT STATUS
# ==========================================

df["Status"] = np.where(
    df[subjects].ge(40).all(axis=1),
    "Pass",
    "Fail"
)

# ==========================================
# 8. CALCULATE STUDENT RANK
# ==========================================

df["Rank"] = (
    df["Average"]
    .rank(ascending=False, method="min")
    .astype(int)
)

# ==========================================
# 9. CLASS PERFORMANCE
# ==========================================

print("\n========== CLASS PERFORMANCE ==========")

print("Class Average:", round(df["Average"].mean(), 2))
print("Highest Average:", df["Average"].max())
print("Lowest Average:", df["Average"].min())
print("Average Attendance:", round(df["Attendance"].mean(), 2))

# ==========================================
# 10. FIND CLASS TOPPER
# ==========================================

topper = df.loc[df["Average"].idxmax()]

print("\n========== CLASS TOPPER ==========")

print("Name:", topper["Name"])
print("Average:", topper["Average"])
print("Grade:", topper["Grade"])

# ==========================================
# 11. SUBJECT-WISE ANALYSIS
# ==========================================

subject_average = df[subjects].mean()

print("\n========== SUBJECT ANALYSIS ==========")
print(subject_average.round(2))
print("Best Subject:", subject_average.idxmax())
print("Weakest Subject:", subject_average.idxmin())

# ==========================================
# 12. LOW ATTENDANCE STUDENTS
# ==========================================

print("\n========== LOW ATTENDANCE STUDENTS ==========")

low_attendance = df[df["Attendance"] < 75]

print(
    low_attendance[["Name", "Attendance"]].to_string(index=False)
)

# ==========================================
# 13. STUDENTS NEEDING IMPROVEMENT
# ==========================================

print("\n========== STUDENTS NEEDING IMPROVEMENT ==========")

improvement = df[df["Average"] < 60]

print(
    improvement[["Name", "Average", "Grade"]].to_string(index=False)
)

# ==========================================
# 14. STUDENT RANKING
# ==========================================

ranking = df.sort_values("Rank")

print("\n========== STUDENT RANKING ==========")

print(
    ranking[["Rank", "Name", "Average", "Grade"]].to_string(index=False)
)

# ==========================================
# 15. EXPORT FINAL CSV REPORT
# ==========================================

report_file = os.path.join(folder, "student_analysis_report.csv")

df.to_csv(report_file, index=False)

# ==========================================
# 16. FINAL PROJECT OUTPUT
# ==========================================

print("\n========== PROJECT COMPLETED ==========")

print("Report saved:", report_file)

print("\nAll tasks completed successfully!")