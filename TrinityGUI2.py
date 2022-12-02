import math
import tkinter as tk
from random import random
from tkinter import ttk
from PIL import ImageTk, Image
from astropy.io import ascii
import glob
import os
import matplotlib.pyplot as plt
import datetime
from astropy.io import ascii
import numpy as np
import sys

LARGEFONT = ("Verdana", 35,)
MedFONT = ("Verdana", 25)
SmFONT = ("Verdana", 15)

HOMEDIR = 'C:/Users/Ginkl/Documents/TrintyWork/'
CAMDIR = HOMEDIR + "Cams/"
INCAMDIR = CAMDIR + "In/"
OUTCAMDIR = CAMDIR + "Out/"
WXDIR = HOMEDIR + 'Weather_data/'

'''
HOMEDIR = "/home/mpotts32/"
CAMDIR = HOMEDIR + "cams/"
INCAMDIR = CAMDIR + "IN/"
OUTCAMDIR = CAMDIR + "OUT/"
WXDIR = HOMEDIR + "weather/"
'''

class popupWindow(object):
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        self.l = tk.Label(top, text="Hello World")
        self.l.pack()
        self.e = tk.Entry(top)
        self.e.pack()
        self.b = tk.Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        canvas = tk.Canvas()
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        ttk.Label(self, text="Trinty GUI", font=LARGEFONT).place(x=25, y=25)

        ####### Door Buttons #############
        def random_status():
            Door_message = ttk.Label(self)
            # Door_message.place_forget()
            value = random()
            if value <= .33:
                statement = 'Status All good'
            elif .33 < value <= .66:
                statement = 'small error'

            else:
                statement = 'ERROR Door wont shut'

            Door_message.config(text=statement)

            Door_message.place(x=25, y=375)
            Door_message.after(5000, Door_message.destroy)

        # canvas.create_rectangle(10,100,1000,500,outline ="black",fill ="white",width = 2)
        # canvas.place(x=750)

        def door_open():
            this_b = tk.Label(self, text='Door Opening')
            this_b.place(x=75, y=175)
            this_b.after(5000, this_b.destroy)

        def door_close():
            this_b = tk.Label(self, text='Door Closing')
            this_b.place(x=75, y=275)
            this_b.after(5000, this_b.destroy)

        door_o_button = ttk.Button(self, text="Door Open", command=door_open)
        door_o_button.place(x=25, y=125, height=50, width=150)

        door_c_button = ttk.Button(self, text="Door Close", command=door_close)
        door_c_button.place(x=25, y=225, height=50, width=150)

        door_status_button = ttk.Button(self, text="Check Status", command=random_status)
        door_status_button.place(x=25, y=325, height=50, width=150)

        # add a text label with status

        ### Webcam images
        # frame = ttk.Frame(self, width=600, height=400)
        # frame.pack()
        # frame.place(x=400,y=100)#anchor='center', relx=0.5, rely=0.5)

        # these are fake button that have the images for the outside and inside cameras that will refresh
        # to whatever the last created file is in the folder

        def inside_images(file_path_in):
            list_in_files = glob.glob(file_path_in)
            file_in = max(list_in_files, key=os.path.getctime)
            #print(f"hey {file_out}")
            img_in = Image.open(file_in).resize((550, 350))
            self.image_in = ImageTk.PhotoImage(img_in)

            inside_but = tk.Button(self, text='Click Me !', image=self.image_in)
            inside_but.place(x=350, y=25)
            ttk.Label(self, text=str(os.path.basename(file_in)), font=SmFONT).place(x=350, y=400)
            canvas.after(50000,inside_images, file_path_in)

        inside_images(INCAMDIR + '*')

        def open_indoor_folder():
            os.startfile(INCAMDIR)
        ttk.Button(self, text="Indoor filepath", command=open_indoor_folder).place(x=700, y=400,height=50, width=150)
        # putting the grid in its place by using
        # grid
        def outside_images(file_path_out):
            list_out_files = glob.glob(file_path_out)
            file_out = max(list_out_files, key=os.path.getctime)
            #print(f"hey {file_out}")
            img_out = Image.open(file_out)

            img_out = img_out.resize((550, 350))

            self.image_out = ImageTk.PhotoImage(img_out)

            outside_but = tk.Button(self, text='Click Me !', image=self.image_out)
            outside_but.place(x=925, y=25)
            ttk.Label(self, text=str(os.path.basename(file_out)), font=SmFONT).place(x=950, y=400)
            canvas.after(50000,outside_images, file_path_out)

        outside_images(OUTCAMDIR + '*')

        def open_outdoor_folder():
            os.startfile(OUTCAMDIR)

        ttk.Button(self, text="Outdoor filepath", command=open_outdoor_folder).place(x=1325, y=400, height=50, width=150)


        # self.image1 = ImageTk.PhotoImage(file="STScI-01G8KCAK75G2JPGHNC40PVTA1R.png")

        # tk.Button(self, text='Click Me !', image=self.image1).place(x=300, y=25)

        ########  Camera Buttons ##########
        '''
        def inside_image():
            self.image = ImageTk.PhotoImage(file='C:/Users/Ginkl/Documents/TrintyWork/Cams/OUt/20221019205435_IN_355.jpg')
            tk.Button(self, text='Click Me !', image=self.image).place(x=800, y=25)
        def outside_image():
            self.image = ImageTk.PhotoImage(file="STScI-01G8KCAK75G2JPGHNC40PVTA1R.png")
            tk.Button(self, text='Click Me !', image=self.image).place(x=800, y=25)
        def alternate_image():
            pass
        door_cam_button = ttk.Button(self, text="Door View Only", command=inside_image)
        door_cam_button.place(x=925, y=475, height=50, width=150)
        out_cam_button = ttk.Button(self, text="Outside View Only", command=outside_image)
        out_cam_button.place(x=1125, y=475, height=50, width=150)
        alt_cam_button = ttk.Button(self, text="Alternate Images", command=alternate_image)
        alt_cam_button.place(x=1325, y=475, height=50, width=150)
        '''

        ##### Weather Section ########
        weather_title = tk.Label(self, text="Weather Data", font=MedFONT)
        weather_title.place(x=925, y=525)

        weather_button = ttk.Button(self, text="More Weather Data", command=lambda: controller.show_frame(Page1))
        weather_button.place(x=1325, y=525, height=50, width=150)

        ##### Labels for the weather section ##########
        tk.Label(self, text="Temperature Current:", font=SmFONT).place(x=925, y=635)
        #tk.Label(self, text="Temperature Avg (1h):", font=SmFONT).place(x=925, y=605)
        tk.Label(self, text="Wind Speed Current:", font=SmFONT).place(x=925, y=665)
        #tk.Label(self, text="Wind Speed Avg (1h):", font=SmFONT).place(x=925, y=665)
        tk.Label(self, text="Humidity Current:", font=SmFONT).place(x=925, y=695)
        tk.Label(self, text="Pressure Current:", font=SmFONT).place(x=925, y=725)
        tk.Label(self, text="Wind Direction:", font=SmFONT).place(x=925, y=755)
        tk.Label(self, text="Dew Point", font=SmFONT).place(x=925, y=785)
        tk.Label(self, text="Sunrise:", font=SmFONT).place(x=925, y=815)
        tk.Label(self, text="Sunset:", font=SmFONT).place(x=925, y=845)
        tk.Label(self, text="Civil Twilight:", font=SmFONT).place(x=925, y=875)
        tk.Label(self, text="Astro Twilight:", font=SmFONT).place(x=925, y=905)

        ####### Updating Labels from the weather station ###############

        # putting the button in its place by
        # using grid
        # button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        #button2 = ttk.Button(self, text="Page 2",
        #                     command=lambda: controller.show_frame(Page2))
        #button2.grid(row=2, column=1, padx=10, pady=10)


        #weather_data_location = 'weatherdata.txt'

        list_of_files = glob.glob(WXDIR + '*')  # * means all if need specific format then *.csv
        latest_file = min(list_of_files, key=os.path.getctime)
        weather_data_location = latest_file
        print(latest_file)
        def make_plots_and_labels(file):

            def weather_data(file):
                obs_col_names = (
                    "Node", "RelativeWindDirection", "RelativeWindSpeed", "CorrectedWindDirection",
                    "AverageRelativeWindDirection",
                    "AverageRelativeWindSpeed", "RelativeGustDirection", "RelativeGustSpeed",
                    "AverageCorrectedWindDirection",
                    "WindSensorStatus", "Pressure", "Pressure at Sea level", "Pressure at Station", "Relative Humidity",
                    "Temperature",
                    "Dewpoint",
                    "Absolute Humidity", "compassHeading", "WindChill", "HeatIndex", "AirDensity", "WetBulbTempature",
                    "SunRiseTime", "SolarNoonTime", "SunsetTime",
                    "Position of the Sun", "Twilight (Civil)",
                    "Twilight (Nautical)",
                    "Twilight (Astronomical)", "X-Tilt", "Y-Tilt", "Z-Orientation", "User Information Field",
                    "System Date and Time",
                    "Supply Voltage", "Status", "Checksum")

                obs_col_pos = (
                    0, 3, 7, 14, 18, 22, 29, 33, 40, 44, 49, 56, 63, 70, 74, 81, 88, 94, 98, 100, 104, 108, 115, 121,
                    127, 133,
                    141,
                    147, 153, 159, 163, 167, 170, 171, 193, 199, 204)
                #obsres = ascii.read(file, format='fixed_width_no_header', data_start=0, col_starts=obs_col_pos, names=obs_col_names)
                obsres = ascii.read(file, format='no_header', data_start=0, delimiter=',',names=obs_col_names)

                # return obsres
                #print(obsres)

                #with open('check.txt', 'w') as filehandle:
                #    for listitem in obsres:
                 #       filehandle.write('%s\n' % listitem)

                output_array = np.array(obsres)
                for i in range(len(output_array)):
                    for j in range(len(output_array[0])):
                        output_array[i][j] = ''.join(str(output_array[i][j]).split(','))
                return output_array

            all_data = weather_data(file)

            # print(all_data)
            def save_plot_png(all_data):
                size = len(all_data)
                wind_direction = [0] * size
                date_n_time = [0] * size
                date = [0] * size
                tempature = [0] * size
                wind_speed = [0] * size
                humidity = [0] * size
                dew_point = [0] * size
                pressure = [0] * size

                for i in range(len(all_data)):
                    tempature[i] = float(all_data[i][14])
                    wind_speed[i] = float(all_data[i][2])
                    humidity[i] = float(all_data[i][13])
                    dew_point[i] = float(all_data[i][15])
                    pressure[i] = float(all_data[i][12])
                    wind_direction[i] = int(all_data[i][1])
                    date_n_time[i] = all_data[i][33]
                    temp = str(date_n_time[i])
                    date[i] = datetime.datetime.strptime(temp[:19], "%Y-%m-%dT%H:%M:%S")

                #print(date)

                def plot_format(x, y, xlabel, ylabel, title, color,fig):


                    plt.plot(x, y, c=color)
                    plt.title(title)
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.xticks(rotation=25)
                    try:
                        os.mkdir(f'{HOMEDIR}weather_plots')
                    except:
                        pass
                    fig.canvas.draw()
                    plt.savefig(f'{HOMEDIR}weather_plots/{title}.png')
                    fig.clear()
                    # FIx so not to many figures will be made


                plot_format(date, wind_direction, 'Date', 'Wind Direction (Degrees)', 'Wind_direction_over_time',
                            'green',fig)
                plot_format(date, tempature, 'Date', 'Tempature (Degrees)', 'Temperature_over_time', 'red',fig)
                plot_format(date, humidity, 'Date', 'Humidity (Percent)', 'Humidity_over_time', 'blue',fig)
                plot_format(date, wind_speed, 'Date', 'Wind Speed (units)', 'Wind_speed_over_time', 'purple',fig)
                plot_format(date, dew_point, 'Date', 'Dew Point (Degrees)', 'Dewpoint_over_time', 'orange',fig)
                plot_format(date, pressure, 'Date', 'Pressure (units)', 'Pressure_over_time', 'pink',fig)


            save_plot_png(all_data)

            def create_labels():
                # updating variables

                tempature = float(all_data[-1][14])
                wind_speed = float(all_data[-1][2])
                humidity = float(all_data[-1][13])
                dew_point = float(all_data[-1][15])
                pressure = float(all_data[-1][12])
                wind_direction = int(all_data[-1][1])
                date_n_time = all_data[-1][33]
                sun_rise = str(all_data[-1][22])
                sun_set = str(all_data[-1][24])
                civil_twi = str(all_data[-1][26])
                astro_twi = str(all_data[-1][28])

                date = datetime.datetime.strptime(date_n_time[:19], "%Y-%m-%dT%H:%M:%S")

                tk.Label(self, text=f'{tempature}', font=SmFONT).place(x=1300, y=635)
                # tk.Label(self, text="Temperature Avg (1h):", font=SmFONT).place(x=925, y=605)
                tk.Label(self, text=f'{wind_speed}', font=SmFONT).place(x=1300, y=665)
                # tk.Label(self, text="Wind Speed Avg (1h):", font=SmFONT).place(x=925, y=665)
                tk.Label(self, text=f'{humidity}', font=SmFONT).place(x=1300, y=695)
                tk.Label(self, text=f'{pressure}', font=SmFONT).place(x=1300, y=725)
                tk.Label(self, text=f'{wind_direction}', font=SmFONT).place(x=1300, y=755)
                tk.Label(self, text=f'{dew_point}', font=SmFONT).place(x=1300, y=785)
                tk.Label(self, text=f'{sun_rise}', font=SmFONT).place(x=1300, y=815)
                tk.Label(self, text=f'{sun_set}', font=SmFONT).place(x=1300, y=845)
                tk.Label(self, text=f'{civil_twi}', font=SmFONT).place(x=1300, y=875)
                tk.Label(self, text=f'{astro_twi}', font=SmFONT).place(x=1300, y=905)

            create_labels()
            canvas.after(50000, make_plots_and_labels, weather_data_location)

        fig = plt.figure()
        make_plots_and_labels(weather_data_location)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas()




        label = ttk.Label(self, text="Weather Data Plots", font=LARGEFONT)
        label.place(x=25,y=25)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.place(x=100, y=450, height=50, width=150)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text=" More Weather Plots",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.place(x=100, y=500, height=50, width=150)



        def open_popup():
            top = tk.Toplevel(self)
            top.geometry("750x250")
            top.title("Weather Data Search")
            tk.Label(top, text="Please enter a date for the weather graphs you want to look at").place(x=25, y=25)
            tk.Label(top, text="Ex. YxxxMxDx").place(x=25, y=50)

            e = tk.Entry(top)
            e.place(x=25,y=75)

            def get_info():
                v = e.get()
                string_to_update=tk.StringVar()
                input_label= tk.Label(top, textvariable=string_to_update,fg='red').place(x=25,y=125)

                if len(v)==8 and v.isdigit()==True:
                    string_to_update.set("")

                    old_data=weather_plots(f'weather_{v}.txt')
                    # make the plots
                    # -update how the save location is determined
                    # make a folder in the weather plots folder
                    # call function to make the same plots to a folder and open the folder so it can be viewed
                else:
                    string_to_update.set("nay")
                    #tk.Label(top, text="Please make a valid input",fg='red').place(x=25, y=125)
                return print(v)
            tk.Button(top, text='Ok', command=get_info).place(x=25,y=100)


        # TO DO
        button3 = ttk.Button(self,text= "Weather Data Search",command=open_popup)
        button3.place(x=100, y=550, height=50, width=150)





        def weather_plots(file_path_in):
            #list_in_files = glob.glob(file_path_in)
            #file_in = max(list_in_files, key=os.path.getctime)
            # print(f"hey {file_out}")
            # ttk.Label(self, text=str(os.path.basename(file_in)), font=SmFONT).place(x=350, y=400)
            plot_1 = Image.open(f'{file_path_in}Dewpoint_over_time.png').resize((550, 350))
            self.plot_1 = ImageTk.PhotoImage(plot_1)
            tk.Button(self, text='Click Me !', image=self.plot_1).place(x=325, y=125)

            plot_2 = Image.open(f'{file_path_in}Temperature_over_time.png').resize((550, 350))
            self.plot_2 = ImageTk.PhotoImage(plot_2)
            tk.Button(self, text='Click Me !', image=self.plot_2).place(x=325, y=500)

            plot_3 = Image.open(f'{file_path_in}Pressure_over_time.png').resize((550, 350))
            self.plot_3 = ImageTk.PhotoImage(plot_3)
            tk.Button(self, text='Click Me !', image=self.plot_3).place(x=925, y=125)

            plot_4 = Image.open(f'{file_path_in}Wind_direction_over_time.png').resize((550, 350))
            self.plot_4 = ImageTk.PhotoImage(plot_4)
            tk.Button(self, text='Click Me !', image=self.plot_4).place(x=925, y=500)

            #plot_5 = Image.open(f'{file_path_in}Wind_speed_over_time.png').resize((550, 350))
            #self.plot_5 = ImageTk.PhotoImage(plot_5)
            #tk.Button(self, text='Click Me !', image=self.plot_5).place(x=950, y=775)

            canvas.after(50000, weather_plots, file_path_in)

        weather_plots("C:\\Users\Ginkl\Documents\TrintyWork\weather_plots\\")

        def weather_plots_folder():
            os.startfile(r'C:\\Users\Ginkl\Documents\TrintyWork\weather_plots')

        ttk.Button(self, text="Weather Plots File Path", command=weather_plots_folder).place(x=100, y=400, height=50, width=150)




# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas()
        label = ttk.Label(self, text="More Weather Data", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Weather Data Plot 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.place(x=100, y=450, height=50, width=150)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.place(x=100, y=400, height=50, width=150)

        def weather_plots(file_path_in):
            #list_in_files = glob.glob(file_path_in)
            #file_in = max(list_in_files, key=os.path.getctime)
            # print(f"hey {file_out}")
            # ttk.Label(self, text=str(os.path.basename(file_in)), font=SmFONT).place(x=350, y=400)


            plot_1 = Image.open(f'{file_path_in}Wind_speed_over_time.png').resize((550, 350))
            self.plot_1 = ImageTk.PhotoImage(plot_1)
            tk.Button(self, text='Click Me !', image=self.plot_1).place(x=325, y=125)
            '''
            plot_2 = Image.open(f'{file_path_in}Temperature_over_time.png').resize((550, 350))
            self.plot_2 = ImageTk.PhotoImage(plot_2)
            tk.Button(self, text='Click Me !', image=self.plot_2).place(x=325, y=500)

            plot_3 = Image.open(f'{file_path_in}Pressure_over_time.png').resize((550, 350))
            self.plot_3 = ImageTk.PhotoImage(plot_3)
            tk.Button(self, text='Click Me !', image=self.plot_3).place(x=925, y=125)

            plot_4 = Image.open(f'{file_path_in}Wind_direction_over_time.png').resize((550, 350))
            self.plot_4 = ImageTk.PhotoImage(plot_4)
            tk.Button(self, text='Click Me !', image=self.plot_4).place(x=925, y=500)
            '''
            canvas.after(50000, weather_plots, file_path_in)

        weather_plots("C:\\Users\Ginkl\Documents\TrintyWork\weather_plots\\")

        def weather_plots_folder():
            os.startfile(r'C:\\Users\Ginkl\Documents\TrintyWork\weather_plots')


# Driver Code

app = tkinterApp()
app.geometry('1500x1000')
app.title("Trinity GUI")
app.mainloop()
