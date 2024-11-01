import tkinter as tk
from tkinter import messagebox
import random

class JokeTeller:
    def __init__(self, root):
        # set up window
        self.root = root
        self.root.title("Joke Teller")
        self.root.geometry("400x400")
        self.jokes = []
        
        # load jokes from file an split them 
        try:
            with open("/Users/shahabmughal/Documents/Level 5 Sem 1/Advance Programming/Assessment 1/randomJokes.txt", "r") as file:
                for line in file:
                    if '?' in line:
                        self.jokes.append(tuple(line.strip().split('?')))
        except FileNotFoundError:
            messagebox.showerror("Error", "Jokes file not found!")
            self.root.quit()
            return

        self.current_setup = None
        self.current_punchline = None

        self.create_widgets()  

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        # entry field for saying the phrase and press enter to reveal joke
        self.command_label = tk.Label(self.frame, text="Say 'Alexa tell me a joke':")
        self.command_label.pack(pady=5)
        
        self.command_entry = tk.Entry(self.frame)
        self.command_entry.pack(pady=5)
        self.command_entry.bind('<Return>', self.process_command)

        self.command_label = tk.Label(self.frame, text="and press 'Enter'.")
        self.command_label.pack(pady=5)

        # create frame for both parts of the joke
        self.setup_frame = tk.Frame(self.frame, relief="solid", borderwidth=1)
        self.setup_frame.pack(pady=5, padx=5, fill='x')
        
        self.punchline_frame = tk.Frame(self.frame, relief="solid", borderwidth=1)
        self.punchline_frame.pack(pady=5, padx=5, fill='x')

        # label to show joke
        self.setup_text = tk.Label(self.setup_frame, text="", wraplength=350, height=2,
                                   font=('Arial', 15), pady=5, padx=10)
        self.setup_text.pack(pady=5)
        
        self.punchline_text = tk.Label(self.punchline_frame, text="", wraplength=350, height=2,
                                       font=('Arial', 15), pady=5, padx=10)
        self.punchline_text.pack(pady=5)

        # button for revealing punchline
        self.reveal_button = tk.Button(self.frame, text="Reveal Punchline", command=self.show_punchline)
        self.reveal_button.pack(pady=5)
        self.reveal_button.config(state='disabled')

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

    def process_command(self, event=None):
        # check command
        command = self.command_entry.get().lower().strip()
        if command == "alexa tell me a joke":
            self.tell_joke()
        self.command_entry.delete(0, tk.END)

    def tell_joke(self):
        # select random joke
        if self.jokes:
            self.current_setup, self.current_punchline = random.choice(self.jokes)
            self.setup_text.config(text=self.current_setup + "?")
            self.punchline_text.config(text="")
            self.reveal_button.config(state='normal')  
        
    def show_punchline(self):
        # show punchline
        if self.current_punchline:
            self.punchline_text.config(text=self.current_punchline)
            self.reveal_button.config(state='disabled')

def main():
    # main function to run code
    root = tk.Tk()
    app = JokeTeller(root)
    root.mainloop()

if __name__ == "__main__":
    main()
