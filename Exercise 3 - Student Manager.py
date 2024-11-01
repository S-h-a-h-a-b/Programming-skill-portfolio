import tkinter as tk
from tkinter import ttk, messagebox

# class to store student data
class Student:
    def __init__(self, student_id, name, course1, course2, course3, exam):
        self.student_id = student_id
        self.name = name
        self.course1 = int(course1)
        self.course2 = int(course2)
        self.course3 = int(course3)
        self.exam = int(exam)
        
    def total_coursework(self):
        return self.course1 + self.course2 + self.course3
    
    def overall_percentage(self):
        total = self.total_coursework() + self.exam
        return (total / 160) * 100
    
    def grade(self):
        # give grade based on percentage
        percentage = self.overall_percentage()
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

# class to handle stundent records and stuff
class StudentManager:
    def __init__(self):
        self.students = []
        self.load_data()
        
        # set up main window
        self.window = tk.Tk()
        self.window.title("Student Manager")
        self.window.geometry("800x600")
        
        heading = tk.Label(self.window, text="Student Manager", font=("Arial", 24))
        heading.pack(pady=20)
        
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        # create buttons
        tk.Button(button_frame, text="View All Student Records", 
                 command=self.view_all_records).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show Highest Score", 
                 command=self.show_highest_score).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show Lowest Score", 
                 command=self.show_lowest_score).pack(side=tk.LEFT, padx=5)
        
        # dropdown menu for selecting individual records
        select_frame = tk.Frame(self.window)
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="View Individual Student Record:").pack(side=tk.LEFT)
        self.student_var = tk.StringVar()
        student_dropdown = ttk.Combobox(select_frame, textvariable=self.student_var)
        student_dropdown['values'] = [student.name for student in self.students]
        student_dropdown.pack(side=tk.LEFT, padx=5)
        tk.Button(select_frame, text="View Record", 
                 command=self.view_individual_record).pack(side=tk.LEFT)
        
        # text area
        self.output_text = tk.Text(self.window, height=20, width=80)
        self.output_text.pack(pady=10)
        
    def load_data(self):
        # take data from file
        try:
            with open("/Users/shahabmughal/Documents/Level 5 Sem 1/Advance Programming/Assessment 1/studentMarks.txt", "r") as file:
                num_students = int(file.readline().strip())
                for _ in range(num_students):
                    line = file.readline().strip().split(',')
                    self.students.append(Student(line[0], line[1], line[2], 
                                              line[3], line[4], line[5]))
        except FileNotFoundError:
            # show error if file not found
            messagebox.showerror("Error", "studentMarks.txt file not found in resources folder")
            self.window.destroy()
            return
        
    def format_student_record(self, student):
        # display format for the data
        return (f"Name: {student.name}\n"
                f"Student Number: {student.student_id}\n"
                f"Total Coursework: {student.total_coursework()}/60\n"
                f"Exam Mark: {student.exam}/100\n"
                f"Overall Percentage: {student.overall_percentage():.1f}%\n"
                f"Grade: {student.grade()}\n")
    
    def view_all_records(self):
        # display rrecords of all students and calculate percentage
        self.output_text.delete(1.0, tk.END)
        total_percentage = 0
        for student in self.students:
            self.output_text.insert(tk.END, self.format_student_record(student) + "\n")
            total_percentage += student.overall_percentage()
        
        avg_percentage = total_percentage / len(self.students)
        summary = (f"\nSummary:\n"
                  f"Number of students: {len(self.students)}\n"
                  f"Average percentage: {avg_percentage:.1f}%\n")
        self.output_text.insert(tk.END, summary)
    
    def view_individual_record(self):
        # display record for ssingle student
        selected_name = self.student_var.get()
        for student in self.students:
            if student.name == selected_name:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, self.format_student_record(student))
                return
    
    def show_highest_score(self):
        # display record of student with highest percentage
        highest_student = max(self.students, 
                            key=lambda x: x.overall_percentage())
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Student with Highest Score:\n\n")
        self.output_text.insert(tk.END, self.format_student_record(highest_student))
    
    def show_lowest_score(self):
        # display record of student with lowest percentage
        lowest_student = min(self.students, 
                           key=lambda x: x.overall_percentage())
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Student with Lowest Score:\n\n")
        self.output_text.insert(tk.END, self.format_student_record(lowest_student))
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = StudentManager()
    app.run()
