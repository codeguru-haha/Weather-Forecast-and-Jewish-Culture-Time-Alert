# Weather Application using API

# Importing the libraries
from tkinter import *
import requests
import json
import datetime
from PIL import ImageTk, Image
from time import strftime
from datetime import datetime
from time import gmtime, strftime
from  tkinter import ttk
from playsound import playsound
import threading
from config import *

api_key = API_KEY 
zmanim_key = Zmanim_API_KEY 
user_id= USER_ID

# necessary details

root = Tk()
root.title("Weather App")
root.attributes("-fullscreen",True)

# alarm variable

alarm_time = []  
set_alarm_time = [{"time":"Time", "date":"Weekday"}]
snooze_val = 90

# Background setting

image = Image.open('background1.jpg')
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo, bg="#4a536b")
label.grid(row=1)

# Sound play
def sound_play():
    playsound("./alarm.mp3")
    time.sleep(snooze_val)    

# time compare for alarm  

def com_time():
    threading.Timer(60.0, com_time).start()

# compare with zmanim times
    compare_time = strftime('%I:%M %p')
    if compare_time in alarm_time:
        sound_play()

# compare with setting alarm
    dt = datetime.now()
    weekday=dt.strftime('%A')
    compare_data1={"time":compare_time, "date":weekday}
    compare_data2={"time":compare_time, "date":"Everyday"}
    if compare_data1 in set_alarm_time:
        sound_play()
    if compare_data2 in set_alarm_time:
        sound_play()
        
# String to datetime and get time

def convert_time(data):
    res = datetime.strptime(data, '%Y-%m-%dT%H:%M:%f%z').strftime('%I:%M %p')
    if (datetime.strptime(data, '%Y-%m-%dT%H:%M:%f%z').strftime('%Y-%m-%d') == '0001-01-01'):
        return ''
    return res

# Dates

def time():
    string = strftime('%I:%M:%S %p')
    hour.config(text=string)
    hour.after(1000, time)
  
# Setting alarm time add

def add_alarm():
    h = hour_var.get()
    m = min_var.get()
    p_m = p_m_var.get()
    w = day_var.get()
    get_time = h + ":" + m + " " + p_m
    savedata={"time":get_time, "date":w}
    if (savedata in set_alarm_time):
        return
    set_alarm_time.append(savedata)
    view_alarm_time()
    
# Setting alarm time delete

def del_alarm():
    h = hour_var.get()
    m = min_var.get()
    p_m = p_m_var.get()
    w = day_var.get()
    get_time = h + ":" + m + " " + p_m
    set_alarm_time.remove({"time":get_time, "date":w})
    view_alarm_time()


def view_alarm_time():
    view_data=[]
    for i in set_alarm_time:
        view_data.append("     " + str(i["time"]) + "       " + str(i["date"]))
    alarm_var = Variable(value=view_data)
    alarm_listbox = Listbox(listvariable=alarm_var, font=("Arial", 13, "bold"))
    alarm_listbox.place(x=115, y=450, height=400, width=235)
# -------------------------------------------------------------------------------------------
def get_all_data():
    get_weather_info()
    get_zmin_data()

