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
        self.count_var = tk.StringVar()

        tk.Label(self.root, text="Start of range:").grid(row=0, column=0, padx=10, pady=10)
        self.min_entry = ttk.Combobox(self.root, textvariable=self.min_var, values=self.last_mins)
        self.min_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="End of range:").grid(row=1, column=0, padx=10, pady=10)
        self.max_entry = ttk.Combobox(self.root, textvariable=self.max_var, values=self.last_maxs)
        self.max_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="How many values:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.count_var).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Generate", command=self.generate).grid(row=3, column=0, columnspan=2, pady=10)

        # Table for results
        self.table = ttk.Treeview(self.root, columns=("Value", "Morning", "Noon", "Evening"), show="headings", height=20)
        self.table.heading("Value", text="Value")
        self.table.heading("Morning", text="Morning Portion")
        self.table.heading("Noon", text="Noon Portion")
        self.table.heading("Evening", text="Evening Portion")
        self.table.column("Value", width=100, anchor="center")
        self.table.column("Morning", width=150, anchor="center")
        self.table.column("Noon", width=150, anchor="center")
        self.table.column("Evening", width=150, anchor="center")
        self.table.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

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
            count = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return
        if count < 2:
            messagebox.showerror("Input Error", "Count must be at least 2.")
            return
        self.update_dropdowns(str(start), str(end))
        step = (end - start) / (count - 1)
        values = [round(start + i * step) for i in range(count)]
        self.table.delete(*self.table.get_children())
        for val in values:
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
                    self.table.insert("", "end", values=(val, morning, noon, evening))
                    found = True
                    break
            if not found:
                self.table.insert("", "end", values=(val, "-", "-", "-"))


if __name__ == "__main__":
    root = tk.Tk()
    app = RangeApp(root)
    root.mainloop()
