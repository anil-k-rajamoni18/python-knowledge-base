import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class StudentForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Registration Form")
        self.root.geometry("600x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        self.students = []
        self._build_ui()

    def _build_ui(self):
        # ── Title ──────────────────────────────────────────────
        title_frame = tk.Frame(self.root, bg="#16213e", pady=18)
        title_frame.pack(fill="x")
        tk.Label(
            title_frame, text="🎓 Student Registration",
            font=("Georgia", 22, "bold"),
            fg="#e94560", bg="#16213e"
        ).pack()
        tk.Label(
            title_frame, text="Fill in the details below",
            font=("Helvetica", 10), fg="#a0a8c0", bg="#16213e"
        ).pack()

        # ── Form Card ──────────────────────────────────────────
        card = tk.Frame(self.root, bg="#16213e", padx=30, pady=20,
                        relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=24, pady=16)

        self.vars = {}
        fields = [
            ("Full Name",        "text",   None),
            ("Student ID",       "text",   None),
            ("Email Address",    "text",   None),
            ("Date of Birth",    "text",   "YYYY-MM-DD"),
            ("Phone Number",     "text",   None),
            ("Gender",           "combo",  ["Male", "Female", "Other", "Prefer not to say"]),
            ("Department",       "combo",  ["Computer Science", "Engineering",
                                            "Business", "Arts & Humanities",
                                            "Natural Sciences", "Law", "Medicine"]),
            ("Year of Study",    "combo",  ["1st Year", "2nd Year", "3rd Year",
                                            "4th Year", "Postgraduate"]),
            ("Address",          "text",   None),
        ]

        for label, ftype, options in fields:
            row = tk.Frame(card, bg="#16213e", pady=5)
            row.pack(fill="x")

            tk.Label(row, text=label, font=("Helvetica", 10, "bold"),
                     fg="#a0a8c0", bg="#16213e", anchor="w", width=16).pack(side="left")

            if ftype == "combo":
                var = tk.StringVar()
                widget = ttk.Combobox(row, textvariable=var, values=options,
                                      state="readonly", font=("Helvetica", 10), width=30)
                widget.pack(side="left", fill="x", expand=True)
            else:
                var = tk.StringVar()
                widget = tk.Entry(row, textvariable=var, font=("Helvetica", 10),
                                  bg="#0f3460", fg="#e0e0e0", insertbackground="white",
                                  relief="flat", bd=6, width=32)
                if options:  # placeholder hint
                    widget.insert(0, options)
                    widget.config(fg="#606880")
                    def _on_focus_in(e, w=widget, hint=options, v=var):
                        if w.get() == hint:
                            w.delete(0, "end")
                            w.config(fg="#e0e0e0")
                    def _on_focus_out(e, w=widget, hint=options):
                        if not w.get():
                            w.insert(0, hint)
                            w.config(fg="#606880")
                    widget.bind("<FocusIn>", _on_focus_in)
                    widget.bind("<FocusOut>", _on_focus_out)
                widget.pack(side="left", fill="x", expand=True)

            self.vars[label] = (var, ftype, options)

        # ── Separator ─────────────────────────────────────────
        sep = tk.Frame(card, bg="#e94560", height=1)
        sep.pack(fill="x", pady=12)

        # ── Buttons ───────────────────────────────────────────
        btn_frame = tk.Frame(card, bg="#16213e")
        btn_frame.pack(fill="x", pady=6)

        self._make_btn(btn_frame, "✔  Submit", "#e94560", self.submit).pack(side="left", padx=(0, 10))
        self._make_btn(btn_frame, "↺  Reset",  "#0f3460", self.reset).pack(side="left")
        self._make_btn(btn_frame, "📋 View All", "#1a6b3c", self.view_all).pack(side="right")

        # ── Status bar ────────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self.root, textvariable=self.status_var,
                          font=("Helvetica", 9), fg="#606880", bg="#1a1a2e", anchor="w")
        status.pack(fill="x", padx=28, pady=(0, 8))

    def _make_btn(self, parent, text, color, cmd):
        btn = tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg="white", font=("Helvetica", 10, "bold"),
            relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
            activebackground=color, activeforeground="white"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self._lighten(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def _lighten(self, hex_color):
        """Return a slightly lighter hex color for hover effect."""
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _get_value(self, label):
        var, ftype, options = self.vars[label]
        val = var.get().strip()
        # Ignore placeholder text
        if options and ftype == "text" and val == options:
            return ""
        return val

    def submit(self):
        data = {label: self._get_value(label) for label in self.vars}

        # Validation
        required = ["Full Name", "Student ID", "Email Address", "Gender",
                    "Department", "Year of Study"]
        missing = [f for f in required if not data[f]]
        if missing:
            messagebox.showwarning("Missing Fields",
                                   "Please fill in:\n• " + "\n• ".join(missing))
            return

        if "@" not in data["Email Address"]:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if data["Date of Birth"]:
            try:
                datetime.strptime(data["Date of Birth"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
                return

        self.students.append(data)
        messagebox.showinfo("Success",
                            f"✅ Student '{data['Full Name']}' registered successfully!\n"
                            f"Total records: {len(self.students)}")
        self.status_var.set(f"Last registered: {data['Full Name']}  •  Total: {len(self.students)}")
        self.reset()

    def reset(self):
        for label, (var, ftype, options) in self.vars.items():
            if ftype == "combo":
                var.set("")
            else:
                var.set("")
                # Re-insert placeholder
                for widget in self.root.winfo_children():
                    pass  # entries handle their own placeholder via FocusOut

    def view_all(self):
        if not self.students:
            messagebox.showinfo("No Records", "No students registered yet.")
            return

        win = tk.Toplevel(self.root)
        win.title("All Students")
        win.geometry("720x420")
        win.configure(bg="#1a1a2e")

        tk.Label(win, text="Registered Students", font=("Georgia", 16, "bold"),
                 fg="#e94560", bg="#1a1a2e").pack(pady=12)

        cols = ["Full Name", "Student ID", "Email Address", "Department", "Year of Study"]
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0f3460", foreground="#e0e0e0",
                         fieldbackground="#0f3460", rowheight=26, font=("Helvetica", 10))
        style.configure("Treeview.Heading", background="#16213e", foreground="#e94560",
                         font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[("selected", "#e94560")])

        tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        for s in self.students:
            tree.insert("", "end", values=[s.get(c, "") for c in cols])

        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(0, 16))
        scrollbar.pack(side="right", fill="y", pady=(0, 16), padx=(0, 16))


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentForm(root)
    root.mainloop()