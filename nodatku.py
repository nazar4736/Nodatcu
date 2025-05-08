import tkinter as tk
from tkinter import filedialog, font, colorchooser, simpledialog, messagebox

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Нодатки")

        self.night_mode = False

        # Панель шаблонів
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side="top", fill="x")

        tk.Button(self.toolbar, text="📝 Список справ", command=self.insert_todo).pack(side="left", padx=2, pady=2)
        tk.Button(self.toolbar, text="💡 Ідеї", command=self.insert_ideas).pack(side="left", padx=2, pady=2)
        tk.Button(self.toolbar, text="📖 Щоденник", command=self.insert_diary).pack(side="left", padx=2, pady=2)

        # Панель форматування
        self.format_bar = tk.Frame(root)
        self.format_bar.pack(side="top", fill="x")

        tk.Button(self.format_bar, text="B", command=self.toggle_bold, font=("Arial", 10, "bold")).pack(side="left", padx=2)
        tk.Button(self.format_bar, text="I", command=self.toggle_italic, font=("Arial", 10, "italic")).pack(side="left", padx=2)
        tk.Button(self.format_bar, text="U", command=self.toggle_underline, font=("Arial", 10, "underline")).pack(side="left", padx=2)

        # Основне текстове поле
        self.text = tk.Text(root, wrap="word", font=("Arial", 12), fg="black", bg="white")
        self.text.pack(expand=True, fill="both")

        self.text.tag_configure("bold", font=("Arial", 12, "bold"))
        self.text.tag_configure("italic", font=("Arial", 12, "italic"))
        self.text.tag_configure("underline", font=("Arial", 12, "underline"))

        # Меню
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новий", command=self.clear_text)
        file_menu.add_command(label="Відкрити...", command=self.load_note)
        file_menu.add_command(label="Зберегти як...", command=self.save_note)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=root.quit)

        format_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Формат", menu=format_menu)
        format_menu.add_command(label="Змінити шрифт", command=self.change_font)
        format_menu.add_command(label="Змінити фон", command=self.change_bg_color)
        format_menu.add_command(label="Жовтий фон", command=self.set_yellow_bg)
        format_menu.add_command(label="Нічний режим", command=self.toggle_night_mode)

    def clear_text(self):
        self.text.delete("1.0", tk.END)

    def save_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text.get("1.0", tk.END))
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def load_note(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.clear_text()
                    self.text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{e}")

    def change_font(self):
        font_name = simpledialog.askstring("Шрифт", "Введіть назву шрифту (наприклад, Arial):")
        font_size = simpledialog.askinteger("Розмір", "Введіть розмір шрифту:")
        if font_name and font_size:
            try:
                self.text.config(font=(font_name, font_size))
            except tk.TclError:
                messagebox.showerror("Помилка", "Неправильний шрифт або розмір!")

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Виберіть колір фону")[1]
        if color:
            self.text.config(bg=color)
            if self.is_dark_color(color):
                self.text.config(fg="white")
            else:
                self.text.config(fg="black")

    def set_yellow_bg(self):
        self.text.config(bg="yellow", fg="black")

    def toggle_night_mode(self):
        if not self.night_mode:
            self.text.config(bg="#2e2e2e", fg="white")
            self.night_mode = True
        else:
            self.text.config(bg="white", fg="black")
            self.night_mode = False

    def is_dark_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 128

    # Форматування виділеного тексту
    def toggle_bold(self):
        self.toggle_tag("bold")

    def toggle_italic(self):
        self.toggle_tag("italic")

    def toggle_underline(self):
        self.toggle_tag("underline")

    def toggle_tag(self, tag_name):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
            if tag_name in self.text.tag_names("sel.first"):
                self.text.tag_remove(tag_name, start, end)
            else:
                self.text.tag_add(tag_name, start, end)
        except tk.TclError:
            pass  # Нічого не виділено

    # Шаблони
    def insert_todo(self):
        self.text.insert(tk.END, "📝 Список справ:\n- [ ] Завдання 1\n- [ ] Завдання 2\n- [ ] Завдання 3\n")

    def insert_ideas(self):
        self.text.insert(tk.END, "💡 Ідеї:\n- Ідея №1\n- Ідея №2\n- Ідея №3\n")

    def insert_diary(self):
        self.text.insert(tk.END, "📖 Щоденник:\nДата: \nНастрій: \nПодії дня: \n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
