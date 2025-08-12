import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4fc")  # Light background

        # --- Title ---
        tk.Label(
            root,
            text="My To-Do List",
            font=("Helvetica", 18, "bold"),
            bg="#4f8cff",
            fg="white",
            pady=10
        ).pack(fill=tk.X)

        # --- Task Entry ---
        self.task_entry = tk.Entry(root, font=("Helvetica", 12), bg="#e6eeff", fg="#333")
        self.task_entry.pack(pady=10, padx=20, fill=tk.X)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg="#f0f4fc")
        btn_frame.pack(pady=5)

        btn_style = {
            "font": ("Helvetica", 11, "bold"),
            "bg": "#4f8cff",
            "fg": "white",
            "activebackground": "#357ae8",
            "activeforeground": "white",
            "bd": 0,
            "relief": tk.FLAT,
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="Add Task", width=12, command=self.add_task, **btn_style).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Mark Done", width=12, command=self.mark_done, **btn_style).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Task", width=12, command=self.delete_task, **btn_style).grid(row=0, column=2, padx=5)

        # --- Task List ---
        list_frame = tk.Frame(root, bg="#f0f4fc")
        list_frame.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 12),
            height=15,
            selectmode=tk.SINGLE,
            bg="#e6eeff",
            fg="#333",
            selectbackground="#4f8cff",
            selectforeground="white",
            bd=0,
            highlightthickness=0
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Load saved tasks
        self.tasks = []
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "done": False})
            self.update_listbox()
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def mark_done(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            del self.tasks[index]
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display = task["task"]
            if task["done"]:
                display += " ✓"
            self.task_listbox.insert(tk.END, display)

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
                self.update_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
