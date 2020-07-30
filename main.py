
# importing all the required modules

import requests

from bs4 import BeautifulSoup

import tkinter as tk

import plyer

import time

import datetime

import threading

def getting_html_data(url):  #get the required data from the website url
    data = requests.get(url)
    return data


def get_covid_19_details_of_India():
        url = "https://www.mygov.in/covid-19"
        html_data = getting_html_data(url)
        soup = BeautifulSoup(html_data.text, "html.parser")
        #with open ('html_data.txt', 'w', encoding="utf-8") as f:
        #f.write(html_data.text)
        row_div = soup.find("div",class_="information_row").find_all("div", class_="iblock")
        all_details = ""
        for block in row_div:
           # print(block)
            icount_var=block.find("span", class_="icount").get_text()
            info_var=block.find("div", class_="info_label").get_text()
            all_details += info_var + " : " + icount_var + "\n"
        return all_details


def refresh_func():  # function which will reload our data and show it on the tkinter window
    new_data = get_covid_19_details_of_India()
    print("Refreshing..............")
    banner_label['text'] = new_data



# function for notifying .......................
def notify_me():
    while True:
          plyer.notification.notify(
          title = "COVID-19 Cases of INDIA",
          message = get_covid_19_details_of_India(),
          timeout = 10,
          app_icon = "corona.ico"
          )
          time.sleep(10)


#now creating a GUI for web scraping using tkinter

root=tk.Tk()  #creating the main window
root.geometry("500x700") #setting the width and height for our gui window
root.configure(bg="black") #setting background color as 0
root.iconbitmap("corona.ico") #setting our icon for the window
root.title("COVID-19 PANDEMIC Corona Cases Tracker - INDIA") # titel of the window
font_var = ("poppins",28,"bold") #font type and size
banner = tk.PhotoImage(file="dis_img.png") #our banner image or main image
banner_label = tk.Label(root,image=banner) 
banner_label.pack()
data_label = tk.Label(root, text=get_covid_19_details_of_India(),font=font_var,bg="black",fg="white") #this will extract data from get_covid_19_details_of_India() function and will display on the gui window
data_label.pack()

refresh_button = tk.Button(root,text="REFRESH",font=font_var,relief='solid',command=refresh_func)  #creating a refresh button for refreshing the window
refresh_button.pack()

#creating a new thread so that whenever we close our gui window the notification alert will be disabled.. else notification will be poping up forever

thread_var = threading.Thread(target=notify_me) #user thread
thread_var.setDaemon(True) # setting user thread to daemon thread 
thread_var.start()


root.mainloop()  #closing the main gui loop

get_covid_19_details_of_India()