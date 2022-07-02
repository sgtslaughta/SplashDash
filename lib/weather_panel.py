import tkinter as tk
from datetime import datetime, date
from PIL import ImageTk, Image
import os.path


class Weather_Lg:
    def __init__(self, app):
        self.w_panel = tk.Frame(app.main_panel, bg="black")
        self.w_panel.pack(fill=tk.BOTH, expand=1)
        self.icon_frame = tk.Frame(self.w_panel, bg="blue2")
        self.icon_frame.grid(row=0, column=0, padx=5, pady=5)
        img = Image.open(os.path('img/001lighticons-08.png'))
        new_img = img.resize((int(app.window.winfo_screenwidth() / 4.5), int(app.window.winfo_screenheight() / 3.5)))
        self.w_icon = ImageTk.PhotoImage(new_img)
        self.p_holder = tk.Label(self.icon_frame, image=self.w_icon)
        #width=int(app.app_w * .74), height=int(app.app_h * .90)
        self.p_holder.pack(fill=tk.BOTH, expand=1)
        self.data_frame = tk.Frame(self.w_panel)
        self.data_frame.grid(row=0, column=1)

        # Create the city section
        self.city_frame = tk.Frame(self.data_frame)
        self.city_frame.grid(row=0, column=1)
        self.city_label = tk.Label(self.city_frame, text="City: ", bg="grey")
        self.city_label.grid(row=0, column=0, sticky=tk.W)
        self.city_text = tk.Label(self.city_frame, text="Hanover", bg="yellow2")
        self.city_text.grid(row=0, column=1)

        # Create the time section
        self.time_frame = tk.Frame(self.data_frame)
        self.time_frame.grid(row=1, column=1)
        self.time_label = tk.Label(self.time_frame, text="Time/ETC: ")
        self.time_label.grid(row=0, column=0)
        self.time_now = datetime.now().strftime("%H:%M:%S")
        self.date_now = date.today().strftime("%d/%m/%Y")
        self.time_now_var = tk.StringVar()
        self.time_now_var.set(f"{self.time_now} {self.date_now}")
        self.time_val = tk.Label(self.time_frame, text=self.time_now_var.get())
        self.time_val.grid(row=0, column=1)

        # Create the real feel section
        self.real_feel_var = tk.StringVar()
        self.real_feel_var.set(str(app.data.real_feel) + "°F")
        self.real_feel_frame = tk.Frame(self.data_frame)
        self.real_feel_label = tk.Label(self.real_feel_frame, text="Real Feel: ")
        self.real_feel_data = tk.Label(self.real_feel_frame, text=self.real_feel_var.get())
        self.real_feel_frame.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.real_feel_label.grid(row=0, column=0, sticky=tk.W)
        self.real_feel_data.grid(row=0, column=1, sticky=tk.E)
        self.update_time()

    def update_time(self):
        self.time_now = datetime.now().strftime("%H:%M:%S")
        self.date_now = date.today().strftime("%d/%m/%Y")
        self.time_now_var.set(f"{self.time_now} {self.date_now}")
        self.time_val.configure(text=self.time_now_var.get())
        self.time_val.after(1000, self.update_time)

    def get_condition_img(self):
        pass