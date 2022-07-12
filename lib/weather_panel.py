import tkinter as tk
from datetime import datetime, date
from PIL import ImageTk, Image, ImageDraw, ImageFont
from . import common
import matplotlib
matplotlib.use('TkAgg')
from requests import get as r_get
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,

)


class MainPanel:
    """Main weather panel class"""
    def __init__(self, app):
        self.app = app
        self.w_panel = tk.Frame(app.main_panel)
        self.w_panel.pack(fill=tk.BOTH, expand=1)
        self.bg = tk.Canvas(self.w_panel, bg='black', height=app.window.winfo_screenheight(), width=app.window.winfo_screenwidth())
        self.bg.place(x=-3, y=-2)
        self.bg_frame_left = None
        self.bg_frame_right = None
        self.bg_day_night = None
        self.bg_ph = None
        self.bg_update()

    def bg_update(self):
        """Check the day/night status every 15 minutes and set app background accordingly"""
        if self.app.wdata.weather_now.is_day.get() == 1:
            self.bg_day_night = Image.open("lib/img/daytime.jpg")
        else:
            self.bg_day_night = Image.open("lib/img/nighttime.jpg")
        self.bg_day_night = self.bg_day_night.resize(
            (int(self.app.window.winfo_screenwidth()*.35), int(self.app.window.winfo_screenheight()*.35)))
        self.bg_day_night = ImageTk.PhotoImage(self.bg_day_night)

        # Resize window to the day/night image size
        self.app.window.geometry(f"{self.bg_day_night.width() - 16 }x{self.bg_day_night.height() - 4}")
        self.bg.create_image(0, 0, anchor=tk.N+tk.W, image=self.bg_day_night)
        self.bg.after(60000*15, self.bg_update)
        self.fill_canvas()

    def fill_canvas(self):
        self.bg_ph = Image.open("lib/img/black_rec.png")
        w = int(self.bg_day_night.width() / 2.1)
        h = int(self.bg_day_night.height() * .91)
        self.bg_ph = self.bg_ph.resize((w, h))
        self.bg_ph = ImageTk.PhotoImage(self.bg_ph)
        self.bg_frame_left = self.bg.create_image(10, 10, anchor=tk.N + tk.W, image=self.bg_ph)


class WNowPanel:
    def __init__(self, app, m_panel):
        self.m_panel = m_panel
        self.app = app
        self.w_now_frame = tk.Frame(self.m_panel.w_panel)
        self.w_now_frame.grid(row=0, column=0, padx=16, pady=16)
        self.time_label = tk.Label(self.w_now_frame, text="Time: ")
        self.time_val = tk.Label(self.w_now_frame, text=self.app.wdata.gen_data.loc_time.get())
        self.cur_temp_label = tk.Label
        self.label_list = {'Time: ': self.app.wdata.gen_data.loc_time, 'Location:': self.app.wdata.gen_data.city,
                           'Current Temp: ': self.app.wdata.weather_now.temp_f, 'Real Feel: ': self.app.wdata.weather_now.real_feel,
                           'Conditions: ': self.app.wdata.weather_now.condition, 'Precipitation: ': self.app.wdata.weather_now.precip,
                           'Humidity: ': self.app.wdata.weather_now.humidity, 'Wind: ': self.app.wdata.weather_now.wind,
                           'Wind Direction: ': self.app.wdata.weather_now.wind_dir, 'UV Rating': self.app.wdata.weather_now.uv}
        self.label_obj = {}
        self.ratio = round((self.m_panel.bg_ph.width() / self.app.m_len) / 2.3)
        self.grid_all(self.label_list)

    def grid_all(self, label_list):
        cnt = 0
        for key in label_list:
            if key == 'Conditions: ':
                self.label_obj[f"{key}frame"] = tk.Frame(self.w_now_frame)
                self.label_obj[f"{key}frame"].grid_columnconfigure(1, weight=1)
                self.label_obj[f"{key}_label"] = tk.Label(self.label_obj[f"{key}frame"], text=key, justify=tk.LEFT,
                                                          anchor="w",
                                                          width=self.ratio)
                self.label_obj[f"{key}dual_frame_ph"] = tk.Frame(self.label_obj[f"{key}frame"], bg="blue",
                                                              width=self.ratio)
                self.label_obj[f"{key}dual_frame"] = tk.Frame(self.label_obj[f"{key}dual_frame_ph"])
                self.label_obj[f"{key}_val"] = tk.Label(self.label_obj[f"{key}dual_frame"], text=self.label_list[key].get())
                url = common.get_web_image('https://' + self.app.wdata.weather_now.icon_loc.get()[2:])
                self.label_obj[f"{key}_canvas"] = tk.Canvas(self.label_obj[f"{key}dual_frame"], width=url.width() - 4, height=url.height() - 4)

                c_h = 28
                c_w = 28
                self.label_obj[f"{key}_canvas"].create_image(c_h, c_w, anchor=tk.CENTER, image=url)

                self.label_obj[f"{key}frame"].grid(row=cnt, column=0, padx=5, sticky=tk.W + tk.E)

                self.label_obj[f"{key}dual_frame_ph"].grid(row=0, column=1)
                self.label_obj[f"{key}dual_frame"].pack(fill=tk.BOTH, expand=1)

                self.label_obj[f"{key}_label"].grid(row=0, column=0, padx=5, sticky=tk.W)
                self.label_obj[f"{key}_val"].grid(row=0, column=0, sticky=tk.E)
                self.label_obj[f"{key}_canvas"].grid(row=0, column=1, sticky=tk.E)

            else:
                self.label_obj[f"{key}frame"] = tk.Frame(self.w_now_frame)
                self.label_obj[f"{key}_label"] = tk.Label(self.label_obj[f"{key}frame"], text=key, justify=tk.LEFT,
                                                          anchor="w", width=self.ratio)
                self.label_obj[f"{key}_val"] = tk.Label(self.label_obj[f"{key}frame"], text=self.label_list[key].get(),
                                                        width=self.ratio)

                self.label_obj[f"{key}frame"].grid(row=cnt, column=0, padx=5, sticky=tk.W + tk.E)
                self.label_obj[f"{key}_label"].grid(row=0, column=0, padx=5, sticky=tk.W)
                self.label_obj[f"{key}_val"].grid(row=0, column=1, padx=5)
            cnt += 1


