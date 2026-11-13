import json
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")

DATABASE = "school_data.json"

def load_data():
    if Path(DATABASE).exists():
        content = Path(DATABASE).read_text().strip()
        if content:
            data = json.loads(content)
            # Auto remove Priya from database
            original_len = len(data.get("Students", []))
            data["Students"] = [s for s in data.get("Students", []) if s["name"].lower().strip() != "priya"]
            if len(data["Students"]) != original_len:
                Path(DATABASE).write_text(json.dumps(data, indent=4))
            return data
    return {"Students": [], "Teachers": []}

def save_data(data):
    # Always ensure Priya is not saved again
    data["Students"] = [s for s in data["Students"] if s["name"].lower().strip() != "priya"]
    Path(DATABASE).write_text(json.dumps(data, indent=4))

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

def validate_email(email):
    return "@" in email and "." in email

def get_avg(s):
    return round(sum(s["grades"].values())/len(s["grades"]), 1) if s["grades"] else 0

def get_status(m):
    if m >= 90:
        return "Excellent"
    if m >= 75:
        return "Good"
    if m >= 50:
        return "Average"
    return "Needs Improvement"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Playfair+Display:wght@700&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #0F0E0C; color: #F5EEDD; }

/* HIDE DEPLOY BUTTON + TOOLBAR + FOOTER */
div[data-testid="stToolbar"] { visibility: hidden !important; height: 0px !important; }
div[data-testid="stDecoration"] { visibility: hidden !important; height: 0px !important; }
div[data-testid="stStatusWidget"] { visibility: hidden !important; }
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] { visibility: hidden !important; height: 0px !important; }

