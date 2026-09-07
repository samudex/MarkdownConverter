import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from markitdown import MarkItDown
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class ConvertirApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Convertir a Markdown")
        self.geometry("460x240")
        self.resizable(False, False)

        self.file_path = None

        tk.Label(self, text="Archivo de entrada:", font=("Segoe UI", 10)).pack(pady=(12, 0))

        self.drop_label = tk.Label(
            self,
            text="Arrastra un archivo aquí\no haz click en 'Seleccionar'",
            fg="gray", relief="groove", bd=2, padx=20, pady=20, width=50, height=3,
            bg="#f0f0f0"
        )
        self.drop_label.pack(padx=12)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_drop)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.select_btn = tk.Button(
            btn_frame, text="Seleccionar archivo", command=self.select_file,
            bg="#4a90d9", fg="white", padx=12, pady=4, cursor="hand2"
        )
        self.select_btn.pack(side="left", padx=4)

        self.convert_btn = tk.Button(
            btn_frame, text="Convertir", command=self.convert,
            bg="#27ae60", fg="white", padx=12, pady=4, cursor="hand2", state="disabled"
        )
        self.convert_btn.pack(side="left", padx=4)

        self.status_label = tk.Label(self, text="", font=("Segoe UI", 9))
        self.status_label.pack()

    def on_drop(self, event):
        raw = event.data.strip()
        path = self._parse_drop_data(raw)
        if path and os.path.isfile(path):
            self.set_file(path)

    def _parse_drop_data(self, data):
        import re
        braces = re.findall(r'\{([^}]+)\}', data)
        if braces:
            return braces[0]
        parts = data.split()
        for part in parts:
            if os.path.isfile(part):
                return part
        return data

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Seleccionar archivo a convertir",
            filetypes=[
                ("Todos los archivos soportados", "*.pdf *.docx *.pptx *.xlsx *.html *.csv *.json *.xml *.txt *.md"),
                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("PowerPoint", "*.pptx"),
                ("Excel", "*.xlsx"),
                ("HTML", "*.html"),
                ("Todos", "*.*"),
            ]
        )
        if path:
            self.set_file(path)

    def set_file(self, path):
        self.file_path = path
        name = os.path.basename(path)
        self.drop_label.config(text=name, fg="black", bg="#e8f5e9")
        self.convert_btn.config(state="normal")
        self.status_label.config(text="")

    def convert(self):
        if not self.file_path:
            return

        self.status_label.config(text="Convirtiendo...", fg="gray")
        self.update()

        try:
            m = MarkItDown()
            result = m.convert(self.file_path)

            base = os.path.splitext(os.path.basename(self.file_path))[0]
            output_name = f"{base}.md"
            output_path = os.path.join(PROJECT_DIR, output_name)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.markdown)

            self.status_label.config(text=f"Guardado: {output_name}", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")

if __name__ == "__main__":
    app = ConvertirApp()
    app.mainloop()
