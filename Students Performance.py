
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# 1. PROJECT FOLDER SETUP
# ==========================================

folder = Path(__file__).resolve().parent
csv_file = folder / "student.csv"
output_folder = folder / "output_graphs"

output_folder.mkdir(exist_ok=True)

# ==========================================
# 2. CREATE CSV IF FILE DOES NOT EXIST
# ==========================================

if not csv_file.exists():

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
# 15. GRAPH 1: SUBJECT AVERAGE
# COLOUR: BLUE
# ==========================================

blue_colors = ["#2563EB", "#60A5FA", "#93C5FD"]

plt.figure(figsize=(8, 5))

plt.bar(
    subjects,
    subject_average,
    color=blue_colors,
    edgecolor="black"
)

plt.title("Subject-wise Average Marks")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig(output_folder / "1_subject_average.png", dpi=300)
plt.close()

# ==========================================
# 16. GRAPH 2: STUDENT AVERAGE
# COLOUR: GREEN
# ==========================================

green_colors = [
    "#166534", "#15803D", "#16A34A", "#22C55E", "#4ADE80",
    "#166534", "#15803D", "#16A34A", "#22C55E", "#4ADE80"
]

plt.figure(figsize=(10, 5))

plt.bar(
    df["Name"],
    df["Average"],
    color=green_colors,
    edgecolor="black"
)

plt.title("Student-wise Average Marks")
plt.xlabel("Students")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig(output_folder / "2_student_average.png", dpi=300)
plt.close()

# ==========================================
# 17. GRAPH 3: ATTENDANCE
# COLOUR: ORANGE
# ==========================================

orange_colors = [
    "#C2410C", "#EA580C", "#F97316", "#FB923C", "#FDBA74",
    "#C2410C", "#EA580C", "#F97316", "#FB923C", "#FDBA74"
]

plt.figure(figsize=(10, 5))

plt.bar(
    df["Name"],
    df["Attendance"],
    color=orange_colors,
    edgecolor="black"
)

plt.title("Student Attendance Analysis")
plt.xlabel("Students")
plt.ylabel("Attendance Percentage")
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig(output_folder / "3_attendance.png", dpi=300)
plt.close()

# ==========================================
# 18. EXPORT FINAL CSV REPORT
# ==========================================

report_file = folder / "student_analysis_report.csv"

df.to_csv(report_file, index=False)

# ==========================================
# 19. FINAL PROJECT OUTPUT
# ==========================================

print("\n========== PROJECT COMPLETED ==========")

print("Report saved:", report_file)

print("\nThree different graphs generated:")

for graph in sorted(output_folder.glob("*.png")):
    print(graph.name)

print("\nAll tasks completed successfully!")