class ForcastPanel:
    def __init__(self, app, m_panel):
        self.m_panel = m_panel
        self.app = app
        self.w_now_frame = tk.Frame(self.m_panel.w_panel)
        self.w_now_frame.grid(row=0, column=1, padx=30, pady=30)
        self.w_now_frame.grid_columnconfigure(0, weight=1)
        self.hr_data = self.app.wdata.forcast_today.data['hour']
        self.ratio = round((self.m_panel.bg_ph.width() / self.app.m_len) / 1.5)
        self.bg = None
        #self.fill_canvas()
        self.obj_dic = {}
        self.img_ph = None
        self.graph_img = {}
        #self.grid_all()
        self.draw_text()

    def fill_canvas(self):
        x = int((self.m_panel.bg_day_night.width() / 2))
        y = int(self.m_panel.bg.coords(self.m_panel.bg_frame_left)[1])
        self.m_panel.bg_frame_right = self.m_panel.bg.create_image(x, y, anchor=tk.N+tk.W, image=self.m_panel.bg_ph)

    def grid_all(self):
        day = 0
        r_cnt = 0
        cnt = int((self.app.wdata.gen_data.loc_time.get().split()[1]).split(':')[0])
        self.hr_data = self.hr_data[cnt]
        hour_to_temp = [[], []]
        hour_to_precip = [[], []]
        while cnt < 23:
            self.obj_dic[f"hr{cnt}_icon"] = common.get_web_image_resize(2.2, 2.2, 'http:' + self.hr_data['condition']['icon'])
            self.obj_dic[f"hr{cnt}_frame"] = tk.Frame(self.w_now_frame)
            self.obj_dic[f"hr{cnt}_t_label"] = tk.Label(self.obj_dic[f"hr{cnt}_frame"], text=f"{self.hr_data['time'].split()[1]}")
            self.obj_dic[f"hr{cnt}_t_label"].configure(font=('Consolas', 8))
            self.obj_dic[f"hr{cnt}_canvas"] = tk.Canvas(self.obj_dic[f"hr{cnt}_frame"], width=self.obj_dic[f"hr{cnt}_icon"].width(), height=self.obj_dic[f"hr{cnt}_icon"].height())
            self.obj_dic[f"hr{cnt}_canvas"].create_image(16, 18, image=self.obj_dic[f"hr{cnt}_icon"])
            self.obj_dic[f"hr{cnt}_d_label"] = tk.Label(self.obj_dic[f"hr{cnt}_frame"], justify=tk.LEFT, width=self.ratio)
            self.obj_dic[f"hr{cnt}_d_label"].config(text=f"{self.hr_data['temp_f']}°F / {self.hr_data['chance_of_rain']}%")
            self.obj_dic[f"hr{cnt}_d_label"].config(font=('Consolas', 8))

            self.obj_dic[f"hr{cnt}_frame"].grid(row=r_cnt, column=0)
            self.obj_dic[f"hr{cnt}_t_label"].grid(row=r_cnt, column=0, sticky=tk.W)
            self.obj_dic[f"hr{cnt}_d_label"].grid(row=r_cnt, column=1, sticky=tk.W)
            self.obj_dic[f"hr{cnt}_canvas"].grid(row=r_cnt, column=2)

            hour_to_temp[0].append(f"{self.hr_data['time'].split()[1]}".split(':')[0])
            hour_to_temp[1].append(float(self.hr_data['temp_f']))
            hour_to_precip[0].append(f"{self.hr_data['time'].split()[1]}".split(':')[0])
            hour_to_precip[1].append(float(self.hr_data['chance_of_rain']))

            if cnt == 22 and day < 1:
                cnt = 0
                self.hr_data = self.app.wdata.gen_data.data['forecast']['forecastday'][1]
                day += 1
            if r_cnt == 12:
                break
            cnt += 1
            r_cnt += 1
            self.hr_data = self.app.wdata.forcast_today.data['hour'][cnt]

        self.graph_img['temp_graph'] = common.make_graph_of_size(clr1='yellow', clr2='red', hlst=hour_to_temp[0], tlst=hour_to_temp[1],
                                        scale=self.m_panel.bg_ph.width() - 40)

        self.graph_img['precip_graph'] = common.make_graph_of_size(clr1='blue', clr2='green', hlst=hour_to_precip[0], tlst=hour_to_precip[1],
                                        scale=self.m_panel.bg_ph.width() - 40)

        graph_canvas = tk.Canvas(self.w_now_frame, width=self.graph_img['temp_graph'].width(), height=self.graph_img['temp_graph'].height())
        self.w_now_frame.grid_columnconfigure(0, weight=1)
        graph_canvas.create_image(190, 48, image=self.graph_img['temp_graph'])
        graph_canvas.create_image(190, 48, image=self.graph_img['precip_graph'])
        graph_canvas.config(height=self.graph_img['precip_graph'].height())
        graph_canvas.grid(row=r_cnt, columnspan=2)

    def draw_text(self):
        cnt = int((self.app.wdata.gen_data.loc_time.get().split()[1]).split(':')[0])
        image = Image.open("lib/img/black_rec.png")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("lib/Roboto-MediumItalic.ttf", size=20)
        print(font.getsize('Tj'))
        x = 20
        while cnt < 23:
            txt = f"{cnt}:00 {self.hr_data[cnt]['temp_f']}°F {self.hr_data[cnt]['chance_of_rain']}%"
            wdth = font.getsize(txt)
            print(wdth)
            mk = 40
            for i in txt.split():
                draw.text((mk, x), i, font=font, fill=(255, 255, 255, 175))
                mk += 150
            #self.obj_dic[f"hr{cnt}_icon"] = common.get_web_image_resize(2, 2, 'http:' + self.hr_data[cnt]['condition']['icon'])
            url = 'http:' + self.hr_data[cnt]['condition']['icon']
            img = Image.open(r_get(url, stream=True).raw)
            img = img.resize((int(img.height * .5), int(img.width * .5)), Image.ANTIALIAS)
            image.paste(img, (mk, x), mask=img)
            #self.m_panel.bg.create_image(560, x+8, anchor=tk.N + tk.W, image=self.obj_dic[f"hr{cnt}_icon"])
            x = x + font.getsize('Tj')[1] + 5
            cnt +=1
        #image.show()
        self.graph_img['text'] = ImageTk.PhotoImage(image)
        x = int((self.m_panel.bg_day_night.width() / 2))
        y = int(self.m_panel.bg.coords(self.m_panel.bg_frame_left)[1])
        self.m_panel.bg_frame_right = self.m_panel.bg.create_image(x, y, anchor=tk.N + tk.W, image=self.graph_img['text'])



