#!/bin/python

import datetime,subprocess
import Tkinter as tk
import requests
import json
import tkMessageBox

#-------------------------------------#

USER = "EMAIL"
PIN = "XXXX"
ENTRY_HOUR = 7
EXIT_HOUR = 15

#-------------------------------------#

def infoSuccess():
    tkMessageBox.showinfo("Success","Successful check-in.")

def error(info):
    return tkMessageBox.askretrycancel("Error during the check-in","Info: {0}".format(info))

def getToken():
    URL= 'https://newapi.intratime.es/api/user/login'
    headers = {
        'Accept': 'application/vnd.apiintratime.v1+json',
        'Content-Type': 'application/x-www-form-urlencoded; charset:utf8',
    }
    data = "user={0}&pin={1}".format(USER,PIN)
    try:
        resp = requests.post(URL , headers= headers, data=data)
    except Exception as e:
        if error("Exception number: " + type(e).__name__):
            getToken()
        else:
            root.destroy()
    else:
        if( resp.status_code == 201 ):
            try:
                return json.loads(resp.text)["USER_TOKEN"]
            except:
                if error("Error trying to get the token"):
                    getToken()
                else:
                    root.destroy()
        else:
            if error("Exception number: " + str(resp.status_code)):
                getToken()
            else:
                root.destroy()

def check(action):
    Token = getToken()
    URL= 'https://newapi.intratime.es/api/user/clocking'
    headers = {
        'Accept': 'application/vnd.apiintratime.v1+json',
        'token': '{0}'.format(Token),
    }
    data = {
        "user_action": action,
        "user_use_server_time":"true",
        "user_timestamp":"{0}".format(datetime.datetime.now().date().isoformat()),
    }
    try:
        resp = requests.post(URL , headers= headers, data=data)
        if( resp.status_code == 201 ):
            if action == 0:
                infoSuccess()
                root.destroy()
        else:
            if error("Response code: " + resp.status_code):
                check(action)
            else:
                root.destroy()
    except Exception as e:
        if error("Exception number: " + type(e).__name__):
            check(action)
        else:
            root.destroy()

def exit(root):
    root.destroy()

def center(toplevel):
    toplevel.update_idletasks()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2
    toplevel.geometry("+%d+%d" % (x, y))

if __name__ == "__main__":
    now =  datetime.datetime.now().time()
    if now > datetime.time(ENTRY_HOUR-1,45,00) and now < datetime.time(ENTRY_HOUR,30,00):
        root = tk.Tk()
        root.resizable(False,False)
        frame = tk.Frame(heigh="250",width="450").place()
        label = tk.Label(text="Do you want to check-in now?")
        label.grid(pady=(10,20),padx=20,row=0,columnspan=2)
        button_cancel = tk.Button(text="No",command=lambda:exit(root))
        button_cancel.grid(column=0,row=1,pady=(0,20))
        button_accept = tk.Button(text="Yes",command=lambda:check(0))
        button_accept.grid(column=1,row=1,pady=(0,20))
        center(root)
        root.mainloop()
    elif now > datetime.time(EXIT_HOUR-1,45,00) and now < datetime.time(EXIT_HOUR,30,00):
        root = tk.Tk()
        root.resizable(False,False)
        frame = tk.Frame(heigh="250",width="450").place()
        label = tk.Label(text="Do you want to check-off now?")
        label.grid(pady=(10,20),padx=20,row=0,columnspan=2)
        button_cancel = tk.Button(text="No",command=lambda:exit(root))
        button_cancel.grid(column=0,row=1,pady=(0,20))
        button_accept = tk.Button(text="Yes",command=lambda:check(1))
        button_accept.grid(column=1,row=1,pady=(0,20))
        center(root)
        root.mainloop()
