import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="School Management Portal", page_icon="🎓", layout="wide")

DATA_FILE = Path("students.csv")
COLUMNS = ["Student ID", "Name", "Class", "Age", "Parent Contact"]

def load_students():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE, dtype={"Student ID": str})
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            return df[COLUMNS]
        except Exception:
            pass
    return pd.DataFrame(columns=COLUMNS)

def save_students(df):
    df.to_csv(DATA_FILE, index=False)

st.title("🎓 School Management Portal")
st.caption("A simple student-record dashboard built with Python and Streamlit.")

students = load_students()

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a page", ["Dashboard", "Add Student", "Student Records", "About"])
    st.divider()
    st.caption("Demo project — use fictional student data.")

if page == "Dashboard":
    st.subheader("Dashboard Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", len(students))
    c2.metric("Classes", students["Class"].nunique() if not students.empty else 0)
    c3.metric("Records Saved", "Yes" if DATA_FILE.exists() else "Not yet")
    st.divider()
    st.subheader("Recently Added Students")
    if students.empty:
        st.info("No student records yet. Open **Add Student** to create your first record.")
    else:
        st.dataframe(students.tail(5).iloc[::-1], use_container_width=True, hide_index=True)
    if not students.empty:
        st.subheader("Students by Class")
        counts = students["Class"].replace("", "Not specified").value_counts()
        st.bar_chart(counts)

elif page == "Add Student":
    st.subheader("Add a Student")
    with st.form("student_form", clear_on_submit=True):
        student_id = st.text_input("Student ID", placeholder="e.g. STU-001")
        name = st.text_input("Full Name")
        col1, col2 = st.columns(2)
        student_class = col1.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        age = col2.number_input("Age", min_value=3, max_value=25, value=10)
        contact = st.text_input("Parent/Guardian Contact (optional)")
        submitted = st.form_submit_button("Save Student", type="primary")
    if submitted:
        if not student_id.strip() or not name.strip():
            st.error("Please enter both Student ID and Full Name.")
        elif students["Student ID"].astype(str).str.casefold().eq(student_id.strip().casefold()).any():
            st.error("That Student ID already exists. Please use a unique ID.")
        else:
            new_row = pd.DataFrame([{
                "Student ID": student_id.strip(),
                "Name": name.strip(),
                "Class": student_class,
                "Age": int(age),
                "Parent Contact": contact.strip()
            }])
            students = pd.concat([students, new_row], ignore_index=True)
            save_students(students)
            st.success(f"Student record for {name.strip()} was saved.")

elif page == "Student Records":
    st.subheader("Student Records")
    if students.empty:
        st.info("No records found. Add a student first.")
    else:
        search = st.text_input("Search by student name or ID")
        filtered = students[
            students["Name"].astype(str).str.contains(search, case=False, na=False) |
            students["Student ID"].astype(str).str.contains(search, case=False, na=False)
        ] if search else students
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.download_button(
            "Download records as CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="student_records.csv",
            mime="text/csv"
        )
        with st.expander("Delete a student record"):
            ids = filtered["Student ID"].astype(str).tolist()
            selected_id = st.selectbox("Select Student ID", ids)
            if st.button("Delete selected record", type="secondary"):
                updated = students[students["Student ID"].astype(str) != selected_id]
                save_students(updated)
                st.success("Record deleted. Refresh the page to see the update.")
                st.rerun()

else:
    st.subheader("About This Project")
    st.write(
        "The School Management Portal is a beginner Python web application. "
        "It demonstrates a dashboard, form input, searchable student records, CSV storage, "
        "and data export."
    )
    st.markdown("""
    **Technologies**
    - Python
    - Streamlit
    - Pandas
    - CSV file storage

    **Important:** This is a learning/demo app. Do not use real student or sensitive personal
    information in a public demo. For a real school, add secure authentication, access controls,
    backups, and a proper database.
    """)
