import tkinter as tk
from tkinter import messagebox
import random
import hangman_stages

WORDLIST_FILENAME = "words.txt"

# ---------------- Load Words ----------------
def loadWords():
    with open(WORDLIST_FILENAME, 'r') as file:
        line = file.readline()
    return line.split()

# ---------------- Game Logic ----------------
class HangmanGame:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Game Using Tk")
        master.geometry("700x600")
        master.configure(bg="#f0f4f7")

        # Load words
        self.wordlist = loadWords()
        self.word_to_guess = ""
        self.guessed_letters = []
        self.attempts = 6

        # GUI components
        self.create_widgets()
        self.new_game()

        # 🔹 Bind Enter key to the guess function
        self.master.bind("<Return>", lambda event: self.make_guess())

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.master, text="🎮 Hangman Game Using Tk", font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#333")
        self.title_label.pack()
        self.title_label = tk.Label(self.master, text="By Lokesh Mishra", font=("Helvetica", 18, "bold"), bg="#f0f4f7", fg="#333")
        self.title_label.pack(pady=10)

        # Hangman stage
        self.stage_label = tk.Label(self.master, text="", font=("Courier", 16), bg="#f0f4f7", justify="left")
        self.stage_label.pack(pady=10)

        # Word display
        self.word_label = tk.Label(self.master, text="", font=("Helvetica", 22, "bold"), bg="#f0f4f7")
        self.word_label.pack(pady=10)

        # Attempts left
        self.attempts_label = tk.Label(self.master, text="", font=("Helvetica", 16), bg="#f0f4f7", fg="#e63946")
        self.attempts_label.pack(pady=5)

        # Guessed letters
        self.guessed_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#f0f4f7")
        self.guessed_label.pack(pady=5)

        # Entry + Button frame
        entry_frame = tk.Frame(self.master, bg="#f0f4f7")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Enter a letter:", font=("Helvetica", 14), bg="#f0f4f7").pack(side=tk.LEFT, padx=5)
        self.guess_entry = tk.Entry(entry_frame, font=("Helvetica", 14), width=5)
        self.guess_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(entry_frame, text="Guess", font=("Helvetica", 14, "bold"), command=self.make_guess, bg="#457b9d", fg="white").pack(side=tk.LEFT, padx=5)

        # Message label
        self.message_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#f0f4f7", fg="#1d3557")
        self.message_label.pack(pady=3)

        # New Game Button
        tk.Button(self.master, text="🔄 New Game", font=("Helvetica", 14, "bold"), command=self.new_game, bg="#2a9d8f", fg="white").pack(pady=15)

    def new_game(self):
        self.word_to_guess = random.choice(self.wordlist).lower()
        self.guessed_letters = []
        self.attempts = 6
        self.update_display()
        self.message_label.config(text="New game started! Guess a letter 🎯")

    def display_word(self):
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess)

    def update_display(self):
        self.stage_label.config(text=hangman_stages.stages[self.attempts])
        self.word_label.config(text=self.display_word())
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
        self.guessed_label.config(text=f"Guessed: {' '.join(sorted(self.guessed_letters))}")

    def make_guess(self):
        guess = self.guess_entry.get().lower().strip()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="❌ Enter a single valid letter.")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="⚠️ You've already guessed that letter.")
            return

        self.guessed_letters.append(guess)

        if guess not in self.word_to_guess:
            self.attempts -= 1
            self.message_label.config(text=f"❌ Wrong guess! {self.attempts} attempts left.")
        else:
            self.message_label.config(text=f"✅ Correct! '{guess}' is in the word.")

        self.update_display()

        if "_" not in self.display_word():
            messagebox.showinfo("🎉 You Win!", f"Congratulations! The word was '{self.word_to_guess}'.")
            self.new_game()
        elif self.attempts == 0:
            messagebox.showerror("💀 Game Over", f"You ran out of attempts! The word was '{self.word_to_guess}'.")
            self.new_game()

# ---------------- Run Game ----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