#Zmanim data get and display
def get_zmin_data():

    zip_code = zip_entry.get()
    url = "https://api.myzmanim.com/engine1.json.aspx/searchPostal"
    tz = int(int(strftime("%z", gmtime()))/60 - 24)
    payload = f'coding=JS&timezone={tz}&query={zip_code}&key={zmanim_key}&user={user_id}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    locationid = res["LocationID"]
    url = "https://api.myzmanim.com/engine1.json.aspx/getDay"
    
    current_date = datetime.today().strftime('%Y-%m-%d')

    payload = f'coding=JS&language=en&locationid={locationid}&inpytdate={current_date}&key={zmanim_key}&user={user_id}'
    
    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    # necessary data display
    
    head_title = [{"name":"Name", "width": 240}, {"name":"Discription", "width": 240}]
    view_heading_data(day_detail, head_title)
    
    datas = ["Parsha",str(res["Time"]["Parsha"])]
    view_data(day_detail, 0, datas)
    
    datas = ["Hebrew Date",str(res["Time"]["DateJewish"])]
    view_data(day_detail, 1, datas)
    
    datas = ["Hebrew Date", str(res["Time"]["DateJewishLong"])]
    view_data(day_detail, 2, datas)
    
    datas = ["Omer Count",str(res["Time"]["Omer"])]
    view_data(day_detail, 3, datas)
    
    datas = ["Dawn",convert_time(res["Zman"]["Dawn72"])]
    view_data(day_detail, 4, datas)
    alarm_time.append(convert_time(res["Zman"]["Dawn72"]))
    
    datas = ["Earlest Talis :" + str(res["Place"]["YakirDegreesDefault"]),convert_time(res["Zman"]["YakirDefault"])]
    view_data(day_detail, 5, datas)
    alarm_time.append(convert_time(res["Zman"]["YakirDefault"]))
    
    datas = ["Sunrise",convert_time(res["Zman"]["SunriseDefault"])]
    view_data(day_detail, 6, datas)
    alarm_time.append(convert_time(res["Zman"]["SunriseDefault"]))
    
    datas = ["Shema MA",convert_time(res["Zman"]["ShemaMA72"])]
    view_data(day_detail, 7, datas)
    alarm_time.append(convert_time(res["Zman"]["ShemaMA72"]))
    
    datas = ["Shema Gra",convert_time(res["Zman"]["ShemaGra"])]
    view_data(day_detail, 8, datas)
    alarm_time.append(convert_time(res["Zman"]["ShemaGra"]))
    
    datas = ["Shachris Gra",convert_time(res["Zman"]["ShachrisGra"])]
    view_data(day_detail, 9, datas)
    alarm_time.append(convert_time(res["Zman"]["ShachrisGra"]))
    
    datas = ["Midday",convert_time(res["Zman"]["Midday"])]
    view_data(day_detail, 10, datas)
    alarm_time.append(convert_time(res["Zman"]["Midday"]))
    
    datas = ["Earliest Mincha",convert_time(res["Zman"]["MinchaStrict"])]
    view_data(day_detail, 11, datas)
    alarm_time.append(convert_time(res["Zman"]["MinchaStrict"]))
    
    datas = ["Plag Hamincha",convert_time(res["Zman"]["PlagGra"])]
    view_data(day_detail, 12, datas)
    alarm_time.append(convert_time(res["Zman"]["PlagGra"]))
    
    datas = ["Candlelighting : " + str(res["Place"]["CandlelightingMinutes"]) + "min",convert_time(res["Zman"]["Candles"])]
    view_data(day_detail, 13, datas)
    alarm_time.append(convert_time(res["Zman"]["Candles"]))
    
    datas = ["Sunset",convert_time(res["Zman"]["SunsetDefault"])]
    view_data(day_detail, 14, datas)
    alarm_time.append(convert_time(res["Zman"]["SunsetDefault"]))
    
    datas = ["Night 3 stars",convert_time(res["Zman"]["NightShabbos"])]
    view_data(day_detail, 15, datas)
    alarm_time.append(convert_time(res["Zman"]["NightShabbos"]))
    
    datas = ["Night 72 minutes",convert_time(res["Zman"]["Night72fix"])]
    view_data(day_detail, 16, datas)
    alarm_time.append(convert_time(res["Zman"]["Night72fix"]))
    
    datas = ["Minyan for Mincha",convert_time(res["Zman"]["SunsetDefault"])]
    view_data(day_detail, 17, datas)
    alarm_time.append(convert_time(res["Zman"]["SunsetDefault"]))
    
    day_detail.place(x=1400, y=400, height=450)
    
