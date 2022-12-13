from tkinter import *
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import csv
import requests
import math
import random
from datetime import datetime
import csv
from random import randint

root = Tk()

with open("temperatures.csv",'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        column = {}
        for h in headers:
            column[h] = []
        for row in reader:
            for h,v in zip(headers,row):
                column[h].append(v)
        print('[Logging-Cities]', column['Лингвистическая метка'])

key = 'f02845d4e0f85335849e27e0c35ac8ba'
url = 'http://api.openweathermap.org/data/2.5/weather'
weathers = ["Париж","Бангкок", "Варшава", "Сиэтл"]
x_original = []
y_original = []
analysisLength = 20
point_y = []
x_fuzzified = []
date_list = []
feels_like = []
longitude = []
latitude = []
Q = []
ground_level = []
maxt = []
mint = []
#clouds = []
sunset = []
sunrise = []

longFact = []
latFact = []
qFact = []
ground_levelFact = []
maxTFact = []
minTFact = []

    
def get_weather(city):
    params = {'APPID': key, 'q': city, 'units': 'metric'}
    result = requests.get(url, params=params)
    weather = result.json()
    info = f'{weather["main"]["temp"]}'
    return info

def recalculate():
    global weathers
    city = cityField.get()
    weathers.append(city)
    print('[Logging-City-Parse]', city)
    print('[Logging-Cities-List]', weathers)
    parse_weather()
root['bg'] = '#fafafa'
root.title('Погодное приложение')
root.geometry('1600x900')


frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top_right = Frame(root, bg='white',bd=5)
frame_top_left = Frame(root, bg='white',bd=5)
frame_top.place(relx=0.45, rely=0.15, width=210, relheight=0.25)
frame_top_right.place(relx=0.05, rely=0.05,width = 560,relheight = 0.45)
frame_top_left.place(relx=0.60,rely=0.05,width=560,relheight=0.45)


frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.4)

cityField = Entry(frame_top, bg='white', font=30)
cityField.pack()


btn = Button(frame_top, text='Посмотреть погоду', command=recalculate)
btn.pack()


info = Label(frame_bottom, text='Погодная информация', bg='#ffb700', font=40)
info.pack()

scrollbar = Scrollbar(frame_top)
scrollbar.pack(side=RIGHT, fill=Y)
weather_listbox = Listbox(frame_top,yscrollcommand=scrollbar.set,width=40)
weather_listbox.pack()
scrollbar.config(command=weather_listbox.yview)



def draw_base(x,y):

    for widget in frame_top_right.winfo_children():
        widget.destroy()
    fig_orig = plt.figure(figsize=(8, 7))
    ax = fig_orig.add_subplot(111)
    ax.clear()
    print(x)
    print(y)
    ax.scatter(x, y)
    
    plt.xticks(np.arange(0, max(x), int(max(x)/3)))
    plt.yticks(np.arange(0, max(y), int(max(y)/3)))
    
    for i, txt in enumerate(weathers):
        plt.annotate(txt, (x[i], y[i])) 
    canvas = FigureCanvasTkAgg(fig_orig, frame_top_right)

    toolbar = NavigationToolbar2Tk(canvas, frame_top_right)

    toolbar.update()
    
    root.update()
    canvas._tkcanvas.update()
    frame_top_right.update()
    canvas._tkcanvas.pack()
    frame_top_right.pack_propagate(False)
    
def parse_weather():
    global x_original
    global y_original
    global feels_like
    global longitude
    global latitude
    global Q
    global ground_level
    global maxt
    global mint
    #global clouds
    global sunset
    global sunrise
    weather_listbox.delete(0, END)
    
    for weather_ex in weathers:
        city_params = {'APPID': key, 'q': weather_ex, 'units': 'metric'} 
        city_result = requests.get(url, params=city_params)
        city_weather = city_result.json()
        print(city_weather)
        weather_listbox.insert(END, f'{str(city_weather["name"])}: {city_weather["main"]["temp"]}, timezone: {city_weather["timezone"]}')
        x_original.append(city_weather["main"]["temp"]) 
        y_original.append(city_weather["timezone"]/1000)
        feels_like.append(city_weather["main"]["feels_like"])
        longitude.append(city_weather["coord"]["lon"])
        latitude.append(city_weather["coord"]["lat"])
        Q.append(city_weather["main"]["pressure"])
        ground_level.append(city_weather["main"]["pressure"])
        maxt.append(city_weather["main"]["temp_max"])
        mint.append(city_weather["main"]["temp_min"])
        #clouds.append(city_weather["weather"]["id"])
        sunset.append(city_weather["sys"]["sunset"])
        sunrise.append(city_weather["sys"]["sunrise"])
    print(x_original,"LOOK")
    draw_base(x_original, y_original)
    uncertainty_generator()
    print(city_weather)

