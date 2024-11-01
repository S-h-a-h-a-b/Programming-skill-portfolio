import tkinter as tk
from tkinter import ttk, messagebox
import os

# class to store student data
class Student:
    def __init__(self, code, name, course1, course2, course3, exam):
        self.code = code
        self.name = name
        self.course_marks = [int(course1), int(course2), int(course3)]
        self.exam_mark = int(exam)
    
    def get_total_coursework(self):
        return sum(self.course_marks)
    
    def get_overall_percentage(self):
        total_marks = self.get_total_coursework() + self.exam_mark
        return (total_marks / 160) * 100
    
    def get_grade(self):
        # give grade based on percentage
        percentage = self.get_overall_percentage()
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
    
    def get_display_text(self):
        # display format for the data
        return (f"Name: {self.name}\n"
                f"Number: {self.code}\n"
                f"Coursework Total: {self.get_total_coursework()}\n"
                f"Exam Mark: {self.exam_mark}\n"
                f"Overall Percentage: {self.get_overall_percentage():.2f}%\n"
                f"Grade: {self.get_grade()}")

class AddStudentWindow:
    def __init__(self, parent, callback):
        # window to add new record
        self.window = tk.Toplevel(parent)
        self.window.title("Add Student")
        self.window.geometry("400x550")
        self.callback = callback
        
        # labels and entry for details
        labels = ['Student Code (1000-9999):', 'Name:', 'Course 1 Mark (0-20):',
                 'Course 2 Mark (0-20):', 'Course 3 Mark (0-20):', 'Exam Mark (0-100):']
        self.entries = {}
        
        for label in labels:
            tk.Label(self.window, text=label).pack(pady=5)
            entry = tk.Entry(self.window)
            entry.pack(pady=5)
            self.entries[label] = entry
        
        tk.Button(self.window, text="Add Student", command=self.add_student).pack(pady=10)
    
    def add_student(self):
        # check all the inputs and then add record or display error
        try:
            code = self.entries['Student Code (1000-9999):'].get()
            if not (1000 <= int(code) <= 9999):
                raise ValueError("Invalid student code")
            
            name = self.entries['Name:'].get()
            if not name:
                raise ValueError("Name cannot be empty")
            
            course_marks = [
                int(self.entries['Course 1 Mark (0-20):'].get()),
                int(self.entries['Course 2 Mark (0-20):'].get()),
                int(self.entries['Course 3 Mark (0-20):'].get())
            ]
            if not all(0 <= mark <= 20 for mark in course_marks):
                raise ValueError("Course marks must be between 0 and 20")
            
            exam = int(self.entries['Exam Mark (0-100):'].get())
            if not 0 <= exam <= 100:
                raise ValueError("Exam mark must be between 0 and 100")
            
            student = Student(code, name, *course_marks, exam)
            self.callback(student)
            self.window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class UpdateStudentWindow:
    def __init__(self, parent, student, callback):
        # window to update record
        self.window = tk.Toplevel(parent)
        self.window.title("Update Student")
        self.window.geometry("400x550")
        self.student = student
        self.callback = callback
        
        # labels and entry for details
        labels = ['Name:', 'Course 1 Mark (0-20):', 'Course 2 Mark (0-20):',
                 'Course 3 Mark (0-20):', 'Exam Mark (0-100):']
        self.entries = {}
        
        tk.Label(self.window, text=f"Student Code: {student.code}").pack(pady=5)
        
        for i, label in enumerate(labels):
            tk.Label(self.window, text=label).pack(pady=5)
            entry = tk.Entry(self.window)
            # fill fields with current data
            if label == 'Name:':
                entry.insert(0, student.name)
            elif label.startswith('Course'):
                entry.insert(0, str(student.course_marks[i-1]))
            else:
                entry.insert(0, str(student.exam_mark))
            entry.pack(pady=5)
            self.entries[label] = entry
        
        tk.Button(self.window, text="Update Student", command=self.update_student).pack(pady=10)
    
    def update_student(self):
        # check all the inputs and then update record or display error
        try:
            name = self.entries['Name:'].get()
            if not name:
                raise ValueError("Name cannot be empty")
            
            course_marks = [
                int(self.entries['Course 1 Mark (0-20):'].get()),
                int(self.entries['Course 2 Mark (0-20):'].get()),
                int(self.entries['Course 3 Mark (0-20):'].get())
            ]
            if not all(0 <= mark <= 20 for mark in course_marks):
                raise ValueError("Course marks must be between 0 and 20")
            
            exam = int(self.entries['Exam Mark (0-100):'].get())
            if not 0 <= exam <= 100:
                raise ValueError("Exam mark must be between 0 and 100")
            
            self.student.name = name
            self.student.course_marks = course_marks
            self.student.exam_mark = exam
            
            self.callback()  
            self.window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class StudentManagementGUI:
    def __init__(self, root):
        # create main window and load students
        self.root = root
        self.root.title("Student Records Management System")
        self.root.geometry("850x500")
        self.filename = "/Users/shahabmughal/Documents/Level 5 Sem 1/Advance Programming/Assessment 1/studentMarks.txt"
        self.students = []
        self.create_frames()
        self.load_students()
    
    def create_frames(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        # button to view all records
        ttk.Button(top_frame, text="View All Records", 
                  command=self.view_all_records).pack(side='left', padx=5)
        
        # dropdown to select single student
        ttk.Label(top_frame, text="Select Student:").pack(side='left', padx=5)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(top_frame, textvariable=self.student_var)
        self.student_dropdown.pack(side='left', padx=5)
        self.student_dropdown.bind('<<ComboboxSelected>>', self.show_selected_student)
        
        # button to view highest and lowest
        ttk.Button(top_frame, text="Show Highest Score", 
                  command=self.show_highest_score).pack(side='left', padx=5)
        ttk.Button(top_frame, text="Show Lowest Score", 
                  command=self.show_lowest_score).pack(side='left', padx=5)
        
        # add new buttons
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(bottom_frame, text="Add Student", 
                  command=self.show_add_student).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Update Selected", 
                  command=self.show_update_student).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Delete Selected", 
                  command=self.delete_selected).pack(side='left', padx=5)
        
        # sort optionss
        ttk.Label(bottom_frame, text="Sort by:").pack(side='left', padx=5)
        sort_options = ['Name', 'Total Score']
        self.sort_var = tk.StringVar(value=sort_options[0])
        sort_menu = ttk.OptionMenu(bottom_frame, self.sort_var, sort_options[0], 
                                 *sort_options, command=self.sort_students)
        sort_menu.pack(side='left', padx=5)
        
        # select order
        self.order_var = tk.StringVar(value="Ascending")
        ttk.Radiobutton(bottom_frame, text="Ascending", variable=self.order_var, 
                       value="Ascending", command=self.sort_students).pack(side='left', padx=5)
        ttk.Radiobutton(bottom_frame, text="Descending", variable=self.order_var, 
                       value="Descending", command=self.sort_students).pack(side='left', padx=5)
        
        # text area
        self.display_text = tk.Text(self.root, height=25, width=70, font=('Courier', 13))
        self.display_text.pack(padx=10, pady=5)
        
        self.stats_label = ttk.Label(self.root, text="")
        self.stats_label.pack(pady=5)
    
    def load_students(self):
        # take data from file
        try:
            with open(self.filename, 'r') as file:
                num_students = int(file.readline().strip())
                for _ in range(num_students):
                    line = file.readline().strip()
                    code, name, *marks = line.split(',')
                    self.students.append(Student(code, name, *marks))
            self.update_dropdown()
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {self.filename} not found!")
    
    def save_students(self):
        # save records to file
        with open(self.filename, 'w') as file:
            file.write(f"{len(self.students)}\n")
            for student in self.students:
                file.write(f"{student.code},{student.name},{','.join(map(str, student.course_marks))},{student.exam_mark}\n")
    
    def update_dropdown(self):
        # update dropdown
        student_names = [f"{student.name}" for student in self.students]
        self.student_dropdown['values'] = student_names
        if student_names:
            self.student_dropdown.set(student_names[0])
    
    def clear_display(self):
        self.display_text.delete(1.0, tk.END)
        self.stats_label.config(text="")
    
    def view_all_records(self):
        # display records of all students
        self.clear_display()
        for student in self.students:
            self.display_text.insert(tk.END, student.get_display_text() + "\n\n")
        
        if self.students:
            avg_percentage = sum(s.get_overall_percentage() for s in self.students) / len(self.students)
            stats = f"Number of students: {len(self.students)} | Average percentage: {avg_percentage:.2f}%"
            self.stats_label.config(text=stats)
    
    def show_selected_student(self, event=None):
        # display record for single student
        self.clear_display()
        selection = self.student_var.get()
        if selection:
            student = next((s for s in self.students if s.name == selection), None)
        if student:
            self.display_text.insert(tk.END, student.get_display_text())
    
    def show_highest_score(self):
        # display record of student with highest score
        if not self.students:
            messagebox.showwarning("Warning", "No students found!")
            return
        
        self.clear_display()
        highest_student = max(self.students, key=lambda s: s.get_overall_percentage())
        self.display_text.insert(tk.END, "Student with highest score:\n\n")
        self.display_text.insert(tk.END, highest_student.get_display_text())
    
    def show_lowest_score(self):
        # display record of student with lowest score
        if not self.students:
            messagebox.showwarning("Warning", "No students found!")
            return
        
        self.clear_display()
        lowest_student = min(self.students, key=lambda s: s.get_overall_percentage())
        self.display_text.insert(tk.END, "Student with lowest score:\n\n")
        self.display_text.insert(tk.END, lowest_student.get_display_text())
    
    def show_add_student(self):
        AddStudentWindow(self.root, self.add_student)
    
    def add_student(self, student):
        # add student
        self.students.append(student)
        self.save_students()
        self.update_dropdown()
        self.view_all_records()
    
    def show_update_student(self):
        # open update window for student
        selection = self.student_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to update")
            return
        
        student = next((s for s in self.students if s.name == selection), None)
        
        if student:
            UpdateStudentWindow(self.root, student, self.refresh_and_save)
    
    def refresh_and_save(self):
        self.save_students()
        self.update_dropdown()
        self.view_all_records()
    
    def delete_selected(self):
        # delete student
        selection = self.student_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            self.students = [s for s in self.students if s.name != selection]
            self.save_students()
            self.update_dropdown()
            self.view_all_records()
    
    def sort_students(self, *args):
        # sort student
        if self.sort_var.get() == 'Name':
            self.students.sort(key=lambda s: s.name,
                             reverse=self.order_var.get() == "Descending")
        else:  
            self.students.sort(key=lambda s: s.get_overall_percentage(),
                             reverse=self.order_var.get() == "Descending")
        self.view_all_records()

def main():
    # main function to run code
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
