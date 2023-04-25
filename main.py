import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring


class ChatBot:
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        self.knowledge_base_path = knowledge_base_path
        self.load_knowledge_base()
        self.build_vocab()

    def load_knowledge_base(self):
        try:
            with open(self.knowledge_base_path) as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            self.knowledge_base = {}

    def save_knowledge_base(self):
        with open(self.knowledge_base_path, "w") as f:
            json.dump(self.knowledge_base, f)

    def build_vocab(self):
        self.vocab = set()
        for key in self.knowledge_base:
            self.vocab.update(key.split())

    def find_best_match(self, question):
        question_words = set(question.lower().split())
        best_match = None
        best_score = 0
        for key in self.knowledge_base:
            key_words = set(key.lower().split())
            score = len(question_words.intersection(key_words)) / len(key_words)
            if score > best_score:
                best_match = key
                best_score = score
        return best_match, best_score

    def learn_from_user(self, question):
        answer = messagebox.askquestion(
            "Unknown Question",
            f"I don't know the answer to this question: {question}. "
            "Would you like to teach me?",
        )
        if answer == "yes":
            new_answer = askstring(
                "Teach Me",
                "What's the answer to this question?",
            )
            self.knowledge_base[question] = new_answer
            self.build_vocab()
            self.save_knowledge_base()

    def get_answer(self, question):
        if question in self.knowledge_base:
            return self.knowledge_base[question]
        else:
            best_match, best_score = self.find_best_match(question)
            if best_match is not None and best_score > 0.5:
                answer = self.knowledge_base[best_match]
                messagebox.showinfo(
                    "I'm not sure",
                    f"I'm not sure about {question}, but I think you might be asking about {best_match}.",
                )
                return answer
            else:
                self.learn_from_user(question)
                return "I'm sorry, I don't know the answer to that question."

class ChatBotGUI:
    def __init__(self):
        self.bot = ChatBot()
        self.root = tk.Tk()
        self.root.title("ChatBot")
        self.build_widgets()

    def build_widgets(self):
        self.output_text = tk.Text(self.root, state="disabled")
        self.output_text.pack(fill="both", expand=True)

        self.input_label = tk.Label(self.root, text="User:")
        self.input_label.pack(side="left")

        self.input_entry = tk.Entry(self.root)
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", self.submit_question)

        self.submit_button = tk.Button(self.root, text="Ask", command=self.submit_question)
        self.submit_button.pack(side="right")

    def submit_question(self, event=None):
        question = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        answer = self.bot.get_answer(question)
        self.display_message("User: " + question)
        self.display_message("ChatBot: " + answer)

    def display_message(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", message + "\n")
        self.output_text.configure(state="disabled")


if __name__ == "__main__":
    ChatBotGUI().root.mainloop()
