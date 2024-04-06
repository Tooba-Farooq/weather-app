import requests
from datetime import datetime
import pytz
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import math

# Initializing global variables
name = None


# Function to perform all tasks from fetching data to displaying it
def fetch_display_weather(city1):
    global name

    # Custom exception class for local_data not fetched
    class DataNotFetchedError(Exception):
        pass

    # Function for fetching weather details
    def weather_details(city2):

        # Fetching weather local_data from openweathermap
        api_key = "96220e7ccb58a16f88ac9d466101e661"
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city2}&units=imperial&APPID={api_key}")
        local_data = weather_data.json()

        # if user entered invalid location for that raising custom error so that I can come out of
        # fetch_display_weather function
        if not local_data or local_data["cod"] != 200:
            raise DataNotFetchedError("Data not fetched")

        # Function for finding out the correct time of given city
        def calculating_current_time():
            timestamp = local_data['dt']
            timezone_offset = local_data['timezone']
            timezone = pytz.FixedOffset(timezone_offset / 60)
            dt = datetime.fromtimestamp(timestamp, timezone)
            return dt

        # Defining current_time and local_current_day
        local_current_time = calculating_current_time().strftime('%I:%M %p')
        local_current_day = calculating_current_time().strftime("%A")
        return local_current_time, local_current_day, local_data

    # Function for setting up background images
    def defining_background_images(bg_image):
        time_image = Image.open(bg_image)
        image_resized = time_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        tk_time_image = ImageTk.PhotoImage(image_resized)
        local_bg_img = Label(master=root, image=tk_time_image)
        local_bg_img.pack(fill=BOTH, expand=True)
        local_bg_img.image = tk_time_image
        return local_bg_img

    # Function for defining variables and placing them in labels
    def labels_variables(local_current_time, local_current_day, local_data):
        global name

        # function to convert fetched wind direction which is in degrees to cardinal
        def degrees_to_cardinal(d):
            dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
                    'N']
            return dirs[round((d % 360) / 22.5)]

        # function to convert fetched sunset and sunrise time from unix timestamp format to 4:00 PM format
        def convert_unix_timestamp_to_time(unix_timestamp):
            datetime_object = datetime.fromtimestamp(unix_timestamp)
            return datetime_object.strftime("%I:%M %p")

        # function to calculate dew point
        def calculate_dewpoint(temperature_fahrenheit, humidity1):
            temperature_celsius = (temperature_fahrenheit - 32) * 5 / 9

            # Applying the Magnus formula
            a = 17.27
            b = 237.7
            alpha = ((a * temperature_celsius) / (b + temperature_celsius)) + math.log(humidity1 / 100.0)
            dew_point_celsius = (b * alpha) / (a - alpha)

            # Convert dew point back to Fahrenheit
            dew_point_fahrenheit = dew_point_celsius * 9 / 5 + 32

            return round(dew_point_fahrenheit)

        # defining variables
        name = local_data["name"]
        temp = round(local_data["main"]["temp"])
        weather = local_data["weather"][0]["main"]
        description = local_data["weather"][0]["description"]
        temp_max = round(local_data["main"]["temp_max"])
        temp_min = round(local_data["main"]["temp_min"])
        feels_like = round(local_data["main"]["feels_like"])
        wind_speed = round(local_data["wind"]["speed"], 1)
        wind_direction_deg = local_data["wind"]["deg"]
        wind_direction_cardinal = degrees_to_cardinal(wind_direction_deg)
        humidity = local_data["main"]["humidity"]
        visibility = f"{(local_data["visibility"]) / 1000}km"
        air_pressure = local_data["main"]["pressure"]
        dew_point = f"{calculate_dewpoint(temp, humidity)}°"
        cloud_cover = local_data["clouds"]["all"]
        sunrise_time = convert_unix_timestamp_to_time(local_data["sys"]["sunrise"])
        sunset_time = convert_unix_timestamp_to_time(local_data["sys"]["sunset"])

        # putting variables in labels
        (Label(master=main_frame, text=name, bg=frame_colour, fg="white", font=("Arial", 24, "bold"))
         .place(relx=0.5, rely=0.055, anchor=CENTER))
        (Label(master=main_frame, text="Current weather", bg=frame_colour, fg="white", font=("Arial", 11))
         .place(relx=0.5, rely=0.115, anchor=CENTER))
        (Label(master=main_frame, text=local_current_time, bg=frame_colour, fg="white", font=("Arial", 18))
         .place(relx=0.5, rely=0.155, anchor=CENTER))
        (Label(master=main_frame, text=f"{temp}", bg=frame_colour, fg="white", font=("Times New Roman", 100))
         .place(relx=0.5, rely=0.284, anchor=CENTER))
        (Label(master=main_frame, text="°F", bg=frame_colour, fg="white", font=("Arial", 30))
         .place(relx=0.655, rely=0.2))
        (Label(master=main_frame, text=weather, bg=frame_colour, fg="white", font=("Arial", 40))
         .place(relx=0.5, rely=0.42, anchor=CENTER))
        (Label(master=main_frame, text=description, bg=frame_colour, fg="white", font=("Arial", 18))
         .place(relx=0.5, rely=0.478, anchor=CENTER))
        (Label(master=main_frame, text=f"{local_current_day[:3]}  {temp_min}°/{temp_max}°", bg=frame_colour, fg="white",
               font=("Arial", 16)).place(relx=0.5, rely=0.532, anchor=CENTER))
        (Label(master=main_frame, text="feels like", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.02, rely=0.575))
        (Label(master=main_frame, text=f"{feels_like}°F", bg=frame_colour, fg="white",
               font=("Arial", 15)).place(relx=0.055, rely=0.625))
        (Label(master=main_frame, text=f"{wind_direction_cardinal} wind", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.5, rely=0.598, anchor=CENTER))
        (Label(master=main_frame, text=f"{wind_speed}mi/h {wind_direction_deg}°", bg=frame_colour, fg="white",
               font=("Arial", 15)).place(relx=0.5, rely=0.646, anchor=CENTER))
        (Label(master=main_frame, text="Humidity", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.755, rely=0.575))
        (Label(master=main_frame, text=f"{humidity}%", bg=frame_colour, fg="white",
               font=("Arial", 15)).place(relx=0.81, rely=0.625))
        (Label(master=main_frame, text="Visibility", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.02, rely=0.695))
        (Label(master=main_frame, text=visibility, bg=frame_colour, fg="white",
               font=("Arial", 15)).place(relx=0.042, rely=0.745))
        (Label(master=main_frame, text="Air Pressure", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.5, rely=0.718, anchor=CENTER))
        (Label(master=main_frame, text=f"{air_pressure}hPa", bg=frame_colour, fg="white",
               font=("Arial", 15)).place(relx=0.5, rely=0.766, anchor=CENTER))
        (Label(master=main_frame, text="Dew Point", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.735, rely=0.695))
        (Label(master=main_frame, text=dew_point, bg=frame_colour, fg="white", font=("Arial", 15))
         .place(relx=0.825, rely=0.745))
        (Label(master=main_frame, text="Sunrise", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.02, rely=0.815))
        (Label(master=main_frame, text=sunrise_time, bg=frame_colour, fg="white", font=("Arial", 15))
         .place(relx=0.02, rely=0.865))
        (Label(master=main_frame, text="Cloud Cover%", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.5, rely=0.838, anchor=CENTER))
        (Label(master=main_frame, text=f"{cloud_cover}%", bg=frame_colour, fg="white", font=("Arial", 15))
         .place(relx=0.5, rely=0.886, anchor=CENTER))
        (Label(master=main_frame, text="Sunset", bg=frame_colour, fg="white",
               font=("Arial", 15, "bold")).place(relx=0.795, rely=0.815))
        (Label(master=main_frame, text=sunset_time, bg=frame_colour, fg="white", font=("Arial", 15))
         .place(relx=0.765, rely=0.865))

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    #  initializing local_bg_img outside of try block so that I can use it in except block as well
    bg_img = None

    try:
        # Fetch weather details
        current_time, current_day, data = weather_details(city1)

        # converting current_time from string to datetime object
        current_time_obj = datetime.strptime(current_time, '%I:%M %p')

        # defining time ranges as datetime objects
        morning_hours_start = datetime.strptime("5:30 AM", '%I:%M %p')
        morning_hours_end = datetime.strptime("9:00 AM", '%I:%M %p')
        day_hours_start = datetime.strptime("9:01 AM", '%I:%M %p')
        day_hours_end = datetime.strptime("5:00 PM", '%I:%M %p')
        evening_hours_start = datetime.strptime("5:01 PM", '%I:%M %p')
        evening_hours_end = datetime.strptime("6:45 PM", '%I:%M %p')
        sunset_hours_start = datetime.strptime("6:46 PM", '%I:%M %p')
        sunset_hours_end = datetime.strptime("7:30 PM", '%I:%M %p')

    # setting background pictures of window and defining colours of frames based on time
        if morning_hours_start <= current_time_obj <= morning_hours_end:
            bg_img = defining_background_images("images\\early_morning.png")
            frame_colour = "#22455d"
        elif day_hours_start <= current_time_obj <= day_hours_end:
            bg_img = defining_background_images("images\\noon.png")
            frame_colour = "#52a3ba"
        elif evening_hours_start <= current_time_obj <= evening_hours_end:
            bg_img = defining_background_images("images\\evening.png")
            frame_colour = "#bd6c5e"
        elif sunset_hours_start <= current_time_obj <= sunset_hours_end:
            bg_img = defining_background_images("images\\sunset.png")
            frame_colour = "#63393a"
        else:
            bg_img = defining_background_images("images\\night.png")
            frame_colour = "#02041f"

    # Create main frame
        main_frame = Frame(master=bg_img, height=1350, width=400, bg=frame_colour)
        main_frame.pack(anchor=CENTER, padx=8, pady=17)

    # Place labels with weather details
        labels_variables(current_time, current_day, data)

    except DataNotFetchedError as ex:
        print("Error fetching weather local_data:", ex)
        print(city1)
        fetch_display_weather(name)  # calling this function again so screen does not go white
        Label(bg_img, text="Invalid locationⓘ", fg="red", font=("Arial", 11)).place(relx=0.9, rely=0.09)

    # Placing search bar and button
    search_bar = customtkinter.CTkEntry(master=root, placeholder_text="Search Location")
    search_bar.place(relx=0.89, rely=0.04)
    search_bar.bind("<Return>", lambda event: fetch_display_weather(search_bar.get()))


# Now making GUI
root = Tk()
root.title("Weather App")
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg="white")
icon = PhotoImage(file="images\\icon.png")
root.iconphoto(True, icon)


# fetching location
try:
    response = requests.get("https://ipinfo.io")
    location_data = response.json()
    city = location_data['city']
    fetch_display_weather(city)
except Exception as e:
    print("Error", f"Failed to fetch location: {e}")
    customtkinter.CTkLabel(root, text="Your location could not be fetched. However you can search weather of any "
                                      "location you want",  fg_color="white", text_color="black",
                           font=("Times New Roman", 20)).place(relx=0.2, rely=0.45)
    except_search_bar = customtkinter.CTkEntry(master=root, bg_color="white", border_width=2, border_color="gray",
                                               width=450, placeholder_text="Search", height=50)
    except_search_bar.place(relx=0.2, rely=0.5)
    (customtkinter.CTkButton(master=root, text="Search", bg_color="#b1b3b1", border_width=2,
                             border_color="gray", height=50, corner_radius=5,
                             command=lambda: fetch_display_weather(except_search_bar.get()))
     .place(relx=0.5, rely=0.5))
root.mainloop()
