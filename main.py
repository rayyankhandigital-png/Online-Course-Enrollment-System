import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------- Inheritance / Polymorphism ----------
class Person:
    def __init__(self, name):
        self.name = name

    def get_details(self):
        return f"Name: {self.name}"

class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course

    def get_details(self):
        return f"Student: {self.name}, Course: {self.course}"

class Admin(Person):
    def __init__(self, name="Admin"):
        super().__init__(name)

    def get_details(self):
        return f"Admin User: {self.name}"

# ---------- GUI ----------
class EnrollmentSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("💻 Online Course Enrollment System")
        self.master.geometry("950x600")
        self.master.configure(bg="#fdf6f0")
        self.filename = "enrollments_data.json"

        # Courses & Descriptions
        self.courses = {
            "🐍 Python Programming": "Learn syntax, functions, OOP, and libraries like NumPy and Tkinter.",
            "📊 Data Science": "Explore pandas, data wrangling, EDA, and visualization with matplotlib and seaborn.",
            "🤖 Machine Learning": "Understand supervised, unsupervised models using Scikit-Learn and TensorFlow.",
            "🌐 Web Development": "HTML, CSS, JavaScript, Flask, Django to build dynamic web apps.",
            "🔐 Cyber Security": "Learn ethical hacking, encryption, malware analysis, and security protocols.",
            "☁️ Cloud Computing": "Work with AWS, Azure, deployment, and architecture fundamentals.",
            "🎨 UI/UX Design": "Design thinking, wireframes, mockups using Figma & Adobe XD.",
            "🧠 Artificial Intelligence": "Explore NLP, CV, neural networks, deep learning concepts.",
            "📱 Mobile App Development": "Build iOS/Android apps using Flutter, Kotlin or React Native.",
            "🎮 Game Development": "Create games using Unity, Unreal Engine and C# or Blueprints.",
            "⚙️ DevOps": "Master Docker, Jenkins, CI/CD pipelines, GitHub Actions and deployment."
        }

        self.setup_styles()
        self.setup_tabs()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook.Tab", font=("Arial", 14, "bold"), padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", "#ffa07a")], foreground=[("selected", "#2c3e50")])
        style.configure("TButton", font=("Arial", 13), padding=6)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))
        style.configure("Treeview", font=("Arial", 12), rowheight=28)

    def setup_tabs(self):
        tab_control = ttk.Notebook(self.master)

        self.student_tab = tk.Frame(tab_control, bg="#fcefee")
        self.admin_tab = tk.Frame(tab_control, bg="#eafcfc")

        tab_control.add(self.student_tab, text="🎓 Student Form")
        tab_control.add(self.admin_tab, text="🛠️ Admin Area")
        tab_control.pack(expand=1, fill="both")

        self.setup_student_tab()
        self.setup_admin_tab()

    # ---------- Student Tab ----------
    def setup_student_tab(self):
        tk.Label(self.student_tab, text="Enter Your Name🔽:", font=("Arial", 15, "bold"),
                 bg="#fcefee", fg="#5c1a1b").pack(pady=10)
        self.name_entry = tk.Entry(self.student_tab, width=35, font=("Arial", 14), bg="#fff0f5", fg="#333")
        self.name_entry.pack(pady=5)

        tk.Label(self.student_tab, text="Select a Course🔽:", font=("Arial", 15, "bold"),
                 bg="#fcefee", fg="#5c1a1b").pack(pady=10)
        self.course_cb = ttk.Combobox(self.student_tab, values=list(self.courses.keys()), state="readonly",
                                      width=40, font=("Arial", 13))
        self.course_cb.pack()
        self.course_cb.bind("<<ComboboxSelected>>", self.update_description)

        tk.Label(self.student_tab, text="Course Description:", font=("Arial", 15, "bold"),
                 bg="#fcefee", fg="#5c1a1b").pack(pady=10)
        self.description_text = tk.Text(self.student_tab, width=70, height=6, font=("Arial", 12),
                                        wrap="word", bg="#fffff0", fg="#333", borderwidth=2, relief="groove")
        self.description_text.pack(pady=5)

        tk.Button(self.student_tab, text="📘 Enroll Now", command=self.enroll_student,
                  font=("Arial", 14, "bold"), bg="#27ae60", fg="white", width=20).pack(pady=20)

    def update_description(self, event):
        course = self.course_cb.get()
        description = self.courses.get(course, "No description available.")
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert(tk.END, description)

    def enroll_student(self):
        name = self.name_entry.get().strip()
        course = self.course_cb.get()

        try:
            if not name or not course:
                raise ValueError("Please enter your name and select a course.")

            student = Student(name, course)
            enrollment = {"name": student.name, "course": student.course}
            self.save_to_file(enrollment)

            messagebox.showinfo("Success", f"{student.get_details()} has been enrolled!")
            self.name_entry.delete(0, tk.END)
            self.course_cb.set("")
            self.description_text.delete("1.0", tk.END)
        except ValueError as ve:
            messagebox.showwarning("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")

    # ---------- Admin Tab ----------
    def setup_admin_tab(self):
        header_frame = tk.Frame(self.admin_tab, bg="#eafcfc")
        header_frame.pack(pady=15)

        ttk.Button(header_frame, text="👁️ View All", command=self.view_enrollments).grid(row=0, column=0, padx=8)
        ttk.Button(header_frame, text="❌ Delete All", command=self.delete_all).grid(row=0, column=1, padx=8)

        self.search_entry = ttk.Entry(header_frame, width=25, font=("Arial", 12))
        self.search_entry.grid(row=0, column=2, padx=8)
        ttk.Button(header_frame, text="🔍 Search", command=self.search_enrollment).grid(row=0, column=3)

        tree_frame = tk.Frame(self.admin_tab, bg="#eafcfc")
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Course"), show="headings", height=15)
        self.tree.heading("Name", text="🔍 Student Name")
        self.tree.heading("Course", text="🗂️ Enrolled Course")
        self.tree.column("Name", anchor="center", width=300)
        self.tree.column("Course", anchor="center", width=400)

        self.tree.tag_configure("evenrow", background="#e0f7fa")
        self.tree.tag_configure("oddrow", background="#ffffff")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)

    def view_enrollments(self):
        try:
            self.tree.delete(*self.tree.get_children())
            data = self.load_from_file()
            for i, entry in enumerate(data):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values=(entry["name"], entry["course"]), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load enrollments: {str(e)}")

    def delete_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all enrollments?"):
            try:
                with open(self.filename, "w") as f:
                    json.dump([], f)
                self.tree.delete(*self.tree.get_children())
                messagebox.showinfo("Deleted", "All enrollments have been cleared.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")

    def search_enrollment(self):
        keyword = self.search_entry.get().strip().lower()
        try:
            self.tree.delete(*self.tree.get_children())
            data = self.load_from_file()
            results = [d for d in data if keyword in d["name"].lower() or keyword in d["course"].lower()]
            if results:
                for i, entry in enumerate(results):
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.tree.insert("", tk.END, values=(entry["name"], entry["course"]), tags=(tag,))
            else:
                messagebox.showinfo("No Results", "❌ No matching enrollments found.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    # ---------- File Handling ----------
    def save_to_file(self, entry):
        try:
            data = self.load_from_file()
            data.append(entry)
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def load_from_file(self):
        try:
            if not os.path.exists(self.filename):
                return []
            with open(self.filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        except Exception as e:
            raise e

# ---------- Main ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = EnrollmentSystem(root)
    root.mainloop()
