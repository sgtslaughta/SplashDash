import tkinter as tk


class Menu:
    def __init__(self, app):
        self.app = app
        self.api_val = app.api_key_val.get()

        # Create the menu
        self.menu_bar = tk.Menu(self.app.window, tearoff=0, activebackground="grey53")
        self.app.window.config(menu=self.menu_bar)

        # => Create the individual drop-down menus with commands
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground="grey53")
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground="grey53")
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground="grey53")
        # Add commands for each
        self.edit_menu.add_command(label="Edit City/Location")
        self.edit_menu.add_command(label="Add API Key", command=lambda: [self.get_api()])
        self.edit_menu.add_command(label="Open Detailed Info...")
        self.file_menu.add_command(label="Quit", command=lambda: [app.kill_app()])
        self.about_menu.add_command(label="About...")

        # Add drop-downs to main menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        self.check_api()

    def check_api(self):
        if self.api_val == "":
            self.edit_menu.entryconfig("Edit City/Location", state="disabled")
        self.edit_menu.after(1000, self.check_api)

    def get_api(self):
        self.api_win = ApiEntry(self)


class ApiEntry:
    def __init__(self, tl):
        self.p_win = tk.Toplevel()
        self.p_win.lift()
        self.entry_frame = tk.Frame(self.p_win)
        self.entry_frame.grid(row=0)
        self.api_label = tk.Label(self.entry_frame, text="API Key: ")
        self.api_entry = tk.Entry(self.entry_frame, width=30)

        self.api_label.grid(row=0, column=0, padx=10, pady=10)
        self.api_entry.grid(row=0, column=1, padx=10, pady=10)

        self.but_p_frame = tk.Frame(self.p_win)
        self.but_p_frame.grid(row=1, columnspan=1, sticky=tk.E+tk.W)
        self.but_frame = tk.Frame(self.but_p_frame, bg="red")
        self.but_frame.pack(fill=tk.BOTH, expand=1)
        self.ok_button = tk.Button(self.but_frame, text="OK", state=tk.DISABLED)
        self.cancel_but = tk.Button(self.but_frame, text="Cancel", command=self.p_win.destroy)
        self.ok_button.grid(row=0, column=0, sticky=tk.W)
        self.cancel_but.grid(row=0, column=1, sticky=tk.E)


