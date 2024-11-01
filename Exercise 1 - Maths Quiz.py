import tkinter as tk
from tkinter import messagebox, ttk
import random

class WelcomeScreen:
    def __init__(self, root, callback):
        self.root, self.symbols = root, []
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # setting up main frame and layout
        frame = ttk.Frame(root, padding="20")
        frame.grid(row=0, column=0, sticky='nsew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        center = ttk.Frame(frame)
        center.grid(row=0, column=0)
        
        # create canvas for math symbols
        self.canvas = tk.Canvas(center, width=400, height=300, bg='white', highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=(0, 20))
        
        # creating or generating random symbols with random position
        for _ in range(15):
            x, y = random.randint(20, 380), random.randint(20, 280)
            text_id = self.canvas.create_text(x, y, 
                text=random.choice(['+', '-', 'x', '÷', '=']),
                font=('Arial', random.randint(20, 36), 'bold'),
                fill=random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']))
            self.symbols.append({'id': text_id, 'dx': random.uniform(-2, 2), 'dy': random.uniform(-2, 2)})
        
        # text and start button
        ttk.Label(center, text="Welcome to Math Quiz!", font=('Arial', 24, 'bold')).grid(row=1, pady=(0, 20))
        ttk.Label(center, text="Test your arithmetic skills!", font=('Arial', 14)).grid(row=2, pady=(0, 30))
        ttk.Button(center, text="Start Quiz", command=callback, width=20).grid(row=3, pady=(0, 20))
        
        self.animate()  

    def animate(self):
        # moving the symbols in canvas
        for symbol in self.symbols:
            pos = self.canvas.coords(symbol['id'])
            if pos[0] < 20 or pos[0] > 380: symbol['dx'] *= -1
            if pos[1] < 20 or pos[1] > 280: symbol['dy'] *= -1
            self.canvas.move(symbol['id'], symbol['dx'], symbol['dy'])
        self.root.after(50, self.animate) 

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        root.title("Arithmetic Quiz")
        root.geometry("440x500")
        root.resizable(False, False)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # creating variables and setting them to zero
        self.vars = {
            'question': tk.StringVar(),
            'answer': tk.StringVar(),
            'score': tk.StringVar(),
            'progress': tk.StringVar()
        }
        self.score = self.current_question = self.attempts = self.current_answer = 0
        self.difficulty = None
        self.show_welcome_screen()

    def setup_main_frame(self):
        # main frame for questions and set layout 
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.center_frame = ttk.Frame(self.main_frame)
        self.center_frame.grid(row=0, column=0)
        
        # setting labels
        for i, (var, text) in enumerate([('progress', ''), ('score', ''), ('question', '')]):
            setattr(self, f"{var}_label", ttk.Label(
                self.center_frame, textvariable=self.vars[var],
                font=('Arial', 12 if i < 2 else 16)
            ).grid(row=i, column=0, pady=5 if i < 2 else 20))
        
        # add entry field for answer and connecting button to the enter key
        self.answer_entry = ttk.Entry(
            self.center_frame, textvariable=self.vars['answer'],
            font=('Arial', 14), justify='center', width=15
        )
        self.answer_entry.grid(row=3, pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        ttk.Button(self.center_frame, text="Submit", command=self.check_answer, 
                  width=20).grid(row=4, pady=10)

    def show_welcome_screen(self):
        self.welcome_screen = WelcomeScreen(self.root, self.start_main_quiz)

    def start_main_quiz(self):
        self.welcome_screen.canvas.master.master.destroy()
        self.setup_main_frame()
        self.display_menu()

    def display_menu(self):
        # menu to choose level
        menu_frame = ttk.Frame(self.main_frame)
        menu_frame.grid(row=0, column=0)
        
        ttk.Label(menu_frame, text="ARITHMETIC QUIZ", font=('Arial', 16, 'bold'),
                 padding=10).pack(pady=(0, 20))
        ttk.Label(menu_frame, text="DIFFICULTY LEVEL", font=('Arial', 14),
                 padding=20).pack(pady=(0, 10))
        
        for text, value in [("1. Easy", "easy"),
                            ("2. Moderate", "moderate"), 
                            ("3. Advanced", "advanced")]:
            ttk.Button(menu_frame, text=text, command=lambda v=value: self.start_quiz(v),
                      width=20).pack(pady=5)
        self.menu_frame = menu_frame

    def start_quiz(self, difficulty):
        # initializing the quiz 
        self.difficulty = difficulty
        self.menu_frame.destroy()
        for widget in [self.vars['progress'], self.vars['score'], self.vars['question'],
                      self.answer_entry]:
            widget.grid() if hasattr(widget, 'grid') else widget.set('')
        self.display_problem()

    def display_problem(self):
        # creating a question of the dificulty level chosen
        self.vars['progress'].set(f"Question {self.current_question + 1} of 10")
        self.vars['score'].set(f"Current Score: {self.score}")
        
        num1 = random.randint(1, 9 if self.difficulty == "easy" else 
                            99 if self.difficulty == "moderate" else 9999)
        num2 = random.randint(1, 9 if self.difficulty == "easy" else 
                            99 if self.difficulty == "moderate" else 9999)
        op = random.choice(['+', '-'])
        self.current_answer = num1 + num2 if op == '+' else num1 - num2
        
        self.vars['question'].set(f"{num1} {op} {num2} = ")
        self.vars['answer'].set("")
        self.answer_entry.focus()

    def check_answer(self):
        # checking answer and adding score
        try:
            if int(self.vars['answer'].get()) == self.current_answer:
                self.score += 10 if self.attempts == 0 else 5
                self.current_question += 1
                self.attempts = 0
                self.display_problem() if self.current_question < 10 else self.display_results()
            else:
                self.attempts += 1
                if self.attempts < 2:
                    messagebox.showinfo("Incorrect", "Try again!")
                    self.vars['answer'].set("")
                else:
                    messagebox.showinfo("Incorrect", f"The correct answer was {self.current_answer}")
                    self.current_question += 1
                    self.attempts = 0
                    self.display_problem() if self.current_question < 10 else self.display_results()
        except ValueError:
            messagebox.showinfo("Error", "Please enter a valid number")

    def display_results(self):
        # display score and grade
        rank = 'A+' if self.score >= 90 else 'A' if self.score >= 80 else 'B' if self.score >= 70 else 'C' if self.score >= 60 else 'D'
        
        if messagebox.askyesno("Results", f"Quiz completed!\nYour score: {self.score}/100\nRank: {rank}\n\nWould you like to play again?"):
            # reset variable
            self.score = self.current_question = self.attempts = 0
            self.difficulty = None

            for widget in [self.vars['progress'], self.vars['score'], self.vars['question'],
                         self.answer_entry]:
                widget.grid_remove() if hasattr(widget, 'grid_remove') else None
            self.display_menu()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()
