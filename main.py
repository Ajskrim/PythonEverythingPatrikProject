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
from tkcalendar import DateEntry

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

        # State variables
        self.last_portion_starts = []
        self.last_portion_ends = []
        self.portion_start_grams_var = tk.StringVar(self.root)
        self.portion_end_grams_var = tk.StringVar(self.root)
        self.start_date_var = tk.StringVar(self.root)
        self.end_date_var = tk.StringVar(self.root)

        # Build UI
        self._create_widgets()

    def _create_widgets(self):
        # Portion start
        tk.Label(self.root, text="Dog food portion at start (grams):").grid(row=0, column=0, padx=10, pady=10)
        self.portion_start_entry = ttk.Combobox(self.root, textvariable=self.portion_start_grams_var, values=self.last_portion_starts)
        self.portion_start_entry.grid(row=0, column=1, padx=10, pady=10)

        # Portion end
        tk.Label(self.root, text="Dog food portion at end (grams):").grid(row=1, column=0, padx=10, pady=10)
        self.portion_end_entry = ttk.Combobox(self.root, textvariable=self.portion_end_grams_var, values=self.last_portion_ends)
        self.portion_end_entry.grid(row=1, column=1, padx=10, pady=10)

        # Start date
        tk.Label(self.root, text="Start date (DD-MM-YYYY):").grid(row=2, column=0, padx=10, pady=10)
        self.start_date_entry = DateEntry(self.root, textvariable=self.start_date_var, date_pattern='dd-mm-yyyy')
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=10)

        # End date
        tk.Label(self.root, text="End date (DD-MM-YYYY):").grid(row=3, column=0, padx=10, pady=10)
        self.end_date_entry = DateEntry(self.root, textvariable=self.end_date_var, date_pattern='dd-mm-yyyy')
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=10)

        # Generate button
        tk.Button(self.root, text="Generate", command=self.generate).grid(row=4, column=0, columnspan=2, pady=10)

        # Results table
        self.table = ttk.Treeview(self.root, columns=("Date", "Value", "Morning", "Noon", "Evening"), show="headings", height=20)
        self.table.heading("Date", text="Date")
        self.table.heading("Value", text="Value")
        self.table.heading("Morning", text="Morning Portion")
        self.table.heading("Noon", text="Noon Portion")
        self.table.heading("Evening", text="Evening Portion")
        self.table.column("Date", width=100, anchor="center")
        self.table.column("Value", width=100, anchor="center")
        self.table.column("Morning", width=150, anchor="center")
        self.table.column("Noon", width=150, anchor="center")
        self.table.column("Evening", width=150, anchor="center")
        self.table.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(5, weight=1)
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
        import datetime
        try:
            portion_start_grams = int(self.portion_start_grams_var.get())
            portion_end_grams = int(self.portion_end_grams_var.get())
            start_date = datetime.datetime.strptime(self.start_date_var.get(), "%d-%m-%Y")
            end_date = datetime.datetime.strptime(self.end_date_var.get(), "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers and dates in DD-MM-YYYY format.")
            return
        if end_date <= start_date:
            messagebox.showerror("Input Error", "End date must be after start date.")
            return
        days = (end_date - start_date).days + 1
        if days < 2:
            messagebox.showerror("Input Error", "Date range must be at least 2 days.")
            return
        self.update_dropdowns(str(portion_start_grams), str(portion_end_grams))
        step = (portion_end_grams - portion_start_grams) / (days - 1)
        values = [round(portion_start_grams + i * step) for i in range(days)]
        self.table.delete(*self.table.get_children())
        date_list = [(start_date + datetime.timedelta(days=i)).strftime("%d-%m-%Y") for i in range(days)]
        for idx, val in enumerate(values):
            row_date = date_list[idx]
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
                    self.table.insert("", "end", values=(row_date, val, morning, noon, evening))
                    found = True
                    break
            if not found:
                self.table.insert("", "end", values=(row_date, val, "-", "-", "-"))


if __name__ == "__main__":
    root = tk.Tk()
    app = RangeApp(root)
    root.mainloop()
