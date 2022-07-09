import tkinter as tk
from re import match
import webbrowser
from .common import get_web_image


class Menu:
    """Instantiate the menu and menu functions"""
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
        self.edit_menu.add_command(label="Add API Key", command=lambda: [self.get_api()])
        self.edit_menu.add_command(label="Open Detailed Info...")
        self.file_menu.add_command(label="Quit", command=lambda: [app.kill_app()])
        self.about_menu.add_command(label="About...", command=lambda: [self.open_about()])

        # Add drop-downs to main menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        self.after = None

        self.check_api_set()

    # Function to enable location entry window only after API has been entered
    def check_api_set(self):
        if self.app.api_key_val.get() != "":
            self.edit_menu.entryconfig("Edit City/Location", state=tk.NORMAL)
        self.after = self.edit_menu.after(1000, self.check_api_set)

    # Create the API entry window
    def get_api(self):
        ApiEntry(self, self.app)

    # Create the location entry window
    def get_loc(self):
        LocWin(self)

    # Open About
    def open_about(self):
        About(self)


class ApiEntry:
    """Create the API entry window"""
    def __init__(self, menu, app):

        # Set variables and create pop up window
        self.menu = menu
        self.app = app
        self.p_win = tk.Toplevel()
        self.p_win.title("Enter API Key")
        self.p_win.lift()
        self.after = None

        # Create the main frame
        self.entry_frame = tk.Frame(self.p_win)
        self.entry_frame.grid(row=0, column=0)

        # Create the Label and Entry frames
        self.api_label = tk.Label(self.entry_frame, text="API Key: ")
        self.api_entry = tk.Entry(self.entry_frame, width=30)
        self.api_label.grid(row=0, column=0, padx=10, pady=10)
        self.api_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create the button frame and objects
        w = self.p_win.winfo_screenwidth() / app.m_len
        self.b_frame = tk.Frame(self.p_win, bg='red')
        self.b_frame.grid(row=1, column=0, sticky='ew')
        self.ok_button = tk.Button(self.b_frame, text="OK", width=int(w / 16), state=tk.DISABLED, command=lambda: [self.set_api()])
        self.cancel_but = tk.Button(self.b_frame, text="Cancel", width=int(w / 16), command=self.p_win.destroy)
        self.ok_button.grid(row=0, column=0, sticky='ew')
        self.cancel_but.grid(row=0, column=1, sticky='ew')

        # Validate proper API format
        self.check_api()

    def set_api(self):
        """Function to get API from entry widget and set value to dash.api_key_val, close window"""
        self.app.api_key_val.set(self.api_entry.get())
        self.p_win.destroy()

    def check_api(self):
        """Function to check the API format against regex, enable OK button once correct"""
        if match("^[a-zA-Z0-9]{30}", self.api_entry.get()):
            self.ok_button.config(state=tk.NORMAL)
        self.after = self.ok_button.after(500, self.check_api)



class LocWin:
    """Create the location entry window"""
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

        # Check entry against regex to validate ZIP code format
        self.check_zip()

    def check_zip(self):
        """Check entry against regex to validate ZIP code format, enable OK button if valid"""
        if match("^[0-9]{5}", self.loc_entry.get()):
            self.ok_button.config(state=tk.NORMAL)
        self.ok_button.after(500, self.check_zip)

    def set_loc(self):
        """Get the ZIP code from the entry form and set it to variable, close window"""
        self.menu.app.location_var.set(self.loc_entry.get())
        self.p_win.destroy()


def callback(url="URL"):
    """Opens a url in default browser"""
    webbrowser.open_new_tab(url)


class About:
    """Create the about screen"""
    def __init__(self, menu):
        self.menu = menu

        # Create the About window
        self.p_win = tk.Toplevel()
        self.p_win.title("About")
        self.p_win.lift()

        # Create the credit frame
        self.credit_frame = tk.Frame(self.p_win)
        self.credit_frame.grid(row=0, column=0, padx=10, pady=10)

        self.credit_label = tk.Label(self.credit_frame, text="API calls made available by: ", font='Helvetica 12 italic')
        self.credit_label.grid(row=0, column=0, padx=5)
        # Get the image from the web // BROKE SOMEHOW
        self.img = get_web_image("https://cdn.weatherapi.com/v4/images/weatherapi_logo.png")
        self.w_api_img_label = tk.Label(self.credit_frame, image=self.img, cursor="hand2")
        self.w_api_img_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.w_api_img_label.bind("<Button-1>", lambda e: [callback("https://www.weatherapi.com/")])
        # Create the url link
        self.w_api_credit = tk.Label(self.credit_frame, text="https://www.weatherapi.com/", fg="blue", cursor="hand2")
        self.w_api_credit.grid(row=1, column=1, padx=5, pady=5)
        self.w_api_credit.bind("<Button-1>", lambda e: [callback("https://www.weatherapi.com/")])