def uncertainty_generator():
    global point_y
    x_array = []
    y_array = []
    center = []
    function_type = []
    boundary = []
    for i,function_ex in enumerate(column['Лингвистическая метка']):
        max_t = float(column['max t'][i])
        min_t = float(column['min t'][i])
        function_type.append(column['function'][i])
        
        if(function_type[i] == "Треугольная"):
            center.append((max_t+min_t)/2)
            x_array.extend((min_t,center[i],max_t))
            y_array.extend((0,1,0))
            boundary.append(int(len(x_array)-1))
        if(function_type[i] == "Трапециевидная"):
            center.append(((min_t + (max_t+min_t)/2)/2+(max_t + (max_t+min_t)/2)/2)/2)
            x_array.extend((min_t,(min_t + (max_t+min_t)/2)/2,(max_t + (max_t+min_t)/2)/2,max_t))
            y_array.extend((0,1,1,0))
            boundary.append(int(len(x_array)-1))
        if(function_type[i] == "Колокообразная"):
            center.append((max_t+min_t)/2)

            x_new = np.linspace(min_t, max_t, 13)
            c = np.average(x_new)
            deviation = np.std(x_new)

            y_new = np.exp(-(np.power((x_new - c) / deviation, 2, dtype=np.float)))
            x_array.extend(x_new)
            y_array.extend(y_new)
            boundary.append(int(len(x_array)-1))
    
    for j,cit in enumerate(x_fuzzified):
        temp = x_fuzzified[j]    
        if len(point_y)==len(x_fuzzified):
            print('[Logging-Time-Lines] Correct Values')

        else:
            kj=check_points(function_type,x_array,center, boundary,temp)
            if kj is None:
                print('[Logging-Cities] Check points Error')
            point_y.append(kj)
            print(kj)
    draw_uncertainty(x_array, y_array, frame_bottom,function_type,center,boundary,'true')
    draw_uncertainty(x_array, y_array, frame_top_left,function_type,center,boundary,'false')

def check_points(type_func,maxx_x,center,boundary,temp):
    k=-1
    counter = 0
    min_x = 0
    l = 0
    for g,funca in enumerate(type_func):
        if l==0:
            min_x = 0
        else:
            min_x = maxx_x[boundary[l-1]+1]
        max_x = maxx_x[boundary[l]]
        print('[Logging-Coordinates-Check points]',max_x)
        print('[Logging-Temperature-Check points]',temp)
        if temp>min_x and temp<max_x:
            if type_func[g]=="Треугольная" and (max_x - temp) / (max_x - (max_x+min_x)/2)>0.25:
                if min_x <= temp < (max_x+min_x)/2:
                    return (temp - min_x) / ((max_x+min_x)/2 - min_x)
                if ((max_x+min_x)/2 <= temp <= max_x):
                    return (max_x - temp) / (max_x - (max_x+min_x)/2)
                return 0
            if type_func[g]=="Трапециевидная":
                a = min_x
                b = (min_x + (max_x+min_x)/2)/2
                c = (max_x + (max_x+min_x)/2)/2
                d = max_x
                if a <= temp < b:
                    return (temp - a) / (b - a)
                if b < temp < c:
                    return 1
                if c <= temp <= d:
                    return (d - temp) / (d - c)
                return 0
            if type_func[g]=="Колокообразная":
                a = min_x
                b = (min_x+max_x)/2
                return math.exp(1)**(-((temp-b)**2)/(2*a**2))
        l+=1
        
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0 or div<0:
       return "OK"
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if y==0:
        return "OK"
    return x, y

