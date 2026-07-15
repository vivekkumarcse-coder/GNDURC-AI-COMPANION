"""
Guru Nanak Dev RCC Information Chatbot
----------------------------------------
Python/Tkinter version of the original HTML/JS chatbot.

Run this file from a folder that also contains the image files
referenced below (same names as in the original web version):
    fees.jpeg
    Academic-calender.jpg
    engineering1.jpeg
    engineering2.jpeg
    electronic.jpeg
    commerce.jpeg
    law.jpeg

If an image is missing, the chatbot will simply show a small
placeholder message instead of crashing.
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import os
import re
import webbrowser

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ----------------------------------------------------------------------
# 1. ANSWERS DATABASE  (same content/keys as the JS "answers" object)
# ----------------------------------------------------------------------
# Images are referenced with the tag  {{IMG:filename.jpg}}
# and are rendered inline by the chat renderer below.
# Bold text is written as **text** and rendered bold.
# <br><br> from the original HTML becomes a blank line; <br> becomes
# a single newline; <hr> becomes a thin divider line.

ANSWERS = {

    "Hello":
        "Hello! How can I help you today?",

    "Admission Procedure":
        "Hello! Welcome to the Guru Nanak Dev University (GNDU) Admission Portal "
        "Support. I am your virtual assistant, here to walk you through the entire "
        "registration and admission structure for the 2026-27 academic session.\n\n"

        "With this breakdown, you can complete your entire application process "
        "smoothly right from home without needing to visit the campus office.\n\n"

        "Let's look at the main steps and structures you need to know:\n\n"

        "**Step I: Login Generation**\n"
        "You begin by entering your basic details on our portal to generate a "
        "unique login ID and password, which will be texted or emailed to you.\n\n"

        "**Step II: Online Registration**\n"
        "You must log in at www.gnduadmissions.org or www.gndu.ac.in to fill out "
        "your details and pay the non-refundable registration fee.\n\n"

        "**Step III: Application Form**\n"
        "After successful registration, you will log back in to fill out the "
        "detailed course-specific application form based on the official "
        "Admission Schedule 2026-27.\n\n"

        "**Step IV: Admit Card**\n"
        "If your program requires an Entrance Test, your admit card (detailing "
        "date, time, and venue) will be automatically generated upon successful "
        "submission.\n\n"

        "**2. Registration Fee Structure**\n"
        "Fees can be paid online via Credit Card, Debit Card, Net Banking, or "
        "through any HDFC Bank branch.\n\n"

        "General UG & PG Programs: \u20b91500 for General Category; \u20b9750 for "
        "SC Category (Punjab Domicile only).\n\n"

        "Engineering & Architecture: A one-time registration fee of \u20b92500 is "
        "charged for B.Tech (based on JEE) and B.Arch (based on NATA).\n\n"

        "**Sports Sciences (MYAS-GNDU Department)**\n"
        "One Program: \u20b91400 (Gen) / \u20b9700 (SC)\n"
        "Two Programs: \u20b91600 (Gen) / \u20b9800 (SC)\n"
        "More than two Programs: \u20b91700 (Gen) / \u20b9850 (SC)\n\n"

        "Foreign / NRI Students: $500 USD (plus an additional 8.5% commission "
        "fee if paid via PayPal).\n\n"

        "**3. Smart Program Grouping**\n"
        "GNDU groups similar courses together so you only have to submit one "
        "single form and a single fee to apply for multiple courses within that "
        "group.\n\n"

        "For example, Group-(v) covers B.Tech branches like Computer Science & "
        "Engineering, Artificial Intelligence & Machine Learning, Electronics & "
        "Communication, etc., based on your JEE Main performance.\n\n"

        "If you want to apply for programs outside your primary selected group, "
        "a separate application form must be submitted for each.\n\n"

        "**4. Mandatory Documents for Counselling**\n"
        "\u2022 Matriculation/Class 10th Certificate (Date of Birth proof)\n"
        "\u2022 Detailed Marks Card (DMC) of qualifying examination\n"
        "\u2022 Character Certificate from last attended institution\n"
        "\u2022 Two passport-size photographs\n"
        "\u2022 JEE Main Admit Card and Rank Card (for B.Tech applicants)\n\n"

        "**5. Entrance Exams, Qualifying Marks & Tie-Breakers**\n"
        "Minimum Entrance Cut-off:\n"
        "\u2022 General Category: 30%\n"
        "\u2022 SC/ST Category: 20%\n\n"

        "Tie-Breaking Rule:\n"
        "If candidates have equal entrance scores, preference is given to the "
        "candidate with higher qualifying examination marks. If the tie still "
        "remains, the older candidate is preferred.\n\n"

        "Provisional Admission:\n"
        "If your final results are pending, you may still attend counselling. "
        "Admission will remain provisional until eligibility requirements are "
        "fulfilled.\n\n"

        "**6. Campus Rules & Attendance Structure**\n"
        "\u2022 Minimum 75% attendance is mandatory separately in theory and "
        "practical classes.\n"
        "\u2022 Continuous absence of 15 days without informing the Head of "
        "Department can lead to removal from university rolls.\n"
        "\u2022 Ragging is strictly prohibited and attracts severe disciplinary "
        "and legal action.",

    "Courses Offered":
        "**\U0001F393 Academic Programs at GNDU Regional Campus, Gurdaspur**\n\n"

        "The campus offers a wide range of undergraduate, postgraduate, diploma, "
        "and doctoral programs designed to build professional competence and "
        "strong academic foundations.\n\n"

        "**1. Engineering & Technology**\n"
        "\u2022 B.Tech (Bachelor of Technology): Computer Science & Engineering, "
        "Electrical Engineering, Civil Engineering.\n"
        "\u2022 M.Tech (Regular): Civil, Mechanical, Electrical, Bio-Technology, "
        "Bio-Informatics, Electronics & Communication Engineering, Computer "
        "Science & Engineering.\n"
        "\u2022 M.Tech (Integrated): 5-Year Integrated Programs in Civil, "
        "Mechanical, Electrical, Electronics & Telecommunication, and Computer "
        "Science.\n"
        "\u2022 Core Stream: Computer Science & Engineering.\n\n"

        "**2. Computer Applications & Information Technology**\n"
        "\u2022 Bachelor of Computer Applications (BCA).\n"
        "\u2022 M.Sc. (Information Technology).\n"
        "\u2022 M.Sc. (Information Technology) Lateral Entry to III Semester.\n"
        "\u2022 Master of Computer Applications (MCA).\n"
        "\u2022 PGDCA (Post Graduate Diploma in Computer Applications).\n"
        "\u2022 Diploma in Computer Applications.\n"
        "\u2022 Diploma in Computer Programming & Information Technology.\n\n"

        "**3. Business, Management & Commerce**\n"
        "\u2022 Bachelor of Business Administration (BBA).\n"
        "\u2022 Bachelor of Commerce (B.Com).\n"
        "\u2022 Master of Commerce (M.Com).\n"
        "\u2022 MBA Specializations: Information Technology, Finance, Human "
        "Resources, Marketing, Insurance & Risk Management.\n\n"

        "**4. Sciences & Mathematics**\n"
        "\u2022 B.Sc. (Non-Medical).\n"
        "\u2022 M.Sc. (Mathematics).\n"
        "\u2022 Core Science Subjects: Botany, Mathematics, Zoology, Physics, "
        "Chemistry, Geology.\n"
        "\u2022 M.Sc. Programs: Physics, Chemistry, Botany, Zoology, "
        "Electronics.\n"
        "\u2022 Applied Sciences: Bio-Technology and Microbiology.\n"
        "\u2022 Agricultural Sciences: Agriculture, Horticulture, Dairy Science "
        "and Fisheries.\n\n"

        "**5. Medical, Health & Para-Medical Sciences**\n"
        "\u2022 Bachelor in Physiotherapy (BPT).\n"
        "\u2022 Diploma in Physiotherapy.\n"
        "\u2022 Bachelor in Optometry.\n"
        "\u2022 B.Sc. Medical Laboratory Technology (MLT).\n"
        "\u2022 B.Sc. Medical Radiography & Imaging Technology (MRIT).\n"
        "\u2022 Lateral Entry Available in MLT and MRIT Programs.\n"
        "\u2022 Diploma in Dialysis Technology.\n"
        "\u2022 Diploma in Operation Theatre Technology.\n"
        "\u2022 Diploma in Child Care & Nutrition.\n"
        "\u2022 Diploma in Homoeopathic Pharmacy.\n"
        "\u2022 Diploma CMS.\n\n"

        "**6. Humanities, Social Sciences & Languages**\n"
        "\u2022 BA Programs: History, Geography, English, Economics, Public "
        "Administration, Political Science, Education, Sociology, Psychology, "
        "Home Science, Music, Fine Arts, Punjabi, Hindi, Urdu, Arabic, Sanskrit, "
        "Bengali, Nepali, Rural Development and Disaster Management.\n"
        "\u2022 MA Programs: Public Administration, Economics, History, "
        "Political Science, Geography, Sociology, Psychology, Mathematics, Home "
        "Science, Rural Development, Disaster Management, Music, Fine Arts, "
        "English, Hindi, Punjabi, Sanskrit and Bengali.\n\n"

        "**7. Hospitality, Tourism & Design**\n"
        "\u2022 B.Sc. Hotel Management & Tourism.\n"
        "\u2022 Bachelor in Hotel Management (All Streams).\n"
        "\u2022 Fashion Technology Programs.\n"
        "\u2022 Diplomas in Fashion Designing, Textile Designing, Interior "
        "Designing, FRM and CAFD.\n"
        "\u2022 Vocational Diplomas in Embroidery and Cutting & Tailoring.\n\n"

        "**8. Law & Education**\n"
        "\u2022 Bachelor of Education (B.Ed.).\n"
        "\u2022 Specialized Law Programs under the Department of Laws.\n\n"

        "**9. Industrial Safety & Environmental Management**\n"
        "\u2022 Post Diploma in Industrial Safety.\n"
        "\u2022 PG Diploma in Industrial Safety & Environment Management.\n"
        "\u2022 PG Diploma in Environment & Pollution Management.\n"
        "\u2022 Core Diplomas in Industrial Safety, Industrial Safety & Fire, "
        "Fire Safety, and Health, Safety & Environment.\n\n"

        "**10. Vocational & Technical Diplomas**\n"
        "\u2022 Diploma in Secretarial Practice.\n"
        "\u2022 Engineering Diplomas in Mechanical, Civil, Electrical, "
        "Electronics & Communication, Refrigeration & Air Conditioning, "
        "Computer Science/IT, Chemical, and Automobile Engineering.\n\n"

        "For detailed eligibility criteria, fee structure, admission schedule, "
        "and seat availability, please refer to the official GNDU admission "
        "portal or contact the Regional Campus administration office.",

    "Fee Structure":
        "{{IMG:fees.jpeg}}",

    "Hostel Facilities":
        "**\U0001F6CF\uFE0F Hostel Charges & Accommodation Information**\n\n"

        "Welcome back to the Guru Nanak Dev University Regional Campus, "
        "Gurdaspur Helpdesk.\n\n"

        "**\U0001F3E0 Hostel Annual Charges & Security**\n\n"

        "At the time of admission, hostel residents are required to pay the "
        "following charges based on their category:\n\n"

        "**For New Students**\n"
        "\u2022 Annual Charges (Sharing Basis): Rs. 19,550/-\n"
        "\u2022 Annual Charges (Single Basis): Rs. 21,050/-\n"
        "\u2022 Mess Security (Refundable): Rs. 6,000/-\n\n"

        "**For Existing Students**\n"
        "\u2022 Annual Charges (Sharing Basis): Rs. 17,850/-\n"
        "\u2022 Annual Charges (Single Basis): Rs. 19,050/-\n"
        "\u2022 Mess Security (Refundable): Rs. 5,000/-\n\n"

        "**\U0001F37D\uFE0F Mess Charges (Diet Rates)**\n\n"

        "Each hostel resident is required to pay minimum monthly mess charges "
        "calculated on a fixed daily diet rate.\n\n"

        "\u2022 Boys Hostel: Minimum monthly mess charges of Rs. 900/- (Rs. 27 "
        "per diet).\n"
        "\u2022 Girls Hostel: Minimum monthly mess charges of Rs. 800/- (Rs. 25 "
        "per diet).\n\n"

        "**\U0001F4DE Important Hostel Contact Numbers**\n\n"

        "For hostel allotment, room availability, permissions, or other "
        "hostel-related queries, students may contact:\n\n"

        "\u2022 Madam Jyoti: 95010-21178\n"
        "\u2022 Hostel Contact: 89681-91313\n"
        "\u2022 Hostel Warden / Staff: 84378-60666\n\n"

        "**\U0001F4CC Note**\n"
        "Hostel fees, mess charges, and security deposits are subject to "
        "revision by the university from time to time. Students are advised to "
        "verify the latest fee structure with the hostel office before "
        "admission.",

    "Placement Information":
        "**\U0001F4BC Placement & Industry Collaborations**\n\n"
        "Guru Nanak Dev University (GNDU) Regional Campus, Gurdaspur maintains "
        "a strong Training and Placement ecosystem that bridges the gap between "
        "academic learning and industry requirements.\n\n"
        "Through active collaborations with leading multinational corporations, "
        "IT companies, manufacturing industries, financial institutions, and "
        "educational organizations, the campus provides students with excellent "
        "opportunities for internships, industrial training, skill development, "
        "and campus placements.\n\n"
        "**\U0001F3E2 Major Recruiters at GNDU Regional Campus, Gurdaspur**\n\n"
        "1. Tech Mahindra\n"
        "2. Nagarro\n"
        "3. John Deere\n"
        "4. Decathlon\n"
        "5. IBM\n"
        "6. Amdocs\n"
        "7. HCL Technologies\n"
        "8. Statusbrew\n"
        "9. Infogain\n"
        "10. SAP\n"
        "11. Trident Group\n"
        "12. Jubilant\n"
        "13. ITC Limited\n"
        "14. ValeurHR\n"
        "15. Canam Enterprises\n"
        "16. Nestl\u00e9 India\n"
        "17. Navyug Infosolutions\n"
        "18. HDFC Bank\n"
        "19. CCI\n"
        "20. Azim Premji University\n"
        "21. Berger Paints\n"
        "22. BOMA\n"
        "23. Axis Bank\n"
        "24. Tata Consultancy Services (TCS)\n"
        "25. Capgemini\n"
        "26. Wipro\n"
        "27. Aakash Educational Services Limited (AESL)\n"
        "28. Accenture\n\n"
        "**\U0001F4C8 Placement Support Services**\n"
        "\u2022 Campus Recruitment Drives\n"
        "\u2022 Industrial Training Programs\n"
        "\u2022 Internship Opportunities\n"
        "\u2022 Technical Skill Development Workshops\n"
        "\u2022 Aptitude & Soft Skills Training\n"
        "\u2022 Resume Building Sessions\n"
        "\u2022 Mock Interviews & Group Discussions\n"
        "\u2022 Career Counseling and Guidance\n\n"
        "GNDU Regional Campus continuously works to strengthen "
        "industry-academia partnerships, ensuring students are equipped with "
        "the skills, knowledge, and professional exposure required for "
        "successful careers in today's competitive job market.",

    "Academic Calendar":
        "The academic calendar includes semester schedules, examinations, "
        "holidays and college events.\n\n"
        "{{IMG:Academic-calender.jpg}}",

    "Scholarships":
        "**\U0001F393 Scholarships & Financial Assistance at GNDU Regional "
        "Campus, Gurdaspur**\n\n"
        "Hello! Welcome to the Guru Nanak Dev University (GNDU) Regional "
        "Campus, Gurdaspur Helpdesk.\n\n"
        "As a student of GNDU, you can benefit from a wide range of "
        "scholarships and financial assistance programs designed to support "
        "academic excellence and ensure equal educational opportunities for "
        "all students.\n\n"
        "**\U0001F3DB\uFE0F Government & Central Scholarship Schemes**\n\n"
        "The university facilitates several Central Government, State "
        "Government, and National Scholarship programs for eligible "
        "students.\n\n"
        "**Targeted Financial Assistance**\n"
        "\u2022 Scholarships for meritorious students.\n"
        "\u2022 Financial support for economically weaker section (EWS) "
        "students.\n"
        "\u2022 Assistance for handicapped, disabled, and visually impaired "
        "students.\n\n"
        "**DPI Punjab Scholarship Programs**\n"
        "\u2022 Post Matric Scholarship for SC students.\n"
        "\u2022 Post Matric Scholarship for OBC students.\n"
        "\u2022 Punjab State Merit Scholarship Scheme.\n\n"
        "**National & Central Government Scholarship Schemes**\n"
        "\u2022 National Scholarships (Post Matric Scholarship for "
        "Minorities).\n"
        "\u2022 Merit-cum-Means Scholarships for Professional and Technical "
        "Courses.\n"
        "\u2022 Central Sector Scheme of Scholarships for College and "
        "University Students.\n"
        "\u2022 Prime Minister's Scholarship Scheme for Central Armed Police "
        "Forces (CAPF) and Assam Rifles personnel wards.\n\n"
        "**\U0001F393 University Endowment Fund Scholarships**\n\n"
        "GNDU also provides scholarships through various donor-funded and "
        "university endowment funds.\n\n"
        "**General Merit Scholarships**\n"
        "\u2022 Harnarinder Jot Sarup Scholarship.\n"
        "\u2022 Mahesh Dutt Bhalla and Jaswant Kaur Bhalla Scholarship.\n"
        "\u2022 Prof. M.P. Satija Scholarship.\n\n"
        "**Library Science Scholarships**\n"
        "\u2022 Smt. Satinder Kaur Ramdev Scholarship (for Library Science "
        "students).\n"
        "\u2022 Prof. Jaginder Singh Ramdev Annual Scholarship awarded to the "
        "top two GNDU students of B.Lib.I.Sc. who secure admission into "
        "M.Lib.I.Sc. during the next academic session.\n\n"
        "**\U0001F469\u200D\U0001F393 Rural Girl Child Empowerment "
        "Scholarship**\n"
        "Balram Kaur Scholarship is available for girl students in the "
        "Department of Library Science and Information who meet any of the "
        "following criteria:\n"
        "\u2022 Belong to Chicha or Bhakna villages.\n"
        "\u2022 Belong to rural areas of Amritsar district.\n"
        "\u2022 Are meritorious students from any rural area of Punjab.\n\n"
        "**\U0001F52C Special Scholarships for Science Students**\n\n"
        "Special scholarships are available for students enrolled in the "
        "following science programs:\n"
        "\u2022 B.Sc. (Hons. School).\n"
        "\u2022 M.Sc. (Hons. School).\n"
        "\u2022 M.Sc. Human Genetics.\n\n"
        "**\U0001F4CC Important Note**\n"
        "Eligibility conditions, scholarship amounts, application deadlines, "
        "and required documents may vary depending on the scheme. Students "
        "are advised to regularly check university notices and scholarship "
        "announcements for the latest updates.\n\n"
        "GNDU Regional Campus is committed to ensuring that financial "
        "constraints never become a barrier to quality education and academic "
        "success.",

    "Contact Details":
        "**ENGINEERING AND TECHNOLOGY:**\n"
        "{{IMG:engineering1.jpeg}}\n"
        "{{IMG:engineering2.jpeg}}\n"
        "{{HR}}\n"
        "**ELECTRONIC AND COMMUNICATION:**\n"
        "{{IMG:electronic.jpeg}}\n"
        "**BUSINESS AND COMMERCE:**\n"
        "{{IMG:commerce.jpeg}}\n"
        "**LAW:**\n"
        "{{IMG:law.jpeg}}",
}


# ----------------------------------------------------------------------
# 2. MAIN APPLICATION CLASS
# ----------------------------------------------------------------------
class ChatbotApp:

    IMAGE_MAX_WIDTH = 480   # mirrors the "max-width:600px" CSS rule, scaled
                            # down a bit to fit comfortably in the window

    def __init__(self, root):
        self.root = root
        self.root.title("Guru Nanak Dev RCC Information Chatbot")
        self.root.geometry("820x680")
        self.root.minsize(600, 500)
        self.root.configure(bg="#e8f4ff")

        # Keep references to PhotoImage objects so they are not
        # garbage-collected after being placed in the Text widget.
        self._image_refs = []

        # Folder the script is run from -> used to locate image files
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self._build_fonts()
        self._build_ui()
        self._show_welcome_message()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_fonts(self):
        self.font_normal = tkfont.Font(family="Arial", size=11)
        self.font_bold = tkfont.Font(family="Arial", size=11, weight="bold")
        self.font_title = tkfont.Font(family="Arial", size=18, weight="bold")
        self.font_button = tkfont.Font(family="Arial", size=11)

    def _build_ui(self):
        # ---- Outer "card" container, mirrors .container ----
        card = tk.Frame(self.root, bg="white", bd=0,
                         highlightbackground="#cccccc", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        # ---- Title ----
        title = tk.Label(
            card, text="\U0001F393 Guru Nanak Dev RCC Information Chatbot",
            font=self.font_title, fg="#003366", bg="white", pady=15
        )
        title.pack(fill="x")

        # ---- Chat area (Text widget + Scrollbar), mirrors #chatArea ----
        chat_frame = tk.Frame(card, bg="white")
        chat_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side="right", fill="y")

        self.chat_area = tk.Text(
            chat_frame,
            wrap="word",
            bg="#fafafa",
            relief="solid",
            bd=1,
            padx=10,
            pady=10,
            font=self.font_normal,
            yscrollcommand=scrollbar.set,
            state="disabled",
            cursor="arrow",
        )
        self.chat_area.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.chat_area.yview)

        # Text tag styling (mirrors .message.user / .message.bot / bold)
        self.chat_area.tag_configure(
            "user_label", font=self.font_bold, foreground="#003366"
        )
        self.chat_area.tag_configure(
            "bot_label", font=self.font_bold, foreground="#0a6e0a"
        )
        self.chat_area.tag_configure("bold", font=self.font_bold)
        self.chat_area.tag_configure(
            "user_bg", background="#d6ecff", lmargin1=80, lmargin2=80,
            rmargin=10, spacing1=6, spacing3=10, justify="right"
        )
        self.chat_area.tag_configure(
            "bot_bg", background="#dff5df", lmargin1=10, lmargin2=10,
            rmargin=80, spacing1=6, spacing3=10, justify="left"
        )
        self.chat_area.tag_configure(
            "hr", foreground="#999999", spacing1=4, spacing3=4
        )
        self.chat_area.tag_configure(
            "missing_img", foreground="#aa3333", font=self.font_normal
        )

        # ---- Controls (Select + Send + Clear), mirrors .controls ----
        controls = tk.Frame(card, bg="white")
        controls.pack(fill="x", padx=15, pady=(0, 15))

        self.question_var = tk.StringVar()
        self.question_options = ["-- Select Query --"] + list(ANSWERS.keys())
        self.question_var.set(self.question_options[0])

        self.dropdown = ttk.Combobox(
            controls,
            textvariable=self.question_var,
            values=self.question_options,
            state="readonly",
            width=30,
            font=self.font_button,
        )
        self.dropdown.pack(side="left", padx=(0, 10), ipady=3)

        send_btn = tk.Button(
            controls, text="Send", command=self.send_message,
            bg="#003366", fg="white", activebackground="#00224d",
            activeforeground="white", relief="flat", padx=20, pady=6,
            font=self.font_button, cursor="hand2"
        )
        send_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(
            controls, text="Clear Chat", command=self.clear_chat,
            bg="#003366", fg="white", activebackground="#00224d",
            activeforeground="white", relief="flat", padx=20, pady=6,
            font=self.font_button, cursor="hand2"
        )
        clear_btn.pack(side="left", padx=5)

        # Allow pressing Enter (with dropdown focused) to send as well
        self.root.bind("<Return>", lambda event: self.send_message())

    # ------------------------------------------------------------------
    # Chat behaviour
    # ------------------------------------------------------------------
    def _show_welcome_message(self):
        self._append_bot_message(
            "Hello! Welcome to Guru Nanak Dev RCC Information Chatbot. "
            "Select a query below to get started."
        )

    def send_message(self):
        question = self.question_var.get()

        if not question or question == self.question_options[0]:
            self._alert("Please select a query.")
            return

        self._append_user_message(question)

        # Mirrors the 500ms setTimeout delay before the bot responds
        self.root.after(500, lambda: self._respond_to(question))

        # Reset dropdown back to placeholder (mirrors selectedIndex = 0)
        self.question_var.set(self.question_options[0])

    def _respond_to(self, question):
        answer = ANSWERS.get(
            question,
            "Sorry, I don't have information on that topic right now."
        )
        self._append_bot_message(answer)

    def clear_chat(self):
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", "end")
        self.chat_area.configure(state="disabled")
        self._image_refs.clear()
        self._append_bot_message("Chat cleared. How may I assist you?")

    def _alert(self, message):
        # Simple modal alert, mirrors JS alert()
        top = tk.Toplevel(self.root)
        top.title("Notice")
        top.resizable(False, False)
        top.transient(self.root)
        tk.Label(top, text=message, padx=25, pady=15,
                 font=self.font_normal).pack()
        tk.Button(top, text="OK", command=top.destroy, width=10,
                  bg="#003366", fg="white", relief="flat",
                  padx=5, pady=4).pack(pady=(0, 15))
        top.grab_set()
        top.focus_set()

    # ------------------------------------------------------------------
    # Message rendering
    # ------------------------------------------------------------------
    def _append_user_message(self, text):
        self.chat_area.configure(state="normal")
        start = self.chat_area.index("end-1c")
        self.chat_area.insert("end", "You: ", "user_label")
        self.chat_area.insert("end", text + "\n")
        end = self.chat_area.index("end-1c")
        self.chat_area.tag_add("user_bg", start, end)
        self.chat_area.insert("end", "\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def _append_bot_message(self, content):
        self.chat_area.configure(state="normal")
        start = self.chat_area.index("end-1c")
        self.chat_area.insert("end", "Bot: ", "bot_label")
        self._render_bot_content(content)
        self.chat_area.insert("end", "\n")
        end = self.chat_area.index("end-1c")
        self.chat_area.tag_add("bot_bg", start, end)
        self.chat_area.insert("end", "\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def _render_bot_content(self, content):
        """
        Parses the answer string for:
          {{IMG:filename}} -> inline image
          {{HR}}           -> horizontal divider
          **bold text**    -> bold styling
          \n               -> newline
        and inserts everything into the Text widget in order.
        """
        # Split on image/hr placeholders while keeping the placeholders
        tokens = re.split(r"(\{\{IMG:[^}]+\}\}|\{\{HR\}\})", content)

        for token in tokens:
            if not token:
                continue

            img_match = re.match(r"\{\{IMG:([^}]+)\}\}", token)
            if img_match:
                filename = img_match.group(1)
                self.chat_area.insert("end", "\n")
                self._insert_image(filename)
                self.chat_area.insert("end", "\n")
                continue

            if token == "{{HR}}":
                self.chat_area.insert(
                    "end", "\n" + ("\u2500" * 40) + "\n", "hr"
                )
                continue

            # Handle **bold** segments within this plain-text token
            self._insert_text_with_bold(token)

    def _insert_text_with_bold(self, text):
        parts = re.split(r"(\*\*.*?\*\*)", text)
        for part in parts:
            if part.startswith("**") and part.endswith("**") and len(part) >= 4:
                self.chat_area.insert("end", part[2:-2], "bold")
            else:
                self.chat_area.insert("end", part)

    def _insert_image(self, filename):
        image_path = os.path.join(self.base_dir, filename)

        if not PIL_AVAILABLE:
            self.chat_area.insert(
                "end",
                f"[Image: {filename}]  (install 'Pillow' via "
                f"'pip install Pillow' to display images)\n",
                "missing_img",
            )
            return

        if not os.path.isfile(image_path):
            self.chat_area.insert(
                "end",
                f"[Image not found: {filename} — make sure it is in the "
                f"same folder as this script]\n",
                "missing_img",
            )
            return

        try:
            pil_image = Image.open(image_path)

            # Scale down to IMAGE_MAX_WIDTH while preserving aspect ratio,
            # mirroring the CSS "max-width:600px" rule.
            w, h = pil_image.size
            if w > self.IMAGE_MAX_WIDTH:
                ratio = self.IMAGE_MAX_WIDTH / float(w)
                new_size = (self.IMAGE_MAX_WIDTH, int(h * ratio))
                pil_image = pil_image.resize(new_size, Image.LANCZOS)

            tk_image = ImageTk.PhotoImage(pil_image)
            self._image_refs.append(tk_image)  # prevent garbage collection

            self.chat_area.image_create("end", image=tk_image)

        except Exception as exc:
            self.chat_area.insert(
                "end",
                f"[Could not load image '{filename}': {exc}]\n",
                "missing_img",
            )


# ----------------------------------------------------------------------
# 3. ENTRY POINT
# ----------------------------------------------------------------------
def main():
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()