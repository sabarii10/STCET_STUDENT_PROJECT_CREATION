import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    course TEXT,
    marks REAL
)
""")
conn.commit()

# -----------------------------
# Functions
# -----------------------------

def add_student(name, age, gender, course, marks):
    cursor.execute(
        "INSERT INTO students(name,age,gender,course,marks) VALUES(?,?,?,?,?)",
        (name, age, gender, course, marks),
    )
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


def update_student(student_id, name, age, gender, course, marks):
    cursor.execute("""
    UPDATE students
    SET name=?, age=?, gender=?, course=?, marks=?
    WHERE id=?
    """, (name, age, gender, course, marks, student_id))
    conn.commit()


def search_student(name):
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + name + '%',)
    )
    return cursor.fetchall()


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student",
    "Search Student"
]

choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Home
# -----------------------------

if choice == "Home":

    st.subheader("Welcome")

    st.write("""
This application allows you to:

- Add Student
- View Students
- Update Student
- Delete Student
- Search Student
""")

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM students")
    avg = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric("Total Students", total)

    if avg is None:
        avg = 0

    col2.metric("Average Marks", round(avg, 2))


# -----------------------------
# Add Student
# -----------------------------

elif choice == "Add Student":

    st.subheader("Add Student")

    name = st.text_input("Student Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=18
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    course = st.text_input("Course")

    marks = st.number_input(
        "Marks",
        min_value=0.0,
        max_value=100.0
    )

    if st.button("Add Student"):

        add_student(name, age, gender, course, marks)

        st.success("Student Added Successfully")


# -----------------------------
# View Students
# -----------------------------

elif choice == "View Students":

    st.subheader("Student Records")

    data = view_students()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Course",
            "Marks"
        ]
    )

    st.dataframe(df, use_container_width=True)

    if not df.empty:

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "students.csv",
            "text/csv"
        )


# -----------------------------
# Update Student
# -----------------------------

elif choice == "Update Student":

    st.subheader("Update Student")

    data = view_students()

    ids = [row[0] for row in data]

    if len(ids) == 0:
        st.warning("No students found")

    else:

        sid = st.selectbox("Student ID", ids)

        record = [x for x in data if x[0] == sid][0]

        name = st.text_input("Name", record[1])

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=record[2]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male","Female","Other"].index(record[3])
        )

        course = st.text_input("Course", record[4])

        marks = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            value=float(record[5])
        )

        if st.button("Update"):

            update_student(
                sid,
                name,
                age,
                gender,
                course,
                marks
            )

            st.success("Record Updated Successfully")


# -----------------------------
# Delete Student
# -----------------------------

elif choice == "Delete Student":

    st.subheader("Delete Student")

    data = view_students()

    ids = [row[0] for row in data]

    if len(ids) == 0:

        st.warning("No students available")

    else:

        sid = st.selectbox("Select Student ID", ids)

        if st.button("Delete"):

            delete_student(sid)

            st.success("Student Deleted Successfully")


# -----------------------------
# Search Student
# -----------------------------

elif choice == "Search Student":

    st.subheader("Search Student")

    keyword = st.text_input("Enter Student Name")

    if st.button("Search"):

        result = search_student(keyword)

        df = pd.DataFrame(
            result,
            columns=[
                "ID",
                "Name",
                "Age",
                "Gender",
                "Course",
                "Marks"
            ]
        )

        st.dataframe(df, use_container_width=True)
