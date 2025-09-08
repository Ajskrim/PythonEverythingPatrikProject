import tkinter as tk
from tkinter import ttk, messagebox

    # ...existing code...
class RangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Range Generator")

        # Center and resize window to 60% of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.6)
        height = int(screen_height * 0.6)
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.last_mins = []
        self.last_maxs = []

        self.min_var = tk.StringVar()
        self.max_var = tk.StringVar()
        self.count_start_var = tk.StringVar()
        self.count_end_var = tk.StringVar()

        tk.Label(self.root, text="Start of range:").grid(row=0, column=0, padx=10, pady=10)
        self.min_entry = ttk.Combobox(self.root, textvariable=self.min_var, values=self.last_mins)
        self.min_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="End of range:").grid(row=1, column=0, padx=10, pady=10)
        self.max_entry = ttk.Combobox(self.root, textvariable=self.max_var, values=self.last_maxs)
        self.max_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Count start:").grid(row=2, column=0, padx=10, pady=10)
        self.count_start_entry = tk.Entry(self.root, textvariable=self.count_start_var)
        self.count_start_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Count end:").grid(row=3, column=0, padx=10, pady=10)
        self.count_end_entry = tk.Entry(self.root, textvariable=self.count_end_var)
        self.count_end_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Generate", command=self.generate).grid(row=4, column=0, columnspan=2, pady=10)

        # Table for results
        self.table = ttk.Treeview(self.root, columns=("Count", "Value", "Morning", "Noon", "Evening"), show="headings", height=20)
        self.table.heading("Count", text="#")
        self.table.heading("Value", text="Value")
        self.table.heading("Morning", text="Morning Portion")
        self.table.heading("Noon", text="Noon Portion")
        self.table.heading("Evening", text="Evening Portion")
        self.table.column("Count", width=50, anchor="center")
        self.table.column("Value", width=100, anchor="center")
        self.table.column("Morning", width=150, anchor="center")
        self.table.column("Noon", width=150, anchor="center")
        self.table.column("Evening", width=150, anchor="center")
        self.table.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    # ...existing code...

    def update_dropdowns(self, min_val, max_val):
        if min_val not in self.last_mins:
            self.last_mins.insert(0, min_val)
            self.last_mins = self.last_mins[:5]
            self.min_entry["values"] = self.last_mins
        if max_val not in self.last_maxs:
            self.last_maxs.insert(0, max_val)
            self.last_maxs = self.last_maxs[:5]
            self.max_entry["values"] = self.last_maxs

    def generate(self):
        try:
            start = int(self.min_var.get())
            end = int(self.max_var.get())
            count_start = int(self.count_start_var.get())
            count_end = int(self.count_end_var.get())
            if count_start < 2 or count_end < count_start:
                raise ValueError
            counts = list(range(count_start, count_end + 1))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for count start and end (start >= 2, end >= start).")
            return
        self.update_dropdowns(str(start), str(end))
        self.table.delete(*self.table.get_children())
        row_idx = 1
        labels = list(range(count_start, count_end + 1))
        values = list(range(start, end + 1))
        # If label count and value count differ, spread values linearly
        if len(labels) != len(values):
            import numpy as np
            values = list(np.linspace(start, end, len(labels), dtype=int))
        for label, val in zip(labels, values):
            found = False
            for x in range(5, val//2 + 1, 5):
                y = val - 2*x
                if abs(x - y) <= 10:
                    if x > y:
                        morning = x
                        noon = y
                        evening = x
                    else:
                        morning = x
                        noon = x
                        evening = y
                    self.table.insert("", "end", values=(label, val, morning, noon, evening))
                    found = True
                    break
            if not found:
                self.table.insert("", "end", values=(label, val, "-", "-", "-"))
            row_idx += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = RangeApp(root)
    root.mainloop()
