import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class Note:
    def __init__(self, title, content, group, date):
        self.title = title
        self.content = content
        self.group = group
        self.date = date

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Книга заметок")

        self.notes = []
        self.current_note = None

        # Создание и настройка элементов интерфейса
        self.title_label = ttk.Label(root, text="Заголовок:")
        self.title_entry = ttk.Entry(root, width=40)
        self.content_label = ttk.Label(root, text="Содержание:")
        self.content_text = tk.Text(root, wrap="word", width=40, height=10)
        self.group_label = ttk.Label(root, text="Группа:")
        self.group_entry = ttk.Entry(root, width=40)
        self.date_label = ttk.Label(root, text="Дата:")
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.date_entry = ttk.Entry(root, textvariable=self.date_var, state="readonly")

        self.note_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.note_listbox.bind("<ButtonRelease-1>", self.load_selected_note)

        self.group_options = ["Все"]
        self.group_var = tk.StringVar()
        self.group_var.set("Все")
        self.group_combobox = ttk.Combobox(root, textvariable=self.group_var, values=self.group_options)
        self.group_combobox.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        self.group_combobox.bind("<<ComboboxSelected>>", self.filter_notes_by_group)

        self.sort_button = ttk.Button(root, text="Сортировать по дате", command=self.sort_notes_by_date)
        self.sort_button.grid(row=5, column=3, padx=5, pady=5, sticky="e")

        self.create_button = ttk.Button(root, text="Создать", command=self.create_note)
        self.edit_button = ttk.Button(root, text="Редактировать", command=self.edit_note)
        self.delete_button = ttk.Button(root, text="Удалить", command=self.delete_note)

        # Размещение элементов на форме
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.content_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.content_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.group_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.group_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.note_listbox.grid(row=0, column=3, rowspan=4, padx=5, pady=5, sticky="ns")
        self.create_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.edit_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.delete_button.grid(row=4, column=2, padx=5, pady=5, sticky="w")

    def create_note(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        group = self.group_entry.get()
        date = self.date_var.get()

        if title and content:
            new_note = Note(title, content, group, date)
            self.notes.append(new_note)
            self.update_note_listbox()
            self.clear_input_fields()
        else:
            messagebox.showwarning("Внимание", "Заголовок и содержание не могут быть пустыми.")

    def edit_note(self):
        if self.current_note:
            title = self.title_entry.get()
            content = self.content_text.get("1.0", tk.END).strip()
            group = self.group_entry.get()
            date = self.date_var.get()

            self.current_note.title = title
            self.current_note.content = content
            self.current_note.group = group
            self.current_note.date = date

            self.update_note_listbox()
            self.clear_input_fields()

    def delete_note(self):
        if self.current_note:
            self.notes.remove(self.current_note)
            self.update_note_listbox()
            self.clear_input_fields()

    def load_selected_note(self, event):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.current_note = self.notes[index]

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, self.current_note.title)

            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", self.current_note.content)

            self.group_entry.delete(0, tk.END)
            self.group_entry.insert(0, self.current_note.group)

            self.date_var.set(self.current_note.date)

    def update_note_listbox(self, notes=None):
        if notes is not None:
            notes.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
            self.notes = notes

        self.note_listbox.delete(0, tk.END)
        for note in self.notes:
            if self.group_var.get() == "Все" or note.group == self.group_var.get():
                self.note_listbox.insert(tk.END, note.title)

    def clear_input_fields(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.group_entry.delete(0, tk.END)
        self.date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def filter_notes_by_group(self, event):
        selected_group = self.group_var.get()
        if selected_group == "Все":
            self.update_note_listbox()
        else:
            filtered_notes = [note for note in self.notes if note.group == selected_group]
            self.update_note_listbox(filtered_notes)

    def sort_notes_by_date(self):
        self.notes.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
        self.update_note_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
