# ui.py
import tkinter as tk
from tkinter import messagebox
from data_handler import DataHandler
from expense_manager import ExpenseManager
from trip_planner import TripPlanner


class PennyWiseUI:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("PennyWise Financial Suite PRO")
        self.win.geometry("900x600")

        # Professional Color Palette
        self.bg_dark = "#121212"
        self.bg_panel = "#1e1e1e"
        self.fg_text = "#ffffff"
        self.accent = "#bb86fc"  # Modern purple accent
        self.danger = "#cf6679"

        self.win.configure(bg=self.bg_dark)

        # Initialize Backend Systems
        self.dh = DataHandler()
        self.expense_manager = ExpenseManager(self.dh)
        self.trip_planner = TripPlanner(self.dh)

        self.setup_layout()

        # The critical line that keeps the app open and running!
        self.win.mainloop()

    def setup_layout(self):
        # Sidebar Navigation
        self.sidebar = tk.Frame(self.win, bg=self.bg_panel, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        title = tk.Label(self.sidebar, text="PennyWise\nPRO", font=(
            "Helvetica", 18, "bold"), fg=self.accent, bg=self.bg_panel)
        title.pack(pady=30)

        tk.Button(self.sidebar, text="Dashboard", bg=self.bg_dark, fg=self.fg_text, relief="flat",
                  command=lambda: self.show_frame("dashboard")).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(self.sidebar, text="Daily Expenses", bg=self.bg_dark, fg=self.fg_text, relief="flat",
                  command=lambda: self.show_frame("expenses")).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(self.sidebar, text="Trip Planner", bg=self.bg_dark, fg=self.fg_text,
                  relief="flat", command=lambda: self.show_frame("trip")).pack(fill=tk.X, pady=5, padx=10)

        # Main Content Area
        self.main_area = tk.Frame(self.win, bg=self.bg_dark)
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dictionary to hold our screens
        self.frames = {}

        # Build the screens
        self.frames["dashboard"] = self.build_dashboard_frame()
        self.frames["expenses"] = self.build_expense_frame()
        self.frames["trip"] = self.build_trip_frame()

        # Show Dashboard by default
        self.show_frame("dashboard")

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # If opening dashboard, refresh the chart
        if frame_name == "dashboard":
            self.draw_chart()

        # Show the requested frame
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)

    # ---------- DASHBOARD (Analytics) ----------
    def build_dashboard_frame(self):
        frame = tk.Frame(self.main_area, bg=self.bg_dark)
        tk.Label(frame, text="Financial Analytics", font=(
            "Helvetica", 20, "bold"), fg=self.fg_text, bg=self.bg_dark).pack(pady=20)

        self.stats_lbl = tk.Label(frame, text="", font=(
            "Helvetica", 14), fg=self.accent, bg=self.bg_dark)
        self.stats_lbl.pack(pady=10)

        # Canvas for custom bar chart
        self.chart_canvas = tk.Canvas(
            frame, width=500, height=300, bg=self.bg_panel, highlightthickness=0)
        self.chart_canvas.pack(pady=20)

        return frame

    def draw_chart(self):
        self.chart_canvas.delete("all")
        data = self.expense_manager.get_expenses_by_category()
        total_exp = self.expense_manager.get_total()
        total_trip = self.trip_planner.calculate_total()

        self.stats_lbl.config(
            text=f"Total Expenses: ${total_exp:.2f}  |  Upcoming Trip Cost: ${total_trip:.2f}")

        if not data:
            self.chart_canvas.create_text(
                250, 150, text="No expense data to visualize.", fill=self.fg_text, font=("Arial", 12))
            return

        # Scratch-built Bar Chart Logic
        categories = list(data.keys())
        values = list(data.values())
        max_val = max(values) if values else 1

        bar_width = 40
        spacing = 60
        start_x = 50
        bottom_y = 250

        # Draw Axes
        self.chart_canvas.create_line(
            40, 20, 40, bottom_y, fill="white", width=2)  # Y Axis
        self.chart_canvas.create_line(
            40, bottom_y, 480, bottom_y, fill="white", width=2)  # X Axis

        for i in range(len(categories)):
            cat = categories[i]
            val = values[i]

            # Calculate bar height relative to max value
            bar_height = (val / max_val) * 200

            x0 = start_x + (i * spacing)
            y0 = bottom_y - bar_height
            x1 = x0 + bar_width
            y1 = bottom_y

            # Draw Bar
            self.chart_canvas.create_rectangle(
                x0, y0, x1, y1, fill=self.accent)
            # Draw Category Label
            self.chart_canvas.create_text(
                x0 + 20, bottom_y + 15, text=cat, fill=self.fg_text, font=("Arial", 9))
            # Draw Value Label
            self.chart_canvas.create_text(
                x0 + 20, y0 - 10, text=f"${val:.0f}", fill=self.fg_text, font=("Arial", 9))

    # ---------- EXPENSE TRACKER ----------
    def build_expense_frame(self):
        frame = tk.Frame(self.main_area, bg=self.bg_dark)
        tk.Label(frame, text="Manage Expenses", font=("Helvetica", 20,
                 "bold"), fg=self.fg_text, bg=self.bg_dark).pack(pady=20)

        # Input Area
        input_frame = tk.Frame(frame, bg=self.bg_dark)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Name:", bg=self.bg_dark,
                 fg=self.fg_text).grid(row=0, column=0, padx=5)
        name_entry = tk.Entry(input_frame, bg=self.bg_panel,
                              fg=self.fg_text, insertbackground="white")
        name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Amount:", bg=self.bg_dark,
                 fg=self.fg_text).grid(row=0, column=2, padx=5)
        amount_entry = tk.Entry(input_frame, bg=self.bg_panel,
                                fg=self.fg_text, insertbackground="white", width=10)
        amount_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Category:", bg=self.bg_dark,
                 fg=self.fg_text).grid(row=0, column=4, padx=5)
        # Category Dropdown
        cat_var = tk.StringVar(value="Food")
        cat_dropdown = tk.OptionMenu(
            input_frame, cat_var, "Food", "Transport", "Bills", "Misc")
        cat_dropdown.config(
            bg=self.bg_panel, fg=self.fg_text, highlightthickness=0)
        cat_dropdown.grid(row=0, column=5, padx=5)

        listbox = tk.Listbox(frame, width=60, height=12, bg=self.bg_panel,
                             fg=self.fg_text, selectbackground=self.accent)
        listbox.pack(pady=20)

        def refresh():
            listbox.delete(0, tk.END)
            for exp in self.expense_manager.get_all_expenses():
                listbox.insert(
                    tk.END, f"[{exp['category']}] {exp['name']} - ${exp['amount']:.2f}")

        def add():
            n = name_entry.get()
            a = amount_entry.get()
            c = cat_var.get()
            if not n or not a:
                messagebox.showerror("Error", "Fill all fields")
                return
            try:
                self.expense_manager.add_expense(n, float(a), c)
                name_entry.delete(0, tk.END)
                amount_entry.delete(0, tk.END)
                refresh()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")

        def delete():
            sel = listbox.curselection()
            if sel:
                self.expense_manager.delete_expense(sel[0])
                refresh()

        btn_frame = tk.Frame(frame, bg=self.bg_dark)
        btn_frame.pack()
        tk.Button(btn_frame, text="Add Expense", command=add,
                  bg=self.accent, fg="black", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete Selected", command=delete,
                  bg=self.danger, fg="black", width=15).pack(side=tk.LEFT, padx=10)

        refresh()
        return frame

    # ---------- TRIP PLANNER ----------
    def build_trip_frame(self):
        frame = tk.Frame(self.main_area, bg=self.bg_dark)
        tk.Label(frame, text="Itinerary Estimator", font=(
            "Helvetica", 20, "bold"), fg=self.fg_text, bg=self.bg_dark).pack(pady=20)

        input_frame = tk.Frame(frame, bg=self.bg_dark)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Cost Category:", bg=self.bg_dark,
                 fg=self.fg_text).grid(row=0, column=0, padx=5)
        cat_entry = tk.Entry(input_frame, bg=self.bg_panel,
                             fg=self.fg_text, insertbackground="white")
        cat_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Amount ($):", bg=self.bg_dark,
                 fg=self.fg_text).grid(row=0, column=2, padx=5)
        amt_entry = tk.Entry(input_frame, bg=self.bg_panel,
                             fg=self.fg_text, insertbackground="white", width=10)
        amt_entry.grid(row=0, column=3, padx=5)

        listbox = tk.Listbox(frame, width=60, height=12, bg=self.bg_panel,
                             fg=self.fg_text, selectbackground=self.accent)
        listbox.pack(pady=20)

        tot_lbl = tk.Label(frame, text="Total: $0.00", font=(
            "Arial", 14), bg=self.bg_dark, fg=self.accent)
        tot_lbl.pack()

        def refresh():
            listbox.delete(0, tk.END)
            costs = self.trip_planner.get_all_costs()
            for c, a in costs.items():
                listbox.insert(tk.END, f"{c} - ${a:.2f}")
            tot_lbl.config(
                text=f"Total: ${self.trip_planner.calculate_total():.2f}")

        def add():
            c = cat_entry.get().strip()
            a = amt_entry.get()
            if not c or not a:
                return
            try:
                self.trip_planner.add_or_update_category(c, float(a))
                cat_entry.delete(0, tk.END)
                amt_entry.delete(0, tk.END)
                refresh()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")

        def delete():
            sel = listbox.curselection()
            if sel:
                item_text = listbox.get(sel[0])
                cat_name = item_text.split(" - $")[0]
                self.trip_planner.remove_category(cat_name)
                refresh()

        btn_frame = tk.Frame(frame, bg=self.bg_dark)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save/Update", command=add,
                  bg=self.accent, fg="black", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete Selected", command=delete,
                  bg=self.danger, fg="black", width=15).pack(side=tk.LEFT, padx=10)

        refresh()
        return frame