class ConstructWPanel:
    def __init__(self, app):
        self.m_panel = MainPanel(app)
        self.wnow_panel = WNowPanel(app, self.m_panel)
        self.fc_panel = ForcastPanel(app, self.m_panel)

    #
    #     # Create the time section
    #     self.time_frame = tk.Frame(self.data_frame)
    #     self.time_frame.grid(row=1, column=1)
    #     self.time_label = tk.Label(self.time_frame, text="Time/ETC: ")
    #     self.time_label.grid(row=0, column=0)
    #     self.time_now = datetime.now().strftime("%H:%M:%S")
    #     self.date_now = date.today().strftime("%d/%m/%Y")
    #     self.time_now_var = tk.StringVar()
    #     self.time_now_var.set(f"{self.time_now} {self.date_now}")
    #     self.time_val = tk.Label(self.time_frame, text=self.time_now_var.get())
    #     self.time_val.grid(row=0, column=1)

    #
    # def update_time(self):
    #     self.time_now = datetime.now().strftime("%H:%M:%S")
    #     self.date_now = date.today().strftime("%d/%m/%Y")
    #     self.time_now_var.set(f"{self.time_now} {self.date_now}")
    #     self.time_val.configure(text=self.time_now_var.get())
    #     self.time_val.after(1000, self.update_time)
    #
    # def get_condition_img(self):
    #     pass