# Get weather and weather forecast and display data
def get_weather_info():

    zip_code = zip_entry.get()

    # API Current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}&units=imperial"

    
    api_request = requests.get(url)
    data = api_request.json()
    
    if(str(api_request) == "<Response [404]>"):
        lable_citi.config(text="Zip code incorrect!")
        return 1
    # Get current weather data
    
    current_temp = data["main"]["temp"]
    current_desc = data["weather"][0]["description"].title()
    high_temp = data["main"]["temp_max"]
    low_temp = data["main"]["temp_min"]
    humidity = data["main"]["humidity"]
    press = data["main"]["pressure"]
    
    # Display Current weather data
    lable_current_weather.config(text=f"Current : {current_temp}°F ,  {current_desc}\n High : {high_temp}°F ,   Low : {low_temp}°F \nHummidity : {humidity} % ,  Pressure : {press}")

    # API Forecast

    api_request = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?zip={zip_code}&appid={api_key}&units=imperial")

    api = json.loads(api_request.content)
    
    # city, country, lat, lon, sunrise, sunset
    
    lable_citi.config(text = api["city"]["name"]+", "+api["city"]["country"])
    lable_pos_lat.config(text = "Latitude : "+ str(api["city"]["coord"]["lat"]))
    lable_pos_long.config(text = "Longtitude : "+ str(api["city"]["coord"]["lon"]))
    
    ##### each time Forecast
    
    ind = 0
    head_title = [{"name":"Time", "width":100}, {"name":"Max Temp", "width":100}, {"name":"Min Temp", "width":100} , {"name":"State", "width":200}]
    view_heading_data(set_data_day, head_title)
    for hour in api["list"][:8]:
        hour_dt = datetime.strptime(hour["dt_txt"], "%Y-%m-%d %H:%M:%S")
        datas=[str(hour_dt.strftime("%I:%M %p")), str(hour["main"]["temp_min"])+ "°F", str(hour["main"]["temp_max"])+ "°F", str(hour["weather"][0]["description"].title())]
        view_data(set_data_day, ind, datas)
        ind = ind + 1
      
    # Update hourly weather Table
    
    set_data_day.place(x=400, y=400, height=450)
   
    # Get 5 day forecast data
    ind = 0
    head_title = [{"name":"Day", "width":120}, {"name":"Max Temp", "width":100}, {"name":"Min Temp", "width":100} , {"name":"State", "width":200}]
    view_heading_data(day_forecast, head_title)
    # Parse JSON response for 5 day forecast data
    for daydata in api["list"][::8]:
        day_dt = datetime.strptime(daydata["dt_txt"], "%Y-%m-%d %H:%M:%S")
        datas = [str(day_dt.strftime("%Y-%m-%d")), str(daydata["main"]["temp_min"])+ "°F", str(daydata["main"]["temp_max"])+ "°F", str(daydata["weather"][0]["description"].title())]
        view_data(day_forecast, ind, datas)
        ind = ind + 1
    # Update 5 day forecast weather table
    day_forecast.place(x=900, y=400, height=450)
    
    
    # Get Day details
   
# making data field
# Making Header
def view_heading_data(field, data):
    buf = []
    for i in data:
        buf.append(i["name"])
    field['columns']= (buf)
    field.column("#0", width=0,  stretch=NO)
    for i in data:
        field.column(i["name"],anchor=CENTER, width=i["width"],)
        
    field.heading("#0",text="",anchor=CENTER)
    for i in data:
        field.heading(i["name"],text=i["name"],anchor=CENTER)
        
# Insert data in table

def view_data(field, id, data):
    field.insert(parent='',index='end',iid=id,text='',values=(data))
    
# -------------------------------------------------------------------------------------------

# zip code input

zip_entry = Entry(root, width=15, font="Poppins 40" , bg="#f2d767", fg="white")
zip_entry.place(x=80, y=90)
Label(root, text="Enter your zip-code", font="Poppins 37", bg="#f2d767", fg="white").place(x=80, y=20)

# Search Bar and Button - function will get executed after presing button

get_weather_button = Button(root, text="Get Weather", command=get_all_data, width=10, fg="red" , bg="#f2d767" ,cursor="arrow", font="Poppins 40 bold")
get_weather_button.place(x=135, y=165)

# Country Names and Coordinates Current Weather
lable_citi = Label(root, text="", width=0, bg='#f4cd61', fg="white", font="Montserrat 50 bold")
lable_citi.place(x=640, y=70)

# Latitude and Longtitude
lable_pos_lat = Label(root, text="", width=0, bg='#f4cd61', fg="white", font="Montserrat 30 bold")
lable_pos_lat.place(x=650, y=170)

lable_pos_long = Label(root, text="", width=0, bg='#f4cd61', fg="white", font="Montserrat 30 bold")
lable_pos_long.place(x=650, y=220)

