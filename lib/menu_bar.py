import tkinter as tk
from re import match


class Menu:
    def __init__(self, app):
        self.app = app

        # Create the menu
        self.menu_bar = tk.Menu(self.app.window, tearoff=0, activebackground="grey53")
        self.app.window.config(menu=self.menu_bar)

        # => Create the individual drop-down menus with commands
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground="grey53")
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground="grey53")
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0, activebackground="grey53")
        # Add commands for each
        self.edit_menu.add_command(label="Edit City/Location")
        self.edit_menu.entryconfig("Edit City/Location", state="disabled", command=lambda: [self.get_loc()])
        self.edit_menu.add_command(label="Add API Key", command=lambda: [self.get_api(app)])
        self.edit_menu.add_command(label="Open Detailed Info...")
        self.file_menu.add_command(label="Quit", command=lambda: [app.kill_app()])
        self.about_menu.add_command(label="About...")

        # Add drop-downs to main menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        self.check_api()

    # Function to enable location entry window only after API has been entered
    def check_api(self):
        if self.app.api_key_val.get() != "":
            self.edit_menu.entryconfig("Edit City/Location", state=tk.NORMAL)
        self.edit_menu.after(1000, self.check_api)

    # Create the API entry window
    def get_api(self, app):
        ApiEntry(self, app)

    # Create the location entry window
    def get_loc(self):
        LocWin(self)


class ApiEntry:
    def __init__(self, menu, app):

        # Set variables and create pop up window
        self.menu = menu
        self.app = app
        self.p_win = tk.Toplevel()
        self.p_win.title("Enter API Key")
        self.p_win.lift()

        # Create the main frame
        self.entry_frame = tk.Frame(self.p_win)
        self.entry_frame.grid(row=0)

        # Create the Label and Entry frames
        self.api_label = tk.Label(self.entry_frame, text="API Key: ")
        self.api_entry = tk.Entry(self.entry_frame, width=30)
        self.api_label.grid(row=0, column=0, padx=10, pady=10)
        self.api_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create the button frame and objects
        self.but_p_frame = tk.Frame(self.p_win)
        self.but_p_frame.grid(row=1, columnspan=1, sticky=tk.E+tk.W)
        self.but_frame = tk.Frame(self.but_p_frame, bg="red")
        self.but_frame.pack(fill=tk.BOTH, expand=1)
        self.ok_button = tk.Button(self.but_frame, text="OK", state=tk.DISABLED, command=lambda: [self.set_api()])
        self.cancel_but = tk.Button(self.but_frame, text="Cancel", command=self.p_win.destroy)
        self.ok_button.grid(row=0, column=0, sticky=tk.W)
        self.cancel_but.grid(row=0, column=1, sticky=tk.E)

        # Validate proper API format
        self.check_api()

    # Function to get API from entry and set value, close window
    def set_api(self):
        self.app.api_key_val.set(self.api_entry.get())
        self.p_win.destroy()

    # Function to check the API format against regex, enable OK button once correct
    def check_api(self):
        if match("^[a-zA-Z0-9]{30}", self.api_entry.get()):
            self.ok_button.config(state=tk.NORMAL)
        self.ok_button.after(500, self.check_api)


class LocWin:
    def __init__(self, menu):
        # Set variables and create pop up window
        self.menu = menu
        self.p_win = tk.Toplevel()
        self.p_win.title("Enter Location")
        self.p_win.lift()

        # Create main frame and button frame
        self.win_frame = tk.Frame(self.p_win)
        self.win_frame.grid(row=0, column=0)
        self.but_frame = tk.Frame(self.p_win)
        self.but_frame.grid(row=1, column=0)

        # Create the location label
        self.loc_label = tk.Label(self.win_frame, text="Location")
        self.loc_label.grid(row=0, column=0, padx=10, pady=10)

        # Create the entry form
        self.loc_entry = tk.Entry(self.win_frame)
        self.loc_entry.insert(0, "Enter ZIP code")
        self.loc_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create the buttons
        self.ok_button = tk.Button(self.but_frame, text="OK", state=tk.DISABLED, command=lambda: [self.set_loc()])
        self.cancel_but = tk.Button(self.but_frame, text="Cancel", command=self.p_win.destroy)
        self.ok_button.grid(row=0, column=0, sticky=tk.W)
        self.cancel_but.grid(row=0, column=1, sticky=tk.E)

        # Check entry agains regex to validate ZIP code format
        self.check_zip()

    # Check entry agains regex to validate ZIP code format, enable OK button if valid
    def check_zip(self):
        if match("^[0-9]{5}", self.loc_entry.get()):
            self.ok_button.config(state=tk.NORMAL)
        self.ok_button.after(500, self.check_zip)

    # Get the ZIP code from the entry form and set it to variable, close window
    def set_loc(self):
        self.menu.app.location_var.set(self.loc_entry.get())
        self.p_win.destroy()
