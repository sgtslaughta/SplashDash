import os
import tkinter as tk
import tkinter.font as tkfont
import lib.weather_panel as wp
import lib.menu_bar as menu
import lib.get_data as data


class App:
    """Main app constructor"""
    def __init__(self):
        self.mode_bg = 'grey13'
        self.mode_fg = 'cyan2'
        self.window = tk.Tk()
        self.window.tk_setPalette(background=self.mode_bg, foreground=self.mode_fg)
        self.api_key = "1d67d07f578f4c48a4e92303222606"
        self.api_key_val = tk.StringVar()
        self.location = 21076
        self.location_var = tk.StringVar()
        self.wdata = data.WData(self)
        # print(self.data.data)
        self.window.title("SplashDash")
        self.cwd = os.getcwd()
        self.window.iconphoto(False, tk.PhotoImage(file=os.path.join(self.cwd, 'lib/img/weather.png')))
        self.font = tkfont.Font(family="Consolas", size=10, weight="normal")
        self.m_len = self.font.measure('0')
        self.m_height = tkfont.Font(font='Consolas').metrics('linespace')
        self.app_h = round(((self.window.winfo_screenheight() / self.m_height) / 3) * 1.1)
        self.app_w = round((self.app_h * 1.5))

        self.set_window_size()
        self.menu = menu.Menu(self)
        self.main_panel = tk.Frame(self.window, bg="green3")
        self.main_panel.pack(fill=tk.BOTH, expand=1)
        self.w_main = wp.ConstructWPanel(self)

    def kill_app(self):
        """Close the whole app"""
        self.window.destroy()

    def set_window_size(self):
        """Get the users screen size and set the app window size to roughly 1/3 h:w"""
        self.window.geometry(f"{int(self.window.winfo_screenwidth() / 3) + 10}x{int(self.window.winfo_screenheight() / 3)}")
        self.window.lift()
        # self.window.resizable(False, False)
