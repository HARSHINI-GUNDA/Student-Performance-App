import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Inject custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #ff9ff3 0%, #54a0ff 100%);
    }
    .stApp {
        background: transparent;
    }
    h1, h2 {
        color: #e84393 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    h1 {
        font-size: 2.8em !important;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
    }
    .stNumberInput > div > input {
        border: 2px solid #00d2d3;
        border-radius: 8px;
        background-color: #f0f8ff;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff6b81, #ffcc5c);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #ffcc5c, #ff6b81);
    }
    .performance-metric {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Constants
N_SAMPLES = 10000
PASS_THRESHOLD = 50
SEED = 42
np.random.seed(SEED)

# Semester-wise subjects
SEMESTER_SUBJECTS = {
    1: ["C Programming", "Differential Equations", "Fundamentals of IT", "Descriptive Statistics","General English 1","Value Education"],
    2: ["DS through C", "Probability Distributions", "Abstract Algebra", "Operating Systems","General English 2","Indian Heritage And Culture"],
    3: ["Database Management Systems", "Computer Organizations", "Python", "Statistical Methods","Environmental Studies"],
    4: ["Java", "Statistical Inference", "Computer Networks", "R Programming", "Data Warehousing", "Accounting And Financial Management"],
    5: ["Artificial Intelligence", "Machine Learning", "Applied Statistics", "Software Engineering", "Operations Research", "Data Visualization Tools"],
    6: ["Data Security", "Big Data Analytics", "Software Testing", "Cloud Computing", "Marketing Data Analytics"]
}

# Recommendations mapping
book_mapping = {
    "C Programming": "The C Programming Language by Kernighan and Ritchie",
    "Differential Equations": "Elementary Differential Equations by Boyce and DiPrima",
    "Fundamentals of IT": "Introduction to Information Technology by Turban, Rainer and Potter",
    "Descriptive Statistics": "Statistics for Engineers and Scientists by William Navidi",
    "General English 1": "Epitome of Wisdom by Maruthi Publications",
    "Value Education": "Human Values - Development Program by AIACHE",
    "DS through C": "Data Structures Using C by Aaron M. Tenenbaum",
    "Probability Distributions": "Introduction to Probability and Statistics by Mendenhall and Beaver",
    "Abstract Algebra": "Abstract Algebra by David S. Dummit and Richard M. Foote",
    "Operating Systems": "Operating System Concepts by Silberschatz, Galvin, and Gagne",
    "General English 2": "Epitome of Wisdom by Maruthi Publications",
    "Indian Heritage And Culture": "The Wonder That Was India by A.L. Basham",
    "Database Management Systems": "Database System Concepts by Silberschatz, Korth, and Sudarshan",
    "Computer Organizations": "Computer Organization and Design by Patterson and Hennessy",
    "Python": "Automate the Boring Stuff with Python by Al Sweigart",
    "Statistical Methods": "Statistics for Engineers and Scientists by William Navidi",
    "Environmental Studies": "Environmental Studies by Benny Joseph",
    "Java": "Effective Java by Joshua Bloch",
    "Statistical Inference": "Statistical Inference by Casella and Berger",
    "Computer Networks": "A Top-Down Approach by Kurose and Ross",
    "R Programming": "R for Data Science by Wickham and Grolemund",
    "Data Warehousing": "The Data Warehouse Toolkit by Ralph Kimball",
    "Accounting And Financial Management": "Financial Accounting by Libby, Libby, and Short",
    "Artificial Intelligence": "Artificial Intelligence: A Modern Approach by Russell and Norvig",
    "Machine Learning": "Pattern Recognition and Machine Learning by Christopher M. Bishop",
    "Applied Statistics": "Applied Statistics and Probability for Engineers by Montgomery and Runger",
    "Software Engineering": "Software Engineering by Ian Sommerville",
    "Operations Research": "Introduction to Operations Research by Hillier and Lieberman",
    "Data Visualization Tools": "Storytelling with Data by Cole Nussbaumer Knaflic",
    "Data Security": "Introduction to Algorithms by Cormen, Leiserson, Rivest, and Stein",
    "Big Data Analytics": "Big Data: A Revolution That Will Transform How We Live by Mayer-Schönberger",
    "Software Testing": "Software Testing by Ron Patton",
    "Cloud Computing": "Cloud Computing: Concepts, Technology & Architecture by Thomas Erl",
    "Marketing Data Analytics": "Marketing Analytics by Winston"
}

topic_mapping = {
    "C Programming": "Pointers, programming constructs, Control structures, Functions, Arrays and strings, Pointers and file handling",
    "Differential Equations": "First Order Differential Equations, Applications of differential equations, Interpolation",
    "Fundamentals of IT": "Computer terminology and number systems, Modern communication technologies, Applications of IT",
    "Descriptive Statistics": "Measures of central tendency, Measures of dispersion, Random variables, Probability basics",
    "General English 1": "Fundamentals of communication, Language proficiency, Writing skills",
    "Value Education": "Ethics, Moral values, Personality development, Life skills",
    "DS through C": "Arrays, Linked Lists, Stacks, Queues, Searching and sorting, Graphs, Trees",
    "Probability Distributions": "Binomial, Poisson, Normal Distributions, Sampling distributions",
    "Abstract Algebra": "Group theory, Normal subgroups, Permutations, Linear equation, Eigenvalues and eigenvectors",
    "Operating Systems": "Process Management, Memory Management, File systems, Deadlocks",
    "General English 2": "Advanced communication skills, Literary appreciation, Functional grammar",
    "Indian Heritage And Culture": "The Indus Valley Civilization, Vedic culture, Major empires, Religious traditions, Art, Architecture",
    "Database Management Systems": "SQL, Normalization, Indexing, Relational database concepts, NoSQL basics",
    "Computer Organizations": "CPU Architecture, Memory Hierarchy, Input/output systems",
    "Python": "Basic syntax, Libraries, Data manipulation, Object-oriented programming",
    "Statistical Methods": "Hypothesis testing, Regression analysis, Non-parametric tests, ANOVA",
    "Environmental Studies": "Environmental awareness, Sustainable development, Gender issues",
    "Java": "OOP, Exception Handling, Multithreading",
    "Statistical Inference": "Likelihood ratio tests, Bayesian inference, Hypothesis testing",
    "Computer Networks": "Input/output systems, Memory hierarchy, CPU architecture",
    "R Programming": "Statistical functions, Visualization, Basic syntax",
    "Data Warehousing": "Data warehouse architecture, OLAP, Association rules, Evaluation metrics",
    "Accounting And Financial Management": "Balance Sheets, Income Statements",
    "Artificial Intelligence": "Search Algorithms, Knowledge Representation, Adversarial search, Expert systems",
    "Machine Learning": "Supervised Learning, Unsupervised Learning, Model evaluation, Neural networks",
    "Applied Statistics": "Discriminant analysis, Time Series Analysis, Factor analysis, Growth curves",
    "Software Engineering": "Requirements engineering, SDLC, Testing methodologies",
    "Operations Research": "Linear Programming, Network flows, Transportation and assignment problems",
    "Data Visualization Tools": "Tools, Visualization principles, Visualizing complex data",
    "Data Security": "Firewalls, Security attacks, Encryption",
    "Big Data Analytics": "Hadoop Ecosystem, HBase, Hive, Pig, NoSQL",
    "Software Testing": "Testing types, Test case design, Quality metrics",
    "Cloud Computing": "Cloud model, Virtualization, Cloud architecture",
    "Marketing Data Analytics": "Market research, Market basket analysis, Customer segmentation"
}

# Define static folders
STATIC_DIR = Path("static/data/previous_papers")
SYLLABUS_DIR = Path("static/data/syllabus")
IMAGE_DIR = Path("static/images")

# Image paths (updated to .jpg)
IMAGE_PATHS = {
    "tracking": IMAGE_DIR / "tracking.jpg",
    "papers": IMAGE_DIR / "papers.jpg",
    "register": IMAGE_DIR / "register.jpg",
    "certificate": IMAGE_DIR / "certificate.jpg",
    "pen_paper": IMAGE_DIR / "pen_paper.jpg",
    "books": IMAGE_DIR / "books.jpg",
    "bulb": IMAGE_DIR / "bulb.jpg",
    "question_papers": IMAGE_DIR / "question_papers.jpg",
    "syllabus": IMAGE_DIR / "syllabus.jpg",
}

# Create syllabus file mapping based on your uploaded syllabus files
syllabus_mapping = {
    "Abstract Algebra": "Abstract_Algebra_Syllabus.pdf",
    "Accounting And Financial Management": "Accounting_And_Financial_Management_Syllabus.pdf",
    "Applied Statistics": "Applied_statistics_Syllabus.pdf",
    "Artificial Intelligence": "Artificial_Intelligence_Syllabus.pdf",
    "Big Data Analytics": "Big_Data_Analytics_Syllabus.pdf",
    "C Programming": "C_Programming_Syllabus.pdf",
    "Cloud Computing": "Cloud_Computing_Syllabus.pdf",
    "Computer Networks": "Computer_Networks_Syllabus.pdf",
    "Computer Organizations": "Computer_Organizations_Syllabus.pdf",
    "Data Security": "Data_Security_Syllabus.pdf",
    "Data Visualization Tools": "Data_Visualization_Tools_Syllabus.pdf",
    "Data Warehousing": "Data_Warehousing_Syllabus.pdf",
    "Database Management Systems": "Database_Management_Systems_Syllabus.pdf",
    "Descriptive Statistics": "Descriptive_Statistics_Syllabus.pdf",
    "Differential Equations": "Differential_Equations_Syllabus.pdf",
    "DS through C": "DS_through_C_Syllabus.pdf",
    "Environmental Studies": "Environmental_Studies_Syllabus.pdf",
    "Fundamentals of IT": "Fundamentals_of_IT_Syllabus.pdf",
    "General English 1": "General_English_1_Syllabus.pdf",
    "General English 2": "General_English_2_Syllabus.pdf",
    "Indian Heritage And Culture": "Indian_Heritage_And_Culture_Syllabus.pdf",
    "Java": "Java_Syllabus.pdf",
    "Machine Learning": "Machine_Learning_Syllabus.pdf",
    "Marketing Data Analytics": "Marketing_Data_Analytics_Syllabus.pdf",
    "Operating Systems": "Operating_Systems_Syllabus.pdf",
    "Operations Research": "Operations_Research_Syllabus.pdf",
    "Probability Distributions": "Probability_Distributions_Syllabus.pdf",
    "Python": "Python_Syllabus.pdf",
    "R Programming": "R_Programming_Syllabus.pdf",
    "Software Engineering": "Software_Engineering_Syllabus.pdf",
    "Software Testing": "Software_Testing_Syllabus.pdf",
    "Statistical Inference": "Statistical_Inference_Syllabus.pdf",
    "Statistical Methods": "Statistical_Methods_Syllabus.pdf",
    "Value Education": "Value_Education_Syllabus.pdf"
}

# Helper function to display images
def display_image(image_key, width=50):
    if IMAGE_PATHS[image_key].exists():
        st.image(str(IMAGE_PATHS[image_key]), width=width)
    else:
        st.image(f"https://via.placeholder.com/{width}x{width}.png?text={image_key.replace('_', '+')}", width=width)

# Streamlit App
st.title("Student Performance Prediction and Tracking")
display_image("tracking", width=100)

# Semester Selection Tabs
tabs = st.tabs([f"Semester {i}" for i in range(1, 7)])

# Initialize session state for tracking performance across semesters
if 'performance_data' not in st.session_state:
    st.session_state.performance_data = {}

for semester, tab in enumerate(tabs, start=1):
    with tab:
        st.header(f"Semester {semester} Performance Tracking")
        display_image("papers")
        
        student_data = {}
        
        # Subject inputs
        for subject in SEMESTER_SUBJECTS[semester]:
            student_data[subject] = st.number_input(
                f"{subject} (Max 60):", 
                min_value=0, 
                max_value=60, 
                value=0, 
                key=f"{semester}_{subject}"
            )
        
        # Common inputs with icons
        display_image("register")
        student_data["Attendance"] = st.number_input(
            "Attendance (Max 100):", 
            min_value=0, 
            max_value=100, 
            value=0, 
            key=f"{semester}_Attendance"
        )
        
        display_image("pen_paper")
        student_data["Assignments"] = st.number_input(
            "Assignments (Max 10):", 
            min_value=0, 
            max_value=10, 
            value=0, 
            key=f"{semester}_Assignments"
        )
        
        display_image("certificate")
        student_data["Participation"] = st.number_input(
            "Participation (Max 10):", 
            min_value=0, 
            max_value=10, 
            value=0, 
            key=f"{semester}_Participation"
        )

        if st.button("Submit & Predict Performance", key=f"submit_{semester}"):
            # Store the data in session state
            st.session_state.performance_data[semester] = student_data
            
            # Check pass/fail
            fail_conditions = {subject: student_data[subject] < 30 for subject in SEMESTER_SUBJECTS[semester]}
            subject_based_fail = any(fail_conditions.values())
            pass_status = 0 if subject_based_fail else 1

            # Calculate overall performance metrics
            total_marks = sum(student_data[subject] for subject in SEMESTER_SUBJECTS[semester])
            avg_score = total_marks / len(SEMESTER_SUBJECTS[semester])
            performance_percentage = (total_marks / (60 * len(SEMESTER_SUBJECTS[semester]))) * 100

            # Display performance metrics
            st.header("Performance Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Marks", f"{total_marks}/{(60 * len(SEMESTER_SUBJECTS[semester]))}")
            with col2:
                st.metric("Average Score", f"{avg_score:.1f}/60")
            with col3:
                st.metric("Performance", f"{performance_percentage:.1f}%")

            # Results
            if pass_status == 1:
                st.success("🎉 Status: Passed! All the best! 🎉")
                st.balloons()
            else:
                failed_subjects = [subject for subject in SEMESTER_SUBJECTS[semester] if fail_conditions[subject]]
                st.error("😓 Status: Needs Improvement 😓")
                st.subheader("Subjects Requiring Attention:")
                for subject in failed_subjects:
                    st.write(f"- {subject} (Score: {student_data[subject]}/60)")

                # Enhanced Recommendations
                recommendations = {
                    "Books": [],
                    "Important Topics": [],
                    "Previous Papers": [],
                    "Syllabus": []
                }
                
                for subject in failed_subjects:
                    if subject in book_mapping:
                        recommendations["Books"].append((subject, book_mapping[subject]))
                    if subject in topic_mapping:
                        recommendations["Important Topics"].append((subject, topic_mapping[subject]))
                    
                    # Previous Papers
                    pdf_path = STATIC_DIR / f"{subject.replace(' ', '_')}.pdf"
                    if pdf_path.exists():
                        recommendations["Previous Papers"].append((subject, pdf_path))
                    
                    # Syllabus
                    syllabus_filename = syllabus_mapping.get(subject)
                    if syllabus_filename:
                        syllabus_path = SYLLABUS_DIR / syllabus_filename
                        if syllabus_path.exists():
                            recommendations["Syllabus"].append((subject, syllabus_path))

                # Display recommendations
                if recommendations["Books"]:
                    st.subheader("Recommended Books:")
                    display_image("books")
                    for subject, book in recommendations["Books"]:
                        st.markdown(f"**{subject}:**")
                        st.write(book)
                        st.write("")

                if recommendations["Important Topics"]:
                    st.subheader("Important Topics to Focus On:")
                    display_image("bulb")
                    for subject, topics in recommendations["Important Topics"]:
                        st.markdown(f"**{subject}:**")
                        topic_list = [t.strip() for t in topics.split(',')]
                        for topic in topic_list:
                            st.write(f"- {topic}")
                        st.write("")

                if recommendations["Previous Papers"]:
                    st.subheader("Previous Question Papers:")
                    display_image("question_papers")
                    for subject, pdf_path in recommendations["Previous Papers"]:
                        try:
                            with open(pdf_path, "rb") as file:
                                st.download_button(
                                    label=f"Download {subject} Previous Papers",
                                    data=file,
                                    file_name=f"{subject}_Previous_Papers.pdf",
                                    mime="application/pdf"
                                )
                        except FileNotFoundError:
                            st.warning(f"Previous papers not available for {subject}")

                if recommendations["Syllabus"]:
                    st.subheader("Subject Syllabus:")
                    display_image("syllabus")
                    for subject, syllabus_path in recommendations["Syllabus"]:
                        try:
                            with open(syllabus_path, "rb") as file:
                                st.download_button(
                                    label=f"Download {subject} Syllabus",
                                    data=file,
                                    file_name=f"{subject}_Syllabus.pdf",
                                    mime="application/pdf"
                                )
                        except FileNotFoundError:
                            st.warning(f"Syllabus not available for {subject}")

# Add a summary section for all semesters
st.header("Overall Performance Summary")
if st.session_state.performance_data:
    summary_data = []
    for semester, data in st.session_state.performance_data.items():
        total_marks = sum(data[subject] for subject in SEMESTER_SUBJECTS[semester])
        max_possible = 60 * len(SEMESTER_SUBJECTS[semester])
        percentage = (total_marks / max_possible) * 100
        summary_data.append({
            "Semester": semester,
            "Total Marks": f"{total_marks}/{max_possible}",
            "Percentage": f"{percentage:.1f}%",
            "Status": "Pass" if all(data[subject] >= 30 for subject in SEMESTER_SUBJECTS[semester]) else "Needs Improvement"
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary.style.highlight_max(axis=0, subset=["Percentage"]))
else:
    st.info("No semester data available yet. Please submit data for at least one semester.")