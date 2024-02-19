import tkinter as tk
import ttkbootstrap as td
from bs4 import BeautifulSoup
import requests
from tkinter import messagebox
import json
import os

root = td.Window(themename="darkly")
root.title('WebScraper')
root.geometry('500x500')

def displaySelectors():
    number_selectors = int(nr_selectors_var.get())

    # Check min and max length of selectors
    if number_selectors > 3 or number_selectors < 1:
        messagebox.showinfo(title='Warning', message='You can only chose from 1 to 3 Selectors!!')
        return
    
    # Print the Selectors that were given
    global selectors
    selectors = []
    for i in range(1, number_selectors+1):
        efl = tk.Label(root, text=f"Selectors #{i}:",)
        selectors.append(efl)
        ef = tk.Text(root, font=("Arial", 10), height=1)
        selectors.append(ef)

    for i in selectors:
        i.pack(padx=30)

    # Print the Scrape Button
    scrape_btn = td.Button(text="Scrape", bootstyle="outline-info", command=scrapeURL)
    scrape_btn.pack(pady=10)

def scrapeURL():
    # convert the url into html and parse it
    url_content = str(url.get("1.0", 'end-1c'))
    html = requests.get(url_content)
    soap = BeautifulSoup(html.text, 'html.parser')

    # select the items from the selectors and append their values into a list
    s_value = []
    for s in range(1, len(selectors), 2):
        s_value.append(selectors[s].get('1.0', 'end-1c'))
            
    # create a new list and append the previous values with the help of BeautifulSoap
    list = []
    for s in s_value:
        # check if the new list is empty
        if not list:
            # check if the selectors are image or heading or paragraph
            if "> img" in s:
                content = soap.select_one(s)['src']
                list.append({'image' : content})
            elif "> h1" in s:
                content = soap.select_one(s).text
                list.append({'heading' : content})
            else:
                content = soap.select_one(s).text
                list.append({'paragraph' : content})
        else:
            # check if the selectors are image or heading or paragraph
            if "> img" in s:
                dict = list[0]
                content = soap.select_one(s)['src']
                dict['image'] = content
            elif "> h1" in s:
                dict = list[0]
                content = soap.select_one(s).text
                dict['heading'] = content
            else:
                dict = list[0]
                content = soap.select_one(s).text
                dict['paragraph'] = content

    if os.path.isfile('./data.json'):
        # Read the Json File and convert it into an array
        with open('./data.json', 'r') as json_file:
            old_json = json.load(json_file)
        
        # Append the new posts into that array
        for i in list:
            old_json.append(i)
            
        # Convert the array into json and write the json file
        json_file = json.dumps(old_json, indent=4)
        with open('data.json', 'w') as fh:
            fh.write(json_file)
        print("Done!")
    else:
        # Convert the array into json and write the json file
        json_file = json.dumps(list, indent=4)
        with open('data.json', 'w') as fh:
            fh.write(json_file)
        print("Done!")

# Title
title = td.Label(root, text="Web Scraper", font=("Arial", 25), bootstyle="default")
title.pack(pady=25)

# Url
url_label = td.Label(root, text="Url:", font=("Arial", 14), bootstyle="info")
url_label.pack()
url = tk.Text(root, height=1, font=("Arial", 14))
url.pack(padx=30)

# Selectors
nr_selectors_label = td.Label(root, text="Selectors:", font=("Arial", 14), bootstyle="success")
nr_selectors_label.pack(pady=20)

nr_selectors_var = tk.StringVar()
nr_selectors = tk.Entry(root, font=("Arial", 14), textvariable=nr_selectors_var)
nr_selectors.pack()

write_btn = td.Button(root, text='Write Selectors', bootstyle=('outline-success'), command=displaySelectors)
write_btn.pack(pady=10)

root.mainloop()