section[data-testid="stSidebar"] { background: #161411 !important; border-right: 1px solid rgba(232,200,122,0.18); }
section[data-testid="stSidebar"] * { color: #EDE8DD !important; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #F5EEDD !important; letter-spacing: -0.5px; }
.top-badge {
    display:inline-block; background: rgba(232,200,122,0.12); border:1px solid rgba(232,200,122,0.35);
    color:#E8C87A; padding:5px 12px; border-radius:100px; font-size:11px; letter-spacing:2px; font-weight:700; text-transform:uppercase;
}
.gold { color:#E8C87A; }
.card {
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border:1px solid rgba(255,255,255,0.09); border-radius:18px; padding:18px;
}
.kpi { background: #1A1815; border:1px solid rgba(232,200,122,0.18); border-radius:18px; padding:18px 16px; }
.kpi small { color:#A8A29E; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; font-weight:700; }
.kpi b { font-size:32px; line-height:1.1; display:block; margin-top:6px; color:#fff; }
.kpi span { font-size:12px; color:#E8C87A; }
div.stButton > button {
    background: linear-gradient(90deg, #C9A24B, #E8C87A) !important;
    color: #1A1405 !important; border: none !important; border-radius: 12px !important;
    font-weight: 800 !important; padding: 10px 18px !important; width: 100%;
}
div.stButton > button:hover { filter: brightness(1.08); }
input, select, textarea { border-radius: 12px !important; }
.detail-label { font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:#A8A29E; font-weight:700; margin:0; }
.detail-value { font-size:15px; color:#fff; font-weight:600; margin:4px 0 0 0; }
</style>
""", unsafe_allow_html=True)

# HEADER
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<span class="top-badge">Student Management System</span>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:42px;margin:10px 0 4px;">Student Management <span class="gold"><i>System.</i></span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#B8B2A8;margin:0;">Manage students, teachers and grades in one premium dashboard.</p>', unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi' style='text-align:center'><small>Today</small><b style='font-size:20px;'>3 Dec 2026</b><span>Live System</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

total_students = len(data["Students"])
total_teachers = len(data["Teachers"])
total_grades = sum(len(s["grades"]) for s in data["Students"])
all_marks = [m for s in data["Students"] for m in s["grades"].values()]
avg_all = round(sum(all_marks)/len(all_marks), 1) if all_marks else 0

k1, k2, k3, k4 = st.columns(4)
for col, label, val, sub in [
    (k1, "Total Students", total_students, "Registered"),
    (k2, "Total Teachers", total_teachers, "Active Staff"),
    (k3, "Grades Added", total_grades, "Subjects"),
    (k4, "School Average", f"{avg_all}%", "Overall Performance"),
]:
    with col:
        st.markdown(f"<div class='kpi'><small>{label}</small><b>{val}</b><span>{sub}</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎓 Navigation")
    menu = st.radio("", ["🏠 Dashboard", "👨‍🎓 Register Student", "👩‍🏫 Register Teacher", "📝 Add Grades", "🔍 Student Details", "🔍 Teacher Details"], label_visibility="collapsed")

if menu == "🏠 Dashboard":
    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.subheader("Recent Students")
        if not data["Students"]:
            st.info("No students yet. Register your first student from sidebar.")
        else:
            rows = []
            for s in data["Students"]:
                rows.append({"Name": s["name"], "Roll": s["roll_no"], "Age": s["age"], "Email": s["email"], "Subjects": len(s["grades"]), "Avg %": get_avg(s)})
            st.dataframe(rows, use_container_width=True, hide_index=True)
    with c2:
        st.subheader("Teachers")
        if not data["Teachers"]:
            st.info("No teachers yet.")
        else:
            for t in data["Teachers"]:
                st.markdown(f"<div class='card' style='margin-bottom:10px'><b>{t['name']}</b><br><span style='color:#A8A29E;font-size:13px'>{t['subject']} • ID: {t['employee_id']} • {t['email']}</span></div>", unsafe_allow_html=True)
        st.subheader("Top Performer")
        if data["Students"]:
            best = max(data["Students"], key=lambda x: sum(x["grades"].values())/len(x["grades"]) if x["grades"] else 0)
            avg_best = round(sum(best["grades"].values())/len(best["grades"]), 1) if best["grades"] else 0
            st.success(f"🏆 {best['name']} • Roll {best['roll_no']} • Avg {avg_best}%")

elif menu == "👨‍🎓 Register Student":
    st.subheader("Register New Student")
    with st.form("student_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
        with col_b:
            age = st.number_input("Age", min_value=3, max_value=100, value=16)
            roll_no = st.number_input("Roll Number *", min_value=1, step=1)
        submitted = st.form_submit_button("✨ Register Student")
        if submitted:
            if not name or not email:
                st.error("Please fill name and email.")
            elif name.lower().strip() == "priya":
                st.error("This student is blocked from registration.")
            elif not validate_email(email):
                st.error("Invalid Email. Must contain @ and .")
            elif any(s["roll_no"] == roll_no for s in data["Students"]):
                st.error(f"Student with Roll No {roll_no} already exists!")
            else:
                data["Students"].append({"name": name, "age": int(age), "email": email, "roll_no": int(roll_no), "grades": {}})
                save_data(data)
                st.success(f"Student {name} registered successfully!")
                st.balloons()

elif menu == "👩‍🏫 Register Teacher":
    st.subheader("Register New Teacher")
    with st.form("teacher_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            subject = st.text_input("Subject *")
        with col_b:
            age = st.number_input("Age", min_value=18, max_value=80, value=30)
            emp_id = st.number_input("Employee ID *", min_value=1, step=1)
        submitted = st.form_submit_button("✨ Register Teacher")
        if submitted:
            if not name or not email or not subject:
                st.error("Please fill all fields.")
            elif not validate_email(email):
                st.error("Invalid Email.")
            elif any(t["employee_id"] == emp_id for t in data["Teachers"]):
                st.error("Teacher with this Employee ID already exists!")
            else:
                data["Teachers"].append({"name": name, "age": int(age), "email": email, "employee_id": int(emp_id), "subject": subject})
                save_data(data)
                st.success(f"Teacher {name} registered successfully!")
                st.balloons()

elif menu == "📝 Add Grades":
    st.subheader("Add Grades")
    if not data["Students"]:
        st.warning("No students found. Register a student first.")
    else:
        student_options = {f"{s['name']} • Roll {s['roll_no']}": s["roll_no"] for s in data["Students"]}
        selected = st.selectbox("Select Student", list(student_options.keys()))
        roll = student_options[selected]
        c1, c2 = st.columns(2)
        with c1:
            subject = st.text_input("Subject Name", placeholder="e.g. Maths, Science")
        with c2:
            marks = st.number_input("Obtained Marks", min_value=0, max_value=100, value=85)
        if st.button("Save Grade"):
            if not subject:
                st.error("Enter subject name.")
            else:
                for s in data["Students"]:
                    if s["roll_no"] == roll:
                        s["grades"][subject] = int(marks)
                        save_data(data)
                        st.success(f"Grade added: {subject} = {marks} for {s['name']}")
                        break
        st.markdown("---")
        st.markdown("**All Grades Table**")
        rows = []
        for s in data["Students"]:
            for sub, m in s["grades"].items():
                rows.append({"Name": s["name"], "Roll": s["roll_no"], "Subject": sub, "Marks": m, "Status": get_status(m)})
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No grades added yet.")

elif menu == "🔍 Student Details":
    st.subheader("Student Details")
    st.caption("Search by Roll Number to view complete structured profile.")
    if not data["Students"]:
        st.warning("No students found.")
    else:
        roll = st.number_input("Enter Roll Number", min_value=1, step=1)
        if st.button("Search Student"):
            found = next((s for s in data["Students"] if s["roll_no"] == roll), None)
            if not found:
                st.error("Student Not Found :(")
            else:
                avg = get_avg(found)
                st.markdown(f"<div class='card'><p class='detail-label'>Student Profile</p><h3 style='margin:6px 0 0 0;'>{found['name']}</h3></div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                a, b, c, d = st.columns(4)
                with a: st.markdown(f"<div class='card'><p class='detail-label'>Full Name</p><p class='detail-value'>{found['name']}</p></div>", unsafe_allow_html=True)
                with b: st.markdown(f"<div class='card'><p class='detail-label'>Roll Number</p><p class='detail-value'>{found['roll_no']}</p></div>", unsafe_allow_html=True)
                with c: st.markdown(f"<div class='card'><p class='detail-label'>Age</p><p class='detail-value'>{found['age']} Years</p></div>", unsafe_allow_html=True)
                with d: st.markdown(f"<div class='card'><p class='detail-label'>Average</p><p class='detail-value' style='color:#E8C87A;'>{avg}%</p></div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                left, right = st.columns([1, 1.4])
                with left:
                    st.markdown(f"<div class='card'><p class='detail-label'>Contact Information</p><p style='margin-top:8px;'>Email<br><b>{found['email']}</b></p><hr style='border-color:rgba(255,255,255,0.1)'><p class='detail-label'>Summary</p><p style='margin-top:8px;'>Total Subjects: <b>{len(found['grades'])}</b><br>Average: <b>{avg}%</b><br>Status: <b>{get_status(avg) if found['grades'] else 'No Grades'}</b></p></div>", unsafe_allow_html=True)
                with right:
                    st.markdown("<div class='card'><p class='detail-label'>Subject Wise Grades</p>", unsafe_allow_html=True)
                    if found["grades"]:
                        grade_rows = [{"Subject": k, "Marks / 100": v, "Status": get_status(v)} for k, v in found["grades"].items()]
                        st.dataframe(grade_rows, use_container_width=True, hide_index=True)
                        for sub, m in found["grades"].items():
                            st.progress(m/100, text=f"{sub} — {m}/100")
                    else:
                        st.info("No grades yet for this student.")
                    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🔍 Teacher Details":
    st.subheader("Teacher Details")
    st.caption("Search by Employee ID to view complete structured profile.")
    if not data["Teachers"]:
        st.warning("No teachers found.")
    else:
        emp = st.number_input("Enter Employee ID", min_value=1, step=1)
        if st.button("Search Teacher"):
            found = next((t for t in data["Teachers"] if t["employee_id"] == emp), None)
            if not found:
                st.error("Teacher Not Found")
            else:
                st.markdown(f"<div class='card'><p class='detail-label'>Teacher Profile</p><h3 style='margin:6px 0 0 0;'>{found['name']}</h3></div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                a, b, c, d = st.columns(4)
                with a: st.markdown(f"<div class='card'><p class='detail-label'>Full Name</p><p class='detail-value'>{found['name']}</p></div>", unsafe_allow_html=True)
                with b: st.markdown(f"<div class='card'><p class='detail-label'>Employee ID</p><p class='detail-value'>{found['employee_id']}</p></div>", unsafe_allow_html=True)
                with c: st.markdown(f"<div class='card'><p class='detail-label'>Subject</p><p class='detail-value'>{found['subject']}</p></div>", unsafe_allow_html=True)
                with d: st.markdown(f"<div class='card'><p class='detail-label'>Age</p><p class='detail-value'>{found['age']} Years</p></div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><p class='detail-label'>Contact Information</p><p style='margin-top:8px;'>Email<br><b>{found['email']}</b></p></div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center;color:#77716A;font-size:12px;letter-spacing:1.5px;'>STUDENT MANAGEMENT SYSTEM © 2026 • BUILT FOR FOCUS</p>", unsafe_allow_html=True)