lable_current_weather = Label(root, text="", width=0, bg="#f6c058", fg="white", font="Montserrat 30 bold")
lable_current_weather.place(x=1200, y=70)


# Each Hour Temperature
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 13))
# style.configure("Treeview.Insert", font=(None, 15))

Label(root, text="Hour Forecast", font="Montserrat 35 bold", fg="white", bg="#c6cad5").place(x=400, y=320, width=500)
set_data_day = ttk.Treeview(root)

# Day Weather forecast

Label(root, text="5 Day Forecast ", font="Montserrat 35 bold", fg="white", bg="#c6cad5").place(x=900, y=320, width=600)
day_forecast = ttk.Treeview(root)

# Day Detail

Label(root, text="Day Details ", font="Montserrat 35 bold", fg="white", bg="#c6cad5").place(x=1400, y=320, width=700)
day_detail = ttk.Treeview(root)

Label(root, text="Alarm Setting", width=10, bg="#c6cad5", fg="white" , font="Montserrat 35 bold").place(x=0, y=320, width=450)

# Setting hour min p_a and weekday for alarm
hour_set = ["01" ,"02","03" ,"04","05" ,"06","07" ,"08","09" ,"10","11" ,"12"]
hour_var = StringVar(value=hour_set[0])
hour_dropdown = OptionMenu(root, hour_var, *hour_set)
hour_dropdown.config(font=("Arial", 11, "bold"), width=4, bg="#dbdee5")
hour_dropdown.place(x=75, y=400)

min_set = ["00" ,"05" ,"10","15" ,"20","25" ,"30","35" ,"40","45" ,"50","55"]
min_var = StringVar(value=min_set[0])
min_dropdown = OptionMenu(root, min_var, *min_set)
min_dropdown.config(font=("Arial", 11, "bold"), width=4, bg="#dbdee5")
min_dropdown.place(x=150, y=400)

p_m_set = ["AM" ,"PM"]
p_m_var = StringVar(value=p_m_set[0])
p_m_dropdown = OptionMenu(root, p_m_var, *p_m_set)
p_m_dropdown.config(font=("Arial", 11, "bold"), width=4, bg="#dbdee5")
p_m_dropdown.place(x=225, y=400)

day_set = ["EveryDay" ,"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_var = StringVar(value=day_set[0])
day_dropdown = OptionMenu(root, day_var, *day_set)
day_dropdown.config(font=("Arial", 11, "bold"), width=7, bg="#dbdee5")
day_dropdown.place(x=300, y=400)

# Alarm List Header

alarm_var = Variable(value=["      Time        Weekday"])

alarm_listbox = Listbox(listvariable=alarm_var, font=("Arial", 13, "bold"))
alarm_listbox.place(x=115, y=550, height=300, width=235)

Button(root, text="Add", command=add_alarm, width=7, fg="red" , bg="#ced2dd" ,cursor="arrow", font="Poppins 12 bold").place(x=135, y=875)
Button(root, text="Delete", command=del_alarm, width=7, fg="red" , bg="#ced2dd" ,cursor="arrow", font="Poppins 12 bold").place(x=265, y=875)

#Snooze part

def get_snooze_val(val):
    global snooze_val
    snooze_val = val

class Snooze:
    def __init__(self, name, val):
        Radiobutton(
            text=name,
            command=lambda i=val: get_snooze_val(i),
            variable=var, value=val).place(x=160, y= int(val / 90) * 30 + 420)

var = IntVar()
var.set(90)

Snooze("90 Seconds", 90)
Snooze(" 3 minutes", 180)
Snooze(" 5 minutes", 300)

# Placing clock and date

dt = datetime.now()
date = Label(root, text=dt.strftime('%A'), bg="#f2d767", font="poppins 60 bold", fg="white")
date.place(x=250, y=930, height=150)

month = Label(root, text=dt.strftime('%d %B %Y'), bg="#f4cf62", fg="White", font="Poppins 60 bold")
month.place(x=650, y=930, height= 150)

#Label(root, text="Current time: ", bg="#edc520", font="Poppins 10").place(x=330, y=460)
# Time
hour = Label(root, 
            font=('calibri', 80, 'bold'),
            background='purple',
            foreground='white')
hour.place(x=1250, y=930, width=700, height=150)

com_time()
time()

root.mainloop()
