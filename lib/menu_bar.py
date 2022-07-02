import tkinter as tk


class Menu:
    def __init__(self, app):
        # Create the menu
        self.menu_bar = tk.Menu(app.window, bg="red", activebackground="green3")
        app.window.config(menu=self.menu_bar)

        # Add the menu to the main window

        # Add the individual drop down menus
        self.file_menu = tk.Menu(self.menu_bar, bg="red", activebackground="green3")
        self.edit_menu = tk.Menu(self.menu_bar, bg="red", activebackground="green3")
        self.file_menu.add_cascade(label="File", menu=self.menu_bar)
        self.file_menu.add_command(label="Quit")
        self.edit_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="City/Location")