def fuzzifier():
    global date_list
    global x_fuzzified
    
    
    global longFact
    global latFact
    global qFact
    global ground_levelFact
    global maxTFact
    global minTFact
    currentMonth = datetime.now().month
    currentDay = int(datetime.now().timetuple().tm_yday)
    dayMatrix = []
     
    for i,calc in enumerate(x_original):
        print (y_original)
        print(i)
        if currentMonth >11 or currentMonth <3:
            checkMonth = "Winter"
            warmDays = int((sunset[i]-sunrise[i]-50000)/365 * latitude[i])
        if currentMonth >2 and currentMonth <6:
            checkMonth = "Spring"
            warmDays = int((sunset[i]-sunrise[i]-50000)/365 * latitude[i])
        if currentMonth >5 and currentMonth <9:
            checkMonth = "Summer"
            warmDays = int((sunset[i]-sunrise[i]-50000)/365 * latitude[i])
        if currentMonth >8 and currentMonth <12:
            checkMonth = "Autumn"
            warmDays = int((sunset[i]-sunrise[i]-50000)/365 * latitude[i])
        coldDays = 365-warmDays
        print(coldDays)
        for x in range (int(coldDays/2)):
            dayMatrix.append(-1)
        for x in range(int(coldDays/2), warmDays):
            dayMatrix.append(1)
        for x in range (warmDays,365):
            dayMatrix.append(-1)
        print(dayMatrix)
        pivot = x_original[i]
        sunFactor = 1
        if abs(latitude[i]>60) and (sunset[i]-sunrise[i]-50000)/10000 > 0.5:
            sunFactor = -1
        else:
            sunFactor = 1
        print(sunFactor)
        for j in range(analysisLength):
            

            random_number1 = randint(51, 100)/100
            random_number2 = randint(51, 100)/100
            random_number3 = randint(51, 100)/100
            random_number4 = randint(41, 100)/100
            random_number5 = randint(31, 100)/100
            random_number6 = randint(71, 100)/100
            if j==0:
                tempa=(pivot)
            tempa= tempa + ((tempa*(1/abs(longitude[i]) + 1/abs(latitude[i]) + math.cos(Q[i]) + abs(math.atan(ground_level[i]/10000))))+ dayMatrix[currentDay + j] * ((maxt[i]-mint[i])*1.25+ feels_like[i]) + sunFactor * (sunset[i] - sunrise[i] - 50000)/1000)/100
            print("!!!tempa", tempa)
            x_fuzzified.append(tempa)
            longFact.append(1/abs(longitude[i])*random_number1)
            latFact.append(1/abs(latitude[i])*random_number2)
            qFact.append(math.cos(Q[i])*random_number3)
            ground_levelFact.append(abs(math.atan(ground_level[i]/10000))*random_number4)
            maxTFact.append((maxt[i]-mint[i])*1.25+ feels_like[i]*random_number5)
            minTFact.append((maxt[i]-mint[i])*1.25+ feels_like[i]*random_number6)
            date_list.append("Day: {}, City: {}".format(currentDay+j,weathers[i]))
        dayMatrix = []
            
        
def draw_uncertainty(x_array, y_array, frame,lingv,center,boundary, with_points):
    global point_y
    global longFact
    global latFact
    global qFact
    global ground_levelFact
    global maxTFact
    global minTFact
    for widget in frame.winfo_children():
        widget.destroy()
    i=2
    title_list = []
    for k,number in enumerate(x_array):
        if (i>1) and (i<len(x_array)-2):
            A = [x_array[i-1],y_array[i-1]]
            B = [x_array[i],y_array[i]]
            C = [x_array[i+1],y_array[i+1]]
            D = [x_array[i+2],y_array[i+2]]
            if line_intersection((A,B),(C,D)) == "OK":
                print('[Logging-Intersection] Lines does not intersect')
            else:
                x_array[i], y_array[i] = line_intersection((A,B),(C,D))
                x_array[i+1], y_array[i+1] = line_intersection((A,B),(C,D))
                print('[Logging-Cities]', line_intersection((A,B),(C,D)))
                i+=2
            i+=1
    fig = plt.figure(figsize=(8, 7))
    fig.add_subplot(111).plot(x_array, y_array)
    
    for i, txt in enumerate(boundary):
        if i<len(boundary)-1:
            color = ['red', 'black', 'blue', 'brown', 'green']
            if i==0:
                plt.plot(x_array[0:boundary[i]+1], y_array[0:boundary[i]+1], color=color[i])
            else:
                plt.plot(x_array[boundary[i]+1:boundary[i+1]+1], y_array[boundary[i]+1:boundary[i+1]+1], color=color[i])
    
    y = []
    x = []
    legend = []

    print("yses,",point_y)
        
    print("xses",x_fuzzified)
    print((type(x_fuzzified)))
    
    print(longitude)
    print(latitude)
    print(Q)
    
    with open("eggz.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(longFact)
        wr.writerow(latFact)
        wr.writerow(qFact)
        wr.writerow(ground_levelFact)
        wr.writerow(maxTFact)
        wr.writerow(minTFact)
        
    for i, temp_x in enumerate(x_fuzzified):
        color = ["violet", "orange", "red", "blue", "green"] * 25
        plt.scatter(x_fuzzified[i],point_y[i], color = color[i])
        plt.annotate(date_list[i], (x_fuzzified[i],point_y[i]),fontsize=4)
    for i, txt in enumerate(lingv):
        plt.annotate(lingv[i], (center[i], 1),size = 3)
    if with_points == 'true':
        for i in range(len(point_y)):
            if (i + 1) % 3 == 0:
                mean = (point_y[i - 2] + point_y[i - 1] + point_y[i]) / 3
                y.append(mean)
            else:
                if i == (len(point_y) - 1):
                    if i % 3 == 0:
                        y.append(point_y[i])
                    else:
                        mean = (point_y[i - 1] + point_y[i]) / 2
                        y.append(mean)
        x = np.linspace(1, 35, len(y))
        plt.plot(x, y, linewidth=3)
        legend.append('trend line')
        
    canvas = FigureCanvasTkAgg(fig, frame)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    root.update()
    canvas._tkcanvas.update()
    frame.update()
    canvas._tkcanvas.pack()
    frame.pack_propagate(False)

parse_weather()
fuzzifier()
uncertainty_generator()
x_original = []
y_original = []
point_y = []
root.update()
root.mainloop()
