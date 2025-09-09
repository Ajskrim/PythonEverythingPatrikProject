def main():
    start = int(input("Enter the start of the range: "))
    end = int(input("Enter the end of the range: "))
    days = int(input("How many days? "))
    if days < 2:
        print("Count must be at least 2.")
        return
    step = (end - start) / (days - 1)
    values = [round(start + i * step) for i in range(days)]
    print("Result:")
    for val in values:
        found = False
        for x in range(5, val//2 + 1, 5):
            y = val - 2*x
            if abs(x - y) <= 10:
                print(f"{val} = 2*{x} + {y}")
                found = True
                break
        if not found:
            print(f"{val} cannot be represented as 2x + y with x < y, x divisible by 5.")


# --- GUI Implementation ---
import tkinter as tk
from tkinter import ttk, messagebox

class RangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dog Food Portion Range Calculator")

        # Center and resize window to 60% of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.6)
        height = int(screen_height * 0.6)
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.last_portion_starts = []
        self.last_portion_ends = []

        self.portion_start_grams_var = tk.StringVar()
        self.portion_end_grams_var = tk.StringVar()
        self.days_var = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self.root, text="Dog food portion at start (grams):").grid(row=0, column=0, padx=10, pady=10)
        self.portion_start_entry = ttk.Combobox(self.root, textvariable=self.portion_start_grams_var, values=self.last_portion_starts)
        self.portion_start_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Dog food portion at end (grams):").grid(row=1, column=0, padx=10, pady=10)
        self.portion_end_entry = ttk.Combobox(self.root, textvariable=self.portion_end_grams_var, values=self.last_portion_ends)
        self.portion_end_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Number of days in period:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.days_var).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Generate", command=self.generate).grid(row=3, column=0, columnspan=2, pady=10)

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
        self.table.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def update_dropdowns(self, portion_start, portion_end):
        if portion_start not in self.last_portion_starts:
            self.last_portion_starts.insert(0, portion_start)
            self.last_portion_starts = self.last_portion_starts[:5]
            self.portion_start_entry["values"] = self.last_portion_starts
        if portion_end not in self.last_portion_ends:
            self.last_portion_ends.insert(0, portion_end)
            self.last_portion_ends = self.last_portion_ends[:5]
            self.portion_end_entry["values"] = self.last_portion_ends

    def generate(self):
        try:
            portion_start_grams = int(self.portion_start_grams_var.get())
            portion_end_grams = int(self.portion_end_grams_var.get())
            days = int(self.days_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return
        if days < 2:
            messagebox.showerror("Input Error", "Number of days must be at least 2.")
            return
        self.update_dropdowns(str(portion_start_grams), str(portion_end_grams))
        step = (portion_end_grams - portion_start_grams) / (days - 1)
        values = [round(portion_start_grams + i * step) for i in range(days)]
        self.table.delete(*self.table.get_children())
        for idx, val in enumerate(values, 1):
            found = False
            for x in range(5, val//2 + 1, 5):
                y = val - 2*x
                if abs(x - y) <= 10:
                    # Dog food logic
                    if x > y:
                        morning = x
                        noon = y
                        evening = x
                    else:
                        morning = x
                        noon = x
                        evening = y
                    self.table.insert("", "end", values=(idx, val, morning, noon, evening))
                    found = True
                    break
            if not found:
                self.table.insert("", "end", values=(idx, val, "-", "-", "-"))


if __name__ == "__main__":
    root = tk.Tk()
    app = RangeApp(root)
    root.mainloop()
