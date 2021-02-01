#!/usr/bin/env python3

import os
import sys
import time
from tkinter import *
import tkinter as tk                     
from tkinter import ttk 
from kvmIPDefs import *
from kvmLocDefs import *

program = "SPIDER KVM MANAGER"
# Created by davidc.
version = "1" 
release = "9/15/20"

# Main window, menu bar, and tab declaration.
view = tk.Tk() 
view.title("IMH SPIDER KVM MANAGER") 
view.geometry("500x320")
optionsMenu = Menu(view)
view.config(menu=optionsMenu)
tabControl = ttk.Notebook(view) 


# Ping all KVM's in terminal.
def checkStatusAll():
 os.system("./pingAllKVM.sh")


# The About window.
def about():
 aboutView = Tk()
 aboutView.title('About Spider Man')
 aboutView.geometry("300x90")
 #add frame.
 aboutFrame = LabelFrame(aboutView, text="", padx=5, pady=5)
 aboutFrame.grid(padx=10, pady=10)

 programTitle = Label(aboutFrame, text=program).pack()
 versionTitle = Label(aboutFrame, text="VERSION: " + version).pack()
 releaseTitle = Label(aboutFrame, text="RELEASE: " + release).pack()


# Menu bar creation.
option = Menu(optionsMenu)
optionsMenu.add_cascade(label="Option", menu=option)
option.add_command(label="Check Status All In Terminal", command=checkStatusAll)
option.add_command(label="About", command=about)
option.add_separator()
option.add_command(label="Exit", command=view.quit)

# Tab creation for KVM's. 
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl) 
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl) 
tab6 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='KVMs: 1-8') 
tabControl.add(tab2, text ='KVMs: 9-16')
tabControl.add(tab3, text ='KVMs: 17-24') 
tabControl.add(tab4, text ='KVMs: 25-32')
tabControl.add(tab5, text ='KVMs: 33-40') 
tabControl.add(tab6, text ='KVMs: 41-48') 
tabControl.pack(expand = 1, fill ="both") 

# Global variables for device entries.
global thisKVM, newIPEntry, newLocationEntry, ipStatus, kvmStatus
ipStatus = ""


# Function to edit devices in IP and Device files.
def fixEntries(thisKVM, newIP, newLocation):
 
 python = sys.executable
 thisKVM = int(thisKVM)
 catKVM = str(thisKVM)
 newIP = newIP.get()
 newLocation = newLocation.get()
 ipEntryStrLen = len(newIP)
 locEntryStrLen = len(newLocation)

 if ipEntryStrLen == 0:
  pass
 else:
  a_file = open("kvmIPDefs.py", "r")
  ipUpdate = a_file.readlines()
  ipUpdate[thisKVM] = "kvm" + catKVM + "IP = \'" + newIP + "\'\n"

  a_file = open("kvmIPDefs.py", "w")
  a_file.writelines(ipUpdate)
  a_file.close()

 if locEntryStrLen == 0:
  pass
 else:
  a_file = open("kvmLocDefs.py", "r")
  locUpdate = a_file.readlines()
  locUpdate[thisKVM] = "kvm" + catKVM + "Loc = \'" + newLocation + "\'\n"

  a_file = open("kvmLocDefs.py", "w")
  a_file.writelines(locUpdate)
  a_file.close()
 
 editor.destroy()
 os.execl(python, python, * sys.argv)


# Device edit menu.
def editKVM(thisKVM):
 global editor
 editor = Tk()
 editor.title('Edit KVM' + thisKVM)
 editor.geometry("200x150")
 
 newIPEntry = StringVar()
 newLocationEntry = StringVar()

 frame = LabelFrame(editor, text="", padx=5, pady=5)
 frame.grid(padx=10, pady=10)
 
 newIPLabel = Label(frame, text="NEW IP", font=("Times", 12, "bold")).grid(row=0, column=0, columnspan=2)
 newIP = Entry(frame, textvariable="")
 newIP.grid(row=1, column=0, columnspan=2)
 
 newLocationLabel = Label(frame, text="NEW LOCATION", font=("Times", 12, "bold")).grid(row=2, column=0, columnspan=2)
 newLocation = Entry(frame, textvariable="")
 newLocation.grid(row=3, column=0, columnspan=2)

 editButton = Button(frame, text="EDIT", font=("Times", 12), padx=1, command=lambda: fixEntries(thisKVM, newIP, newLocation))
 editButton.grid(row=4, column=0, columnspan=4, ipadx=30)


# IP button press function.
def webIface(self):
 kvmIP = self
 os.system('firefox ' + kvmIP)


# KVM device state.
def kvmPingState(self, kvmStatus):
 pingThis = self
 ipStatus = os.popen("ping -c 1 " + pingThis + " | grep -o \"Destination Host Unreachable\" > noOutput && printf \"DOWN\" || printf \"UP\"").read()
 os.popen("true > noOutput").read()
 kvmStatus.set(ipStatus)


# TAB 1: ('KVMs: 1-8')  
kvmNameTab1Label = Label(tab1, text="KVM NAME", font=("Times", 14, "bold")).grid(row=1, column=0, padx=2, pady=2)
ipAddressTab1Label = Label(tab1, text="IP ADDRESS", font=("Times", 14, "bold")).grid(row=1, column=1, padx=5, pady=2)
locationTab1Label = Label(tab1, text="LOCATION", font=("Times", 14, "bold")).grid(row=1, column=2, padx=5, pady=2)
statusTab1Label = Label(tab1, text="STATUS", font=("Times", 14, "bold")).grid(row=1, column=3, padx=10, pady=2)

kvm1NameButton = Button(tab1, text="KVM1", font=("Times", 12), padx=30, command=lambda: editKVM("1")).grid(row=2, column=0)
kvm1IPButton = Button(tab1, text=kvm1IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm1IP)).grid(row=2, column=1)
kvm1LocationLabel = Label(tab1, text=kvm1Loc, font=("Times", 12)).grid(row=2, column=2)
kvm1Status = StringVar()
kvm1StatusButton = Button(tab1, textvariable=kvm1Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm1IP, kvm1Status))
kvm1Status.set("CHECK")
kvm1StatusButton.grid(row=2, column=3)

kvm2NameButton = Button(tab1, text="KVM2", font=("Times", 12), padx=30, command=lambda: editKVM("2")).grid(row=3, column=0)
kvm2IPButton = Button(tab1, text=kvm2IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm2IP)).grid(row=3, column=1)
kvm2LocationLabel = Label(tab1, text=kvm2Loc, font=("Times", 12)).grid(row=3, column=2)
kvm2Status = StringVar()
kvm2StatusButton = Button(tab1, textvariable=kvm2Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm2IP, kvm2Status))
kvm2Status.set("CHECK")
kvm2StatusButton.grid(row=3, column=3)

kvm3NameButton = Button(tab1, text="KVM3", font=("Times", 12), padx=30, command=lambda: editKVM("3")).grid(row=4, column=0)
kvm3IPButton = Button(tab1, text=kvm3IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm3IP)).grid(row=4, column=1)
kvm3LocationLabel = Label(tab1, text=kvm3Loc, font=("Times", 12)).grid(row=4, column=2)
kvm3Status = StringVar()
kvm3StatusButton = Button(tab1, textvariable=kvm3Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm3IP, kvm3Status))
kvm3Status.set("CHECK")
kvm3StatusButton.grid(row=4, column=3)

kvm4NameButton = Button(tab1, text="KVM4", font=("Times", 12), padx=30, command=lambda: editKVM("4")).grid(row=5, column=0)
kvm4IPButton = Button(tab1, text=kvm4IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm4IP)).grid(row=5, column=1)
kvm4LocationLabel = Label(tab1, text=kvm4Loc, font=("Times", 12)).grid(row=5, column=2)
kvm4Status = StringVar()
kvm4StatusButton = Button(tab1, textvariable=kvm4Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm4IP, kvm4Status))
kvm4Status.set("CHECK")
kvm4StatusButton.grid(row=5, column=3)

kvm5NameButton = Button(tab1, text="KVM5", font=("Times", 12), padx=30, command=lambda: editKVM("5")).grid(row=6, column=0)
kvm5IPButton = Button(tab1, text=kvm5IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm5IP)).grid(row=6, column=1)
kvm5LocationLabel = Label(tab1, text=kvm5Loc, font=("Times", 12)).grid(row=6, column=2)
kvm5Status = StringVar()
kvm5StatusButton = Button(tab1, textvariable=kvm5Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm5IP, kvm5Status))
kvm5Status.set("CHECK")
kvm5StatusButton.grid(row=6, column=3)

kvm6NameButton = Button(tab1, text="KVM6", font=("Times", 12), padx=30, command=lambda: editKVM("6")).grid(row=7, column=0)
kvm6IPButton = Button(tab1, text=kvm6IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm6IP)).grid(row=7, column=1)
kvm6LocationLabel = Label(tab1, text=kvm6Loc, font=("Times", 12)).grid(row=7, column=2)
kvm6Status = StringVar()
kvm6StatusButton = Button(tab1, textvariable=kvm6Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm6IP, kvm6Status))
kvm6Status.set("CHECK")
kvm6StatusButton.grid(row=7, column=3)

kvm7NameButton = Button(tab1, text="KVM7", font=("Times", 12), padx=30, command=lambda: editKVM("7")).grid(row=8, column=0)
kvm7IPButton = Button(tab1, text=kvm7IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm7IP)).grid(row=8, column=1)
kvm7LocationLabel = Label(tab1, text=kvm7Loc, font=("Times", 12)).grid(row=8, column=2)
kvm7Status = StringVar()
kvm7StatusButton = Button(tab1, textvariable=kvm7Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm7IP, kvm7Status))
kvm7Status.set("CHECK")
kvm7StatusButton.grid(row=8, column=3)

kvm8NameButton = Button(tab1, text="KVM8", font=("Times", 12), padx=30, command=lambda: editKVM("8")).grid(row=9, column=0)
kvm8IPButton = Button(tab1, text=kvm8IP, font=("Times", 12), padx=5, command=lambda: webIface(kvm8IP)).grid(row=9, column=1)
kvm8LocationLabel = Label(tab1, text=kvm8Loc, font=("Times", 12)).grid(row=9, column=2)
kvm8Status = StringVar()
kvm8StatusButton = Button(tab1, textvariable=kvm8Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm8IP, kvm8Status))
kvm8Status.set("CHECK")
kvm8StatusButton.grid(row=9, column=3)


# TAB 2: ('KVMs: 9-16')  
tabControl.pack(expand = 1, fill ="both") 
kvmNameTab2Label = Label(tab2, text="KVM NAME", font=("Times", 14, "bold")).grid(row=1, column=0, padx=2, pady=2)
ipAddressTab2Label = Label(tab2, text="IP ADDRESS", font=("Times", 14, "bold")).grid(row=1, column=1, padx=5, pady=2)
locationTab2Label = Label(tab2, text="LOCATION", font=("Times", 14, "bold")).grid(row=1, column=2, padx=5, pady=2)
statusTab2Label = Label(tab2, text="STATUS", font=("Times", 14, "bold")).grid(row=1, column=3, padx=10, pady=2)

kvm9NameButton = Button(tab2, text="KVM9", font=("Times", 12), padx=30, command=lambda: editKVM("9")).grid(row=2, column=0)
kvm9IPButton = Button(tab2, text=kvm9IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm9IP)).grid(row=2, column=1)
kvm9LocationLabel = Label(tab2, text=kvm9Loc, font=("Times", 12)).grid(row=2, column=2)
kvm9Status = StringVar()
kvm9StatusButton = Button(tab2, textvariable=kvm9Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm9IP, kvm9Status))
kvm9Status.set("CHECK")
kvm9StatusButton.grid(row=2, column=3)

kvm10NameButton = Button(tab2, text="KVM10", font=("Times", 12), padx=30, command=lambda: editKVM("10")).grid(row=3, column=0)
kvm10IPButton = Button(tab2, text=kvm10IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm10IP)).grid(row=3, column=1)
kvm10LocationLabel = Label(tab2, text=kvm10Loc, font=("Times", 12)).grid(row=3, column=2)
kvm10Status = StringVar()
kvm10StatusButton = Button(tab2, textvariable=kvm10Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm10IP, kvm10Status))
kvm10Status.set("CHECK")
kvm10StatusButton.grid(row=3, column=3)

kvm11NameButton = Button(tab2, text="KVM11", font=("Times", 12), padx=30, command=lambda: editKVM("11")).grid(row=4, column=0)
kvm11IPButton = Button(tab2, text=kvm11IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm11IP)).grid(row=4, column=1)
kvm11LocationLabel = Label(tab2, text=kvm11Loc, font=("Times", 12)).grid(row=4, column=2)
kvm11Status = StringVar()
kvm11StatusButton = Button(tab2, textvariable=kvm11Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm11IP, kvm11Status))
kvm11Status.set("CHECK")
kvm11StatusButton.grid(row=4, column=3)

kvm12NameButton = Button(tab2, text="KVM12", font=("Times", 12), padx=30, command=lambda: editKVM("12")).grid(row=5, column=0)
kvm12IPButton = Button(tab2, text=kvm12IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm12IP)).grid(row=5, column=1)
kvm12LocationLabel = Label(tab2, text=kvm12Loc, font=("Times", 12)).grid(row=5, column=2)
kvm12Status = StringVar()
kvm12StatusButton = Button(tab2, textvariable=kvm12Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm12IP, kvm12Status))
kvm12Status.set("CHECK")
kvm12StatusButton.grid(row=5, column=3)

kvm13NameButton = Button(tab2, text="KVM13", font=("Times", 12), padx=30, command=lambda: editKVM("13")).grid(row=6, column=0)
kvm13IPButton = Button(tab2, text=kvm13IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm13IP)).grid(row=6, column=1)
kvm13LocationLabel = Label(tab2, text=kvm5Loc, font=("Times", 12)).grid(row=6, column=2)
kvm13Status = StringVar()
kvm13StatusButton = Button(tab2, textvariable=kvm13Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm13IP, kvm13Status))
kvm13Status.set("CHECK")
kvm13StatusButton.grid(row=6, column=3)

kvm14NameButton = Button(tab2, text="KVM14", font=("Times", 12), padx=30, command=lambda: editKVM("14")).grid(row=7, column=0)
kvm14IPButton = Button(tab2, text=kvm14IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm14IP)).grid(row=7, column=1)
kvm14LocationLabel = Label(tab2, text=kvm14Loc, font=("Times", 12)).grid(row=7, column=2)
kvm14Status = StringVar()
kvm14StatusButton = Button(tab2, textvariable=kvm14Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm14IP, kvm14Status))
kvm14Status.set("CHECK")
kvm14StatusButton.grid(row=7, column=3)

kvm15NameButton = Button(tab2, text="KVM15", font=("Times", 12), padx=30, command=lambda: editKVM("15")).grid(row=8, column=0)
kvm15IPButton = Button(tab2, text=kvm15IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm15IP)).grid(row=8, column=1)
kvm15LocationLabel = Label(tab2, text=kvm15Loc, font=("Times", 12)).grid(row=8, column=2)
kvm15Status = StringVar()
kvm15StatusButton = Button(tab2, textvariable=kvm15Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm15IP, kvm15Status))
kvm15Status.set("CHECK")
kvm15StatusButton.grid(row=8, column=3)

kvm16NameButton = Button(tab2, text="KVM16", font=("Times", 12), padx=30, command=lambda: editKVM("16")).grid(row=9, column=0)
kvm16IPButton = Button(tab2, text=kvm16IP, font=("Times", 12), padx=5, command=lambda: webIface(kvm16IP)).grid(row=9, column=1)
kvm16LocationLabel = Label(tab2, text=kvm16Loc, font=("Times", 12)).grid(row=9, column=2)
kvm16Status = StringVar()
kvm16StatusButton = Button(tab2, textvariable=kvm16Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm16IP, kvm16Status))
kvm16Status.set("CHECK")
kvm16StatusButton.grid(row=9, column=3)


# TAB 3: ('KVMs: 17-24')
kvmNameTab3Label = Label(tab3, text="KVM NAME", font=("Times", 14, "bold")).grid(row=1, column=0, padx=2, pady=2)
ipAddressTab3Label = Label(tab3, text="IP ADDRESS", font=("Times", 14, "bold")).grid(row=1, column=1, padx=5, pady=2)
locationTab3Label = Label(tab3, text="LOCATION", font=("Times", 14, "bold")).grid(row=1, column=2, padx=5, pady=2)
statusTab3Label = Label(tab3, text="STATUS", font=("Times", 14, "bold")).grid(row=1, column=3, padx=10, pady=2)

kvm17NameButton = Button(tab3, text="KVM17", font=("Times", 12), padx=30, command=lambda: editKVM("17")).grid(row=2, column=0)
kvm17IPButton = Button(tab3, text=kvm17IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm17IP)).grid(row=2, column=1)
kvm17LocationLabel = Label(tab3, text=kvm17Loc, font=("Times", 12)).grid(row=2, column=2)
kvm17Status = StringVar()
kvm17StatusButton = Button(tab3, textvariable=kvm17Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm17IP, kvm17Status))
kvm17Status.set("CHECK")
kvm17StatusButton.grid(row=2, column=3)

kvm18NameButton = Button(tab3, text="KVM18", font=("Times", 12), padx=30, command=lambda: editKVM("18")).grid(row=3, column=0)
kvm18IPButton = Button(tab3, text=kvm18IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm18IP)).grid(row=3, column=1)
kvm18LocationLabel = Label(tab3, text=kvm18Loc, font=("Times", 12)).grid(row=3, column=2)
kvm18Status = StringVar()
kvm18StatusButton = Button(tab3, textvariable=kvm18Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm18IP, kvm18Status))
kvm18Status.set("CHECK")
kvm18StatusButton.grid(row=3, column=3)

kvm19NameButton = Button(tab3, text="KVM19", font=("Times", 12), padx=30, command=lambda: editKVM("19")).grid(row=4, column=0)
kvm19IPButton = Button(tab3, text=kvm19IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm19IP)).grid(row=4, column=1)
kvm19LocationLabel = Label(tab3, text=kvm19Loc, font=("Times", 12)).grid(row=4, column=2)
kvm19Status = StringVar()
kvm19StatusButton = Button(tab3, textvariable=kvm19Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm19IP, kvm19Status))
kvm19Status.set("CHECK")
kvm19StatusButton.grid(row=4, column=3)

kvm20NameButton = Button(tab3, text="KVM20", font=("Times", 12), padx=30, command=lambda: editKVM("20")).grid(row=5, column=0)
kvm20IPButton = Button(tab3, text=kvm20IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm20IP)).grid(row=5, column=1)
kvm20LocationLabel = Label(tab3, text=kvm20Loc, font=("Times", 12)).grid(row=5, column=2)
kvm20Status = StringVar()
kvm20StatusButton = Button(tab3, textvariable=kvm20Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm20IP, kvm20Status))
kvm20Status.set("CHECK")
kvm20StatusButton.grid(row=5, column=3)

kvm21NameButton = Button(tab3, text="KVM21", font=("Times", 12), padx=30, command=lambda: editKVM("21")).grid(row=6, column=0)
kvm21IPButton = Button(tab3, text=kvm21IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm21IP)).grid(row=6, column=1)
kvm21LocationLabel = Label(tab3, text=kvm21Loc, font=("Times", 12)).grid(row=6, column=2)
kvm21Status = StringVar()
kvm21StatusButton = Button(tab3, textvariable=kvm21Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm21IP, kvm21Status))
kvm21Status.set("CHECK")
kvm21StatusButton.grid(row=6, column=3)

kvm22NameButton = Button(tab3, text="KVM22", font=("Times", 12), padx=30, command=lambda: editKVM("22")).grid(row=7, column=0)
kvm22IPButton = Button(tab3, text=kvm22IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm22IP)).grid(row=7, column=1)
kvm22LocationLabel = Label(tab3, text=kvm22Loc, font=("Times", 12)).grid(row=7, column=2)
kvm22Status = StringVar()
kvm22StatusButton = Button(tab3, textvariable=kvm22Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm22IP, kvm22Status))
kvm22Status.set("CHECK")
kvm22StatusButton.grid(row=7, column=3)

kvm23NameButton = Button(tab3, text="KVM23", font=("Times", 12), padx=30, command=lambda: editKVM("23")).grid(row=8, column=0)
kvm23IPButton = Button(tab3, text=kvm23IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm23IP)).grid(row=8, column=1)
kvm23LocationLabel = Label(tab3, text=kvm23Loc, font=("Times", 12)).grid(row=8, column=2)
kvm23Status = StringVar()
kvm23StatusButton = Button(tab3, textvariable=kvm23Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm23IP, kvm23Status))
kvm23Status.set("CHECK")
kvm23StatusButton.grid(row=8, column=3)

kvm24NameButton = Button(tab3, text="KVM24", font=("Times", 12), padx=30, command=lambda: editKVM("24")).grid(row=9, column=0)
kvm24IPButton = Button(tab3, text=kvm24IP, font=("Times", 12), padx=5, command=lambda: webIface(kvm24IP)).grid(row=9, column=1)
kvm24LocationLabel = Label(tab3, text=kvm24Loc, font=("Times", 12)).grid(row=9, column=2)
kvm24Status = StringVar()
kvm24StatusButton = Button(tab3, textvariable=kvm16Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm24IP, kvm24Status))
kvm24Status.set("CHECK")
kvm24StatusButton.grid(row=9, column=3)


# TAB 4: ('KVMs: 25-32')
kvmNameTab4Label = Label(tab4, text="KVM NAME", font=("Times", 14, "bold")).grid(row=1, column=0, padx=2, pady=2)
ipAddressTab4Label = Label(tab4, text="IP ADDRESS", font=("Times", 14, "bold")).grid(row=1, column=1, padx=5, pady=2)
locationTab4Label = Label(tab4, text="LOCATION", font=("Times", 14, "bold")).grid(row=1, column=2, padx=5, pady=2)
statusTab4Label = Label(tab4, text="STATUS", font=("Times", 14, "bold")).grid(row=1, column=3, padx=10, pady=2)

kvm25NameButton = Button(tab4, text="KVM25", font=("Times", 12), padx=30, command=lambda: editKVM("25")).grid(row=2, column=0)
kvm25IPButton = Button(tab4, text=kvm25IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm25IP)).grid(row=2, column=1)
kvm25LocationLabel = Label(tab4, text=kvm25Loc, font=("Times", 12)).grid(row=2, column=2)
kvm25Status = StringVar()
kvm25StatusButton = Button(tab4, textvariable=kvm25Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm25IP, kvm25Status))
kvm25Status.set("CHECK")
kvm25StatusButton.grid(row=2, column=3)

kvm26NameButton = Button(tab4, text="KVM26", font=("Times", 12), padx=30, command=lambda: editKVM("26")).grid(row=3, column=0)
kvm26IPButton = Button(tab4, text=kvm26IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm26IP)).grid(row=3, column=1)
kvm26LocationLabel = Label(tab4, text=kvm26Loc, font=("Times", 12)).grid(row=3, column=2)
kvm26Status = StringVar()
kvm26StatusButton = Button(tab4, textvariable=kvm26Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm26IP, kvm26Status))
kvm26Status.set("CHECK")
kvm26StatusButton.grid(row=3, column=3)

kvm27NameButton = Button(tab4, text="KVM27", font=("Times", 12), padx=30, command=lambda: editKVM("27")).grid(row=4, column=0)
kvm27IPButton = Button(tab4, text=kvm27IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm27IP)).grid(row=4, column=1)
kvm27LocationLabel = Label(tab4, text=kvm27Loc, font=("Times", 12)).grid(row=4, column=2)
kvm27Status = StringVar()
kvm27StatusButton = Button(tab4, textvariable=kvm27Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm27IP, kvm27Status))
kvm27Status.set("CHECK")
kvm27StatusButton.grid(row=4, column=3)

kvm28NameButton = Button(tab4, text="KVM28", font=("Times", 12), padx=30, command=lambda: editKVM("28")).grid(row=5, column=0)
kvm28IPButton = Button(tab4, text=kvm28IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm28IP)).grid(row=5, column=1)
kvm28LocationLabel = Label(tab4, text=kvm28Loc, font=("Times", 12)).grid(row=5, column=2)
kvm28Status = StringVar()
kvm28StatusButton = Button(tab4, textvariable=kvm28Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm28IP, kvm28Status))
kvm28Status.set("CHECK")
kvm28StatusButton.grid(row=5, column=3)

kvm29NameButton = Button(tab4, text="KVM29", font=("Times", 12), padx=30, command=lambda: editKVM("29")).grid(row=6, column=0)
kvm29IPButton = Button(tab4, text=kvm29IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm29IP)).grid(row=6, column=1)
kvm29LocationLabel = Label(tab4, text=kvm29Loc, font=("Times", 12)).grid(row=6, column=2)
kvm29Status = StringVar()
kvm29StatusButton = Button(tab4, textvariable=kvm29Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm29IP, kvm29Status))
kvm29Status.set("CHECK")
kvm29StatusButton.grid(row=6, column=3)

kvm30NameButton = Button(tab4, text="KVM30", font=("Times", 12), padx=30, command=lambda: editKVM("30")).grid(row=7, column=0)
kvm30IPButton = Button(tab4, text=kvm30IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm30IP)).grid(row=7, column=1)
kvm30LocationLabel = Label(tab4, text=kvm30Loc, font=("Times", 12)).grid(row=7, column=2)
kvm30Status = StringVar()
kvm30StatusButton = Button(tab4, textvariable=kvm30Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm30IP, kvm30Status))
kvm30Status.set("CHECK")
kvm30StatusButton.grid(row=7, column=3)

kvm31NameButton = Button(tab4, text="KVM31", font=("Times", 12), padx=30, command=lambda: editKVM("31")).grid(row=8, column=0)
kvm31IPButton = Button(tab4, text=kvm31IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm31IP)).grid(row=8, column=1)
kvm31LocationLabel = Label(tab4, text=kvm31Loc, font=("Times", 12)).grid(row=8, column=2)
kvm31Status = StringVar()
kvm31StatusButton = Button(tab4, textvariable=kvm31Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm31IP, kvm31Status))
kvm31Status.set("CHECK")
kvm31StatusButton.grid(row=8, column=3)

kvm32NameButton = Button(tab4, text="KVM32", font=("Times", 12), padx=30, command=lambda: editKVM("32")).grid(row=9, column=0)
kvm32IPButton = Button(tab4, text=kvm32IP, font=("Times", 12), padx=5, command=lambda: webIface(kvm32IP)).grid(row=9, column=1)
kvm32LocationLabel = Label(tab4, text=kvm32Loc, font=("Times", 12)).grid(row=9, column=2)
kvm32Status = StringVar()
kvm32StatusButton = Button(tab4, textvariable=kvm32Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm32IP, kvm32Status))
kvm32Status.set("CHECK")
kvm32StatusButton.grid(row=9, column=3)


# TAB 5: ('KVMs: 33-40')
kvmNameTab5Label = Label(tab5, text="KVM NAME", font=("Times", 14, "bold")).grid(row=1, column=0, padx=2, pady=2)
ipAddressTab5Label = Label(tab5, text="IP ADDRESS", font=("Times", 14, "bold")).grid(row=1, column=1, padx=5, pady=2)
locationTab5Label = Label(tab5, text="LOCATION", font=("Times", 14, "bold")).grid(row=1, column=2, padx=5, pady=2)
statusTab5Label = Label(tab5, text="STATUS", font=("Times", 14, "bold")).grid(row=1, column=3, padx=10, pady=2)

kvm33NameButton = Button(tab5, text="KVM33", font=("Times", 12), padx=30, command=lambda: editKVM("33")).grid(row=2, column=0)
kvm33IPButton = Button(tab5, text=kvm33IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm33IP)).grid(row=2, column=1)
kvm33LocationLabel = Label(tab5, text=kvm33Loc, font=("Times", 12)).grid(row=2, column=2)
kvm33Status = StringVar()
kvm33StatusButton = Button(tab5, textvariable=kvm33Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm33IP, kvm33Status))
kvm33Status.set("CHECK")
kvm33StatusButton.grid(row=2, column=3)

kvm34NameButton = Button(tab5, text="KVM34", font=("Times", 12), padx=30, command=lambda: editKVM("34")).grid(row=3, column=0)
kvm34IPButton = Button(tab5, text=kvm34IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm34IP)).grid(row=3, column=1)
kvm34LocationLabel = Label(tab5, text=kvm34Loc, font=("Times", 12)).grid(row=3, column=2)
kvm34Status = StringVar()
kvm34StatusButton = Button(tab5, textvariable=kvm34Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm34IP, kvm34Status))
kvm34Status.set("CHECK")
kvm34StatusButton.grid(row=3, column=3)

kvm35NameButton = Button(tab5, text="KVM35", font=("Times", 12), padx=30, command=lambda: editKVM("35")).grid(row=4, column=0)
kvm35IPButton = Button(tab5, text=kvm35IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm35IP)).grid(row=4, column=1)
kvm35LocationLabel = Label(tab5, text=kvm35Loc, font=("Times", 12)).grid(row=4, column=2)
kvm35Status = StringVar()
kvm35StatusButton = Button(tab5, textvariable=kvm35Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm35IP, kvm35Status))
kvm35Status.set("CHECK")
kvm35StatusButton.grid(row=4, column=3)

kvm36NameButton = Button(tab5, text="KVM36", font=("Times", 12), padx=30, command=lambda: editKVM("36")).grid(row=5, column=0)
kvm36IPButton = Button(tab5, text=kvm36IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm36IP)).grid(row=5, column=1)
kvm36LocationLabel = Label(tab5, text=kvm36Loc, font=("Times", 12)).grid(row=5, column=2)
kvm36Status = StringVar()
kvm36StatusButton = Button(tab5, textvariable=kvm36Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm36IP, kvm36Status))
kvm36Status.set("CHECK")
kvm36StatusButton.grid(row=5, column=3)

kvm37NameButton = Button(tab5, text="KVM37", font=("Times", 12), padx=30, command=lambda: editKVM("37")).grid(row=6, column=0)
kvm37IPButton = Button(tab5, text=kvm37IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm37IP)).grid(row=6, column=1)
kvm37LocationLabel = Label(tab5, text=kvm37Loc, font=("Times", 12)).grid(row=6, column=2)
kvm37Status = StringVar()
kvm37StatusButton = Button(tab5, textvariable=kvm37Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm37IP, kvm37Status))
kvm37Status.set("CHECK")
kvm37StatusButton.grid(row=6, column=3)

kvm38NameButton = Button(tab5, text="KVM38", font=("Times", 12), padx=30, command=lambda: editKVM("38")).grid(row=7, column=0)
kvm38IPButton = Button(tab5, text=kvm38IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm38IP)).grid(row=7, column=1)
kvm38LocationLabel = Label(tab5, text=kvm38Loc, font=("Times", 12)).grid(row=7, column=2)
kvm38Status = StringVar()
kvm38StatusButton = Button(tab5, textvariable=kvm38Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm38IP, kvm38Status))
kvm38Status.set("CHECK")
kvm38StatusButton.grid(row=7, column=3)

kvm39NameButton = Button(tab5, text="KVM39", font=("Times", 12), padx=30, command=lambda: editKVM("39")).grid(row=8, column=0)
kvm39IPButton = Button(tab5, text=kvm39IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm39IP)).grid(row=8, column=1)
kvm39LocationLabel = Label(tab5, text=kvm39Loc, font=("Times", 12)).grid(row=8, column=2)
kvm39Status = StringVar()
kvm39StatusButton = Button(tab5, textvariable=kvm39Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm39IP, kvm39Status))
kvm39Status.set("CHECK")
kvm39StatusButton.grid(row=8, column=3)

kvm40NameButton = Button(tab5, text="KVM40", font=("Times", 12), padx=30, command=lambda: editKVM("40")).grid(row=9, column=0)
kvm40IPButton = Button(tab5, text=kvm40IP, font=("Times", 12), padx=5, command=lambda: webIface(kvm40IP)).grid(row=9, column=1)
kvm40LocationLabel = Label(tab5, text=kvm40Loc, font=("Times", 12)).grid(row=9, column=2)
kvm40Status = StringVar()
kvm40StatusButton = Button(tab5, textvariable=kvm40Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm40IP, kvm40Status))
kvm40Status.set("CHECK")
kvm40StatusButton.grid(row=9, column=3)


# TAB 6: ('KVMs: 41-48')
kvmNameTab6Label = Label(tab6, text="KVM NAME", font=("Times", 14, "bold")).grid(row=1, column=0, padx=2, pady=2)
ipAddressTab6Label = Label(tab6, text="IP ADDRESS", font=("Times", 14, "bold")).grid(row=1, column=1, padx=5, pady=2)
locationTab6Label = Label(tab6, text="LOCATION", font=("Times", 14, "bold")).grid(row=1, column=2, padx=5, pady=2)
statusTab6Label = Label(tab6, text="STATUS", font=("Times", 14, "bold")).grid(row=1, column=3, padx=10, pady=2)

kvm41NameButton = Button(tab6, text="KVM41", font=("Times", 12), padx=30, command=lambda: editKVM("41")).grid(row=2, column=0)
kvm41IPButton = Button(tab6, text=kvm41IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm41IP)).grid(row=2, column=1)
kvm41LocationLabel = Label(tab6, text=kvm41Loc, font=("Times", 12)).grid(row=2, column=2)
kvm41Status = StringVar()
kvm41StatusButton = Button(tab6, textvariable=kvm41Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm41IP, kvm41Status))
kvm41Status.set("CHECK")
kvm41StatusButton.grid(row=2, column=3)

kvm42NameButton = Button(tab6, text="KVM42", font=("Times", 12), padx=30, command=lambda: editKVM("42")).grid(row=3, column=0)
kvm42IPButton = Button(tab6, text=kvm42IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm42IP)).grid(row=3, column=1)
kvm42LocationLabel = Label(tab6, text=kvm42Loc, font=("Times", 12)).grid(row=3, column=2)
kvm42Status = StringVar()
kvm42StatusButton = Button(tab6, textvariable=kvm42Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm42IP, kvm42Status))
kvm42Status.set("CHECK")
kvm42StatusButton.grid(row=3, column=3)

kvm43NameButton = Button(tab6, text="KVM43", font=("Times", 12), padx=30, command=lambda: editKVM("43")).grid(row=4, column=0)
kvm43IPButton = Button(tab6, text=kvm43IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm43IP)).grid(row=4, column=1)
kvm43LocationLabel = Label(tab6, text=kvm43Loc, font=("Times", 12)).grid(row=4, column=2)
kvm43Status = StringVar()
kvm43StatusButton = Button(tab6, textvariable=kvm43Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm43IP, kvm43Status))
kvm43Status.set("CHECK")
kvm43StatusButton.grid(row=4, column=3)

kvm44NameButton = Button(tab6, text="KVM44", font=("Times", 12), padx=30, command=lambda: editKVM("44")).grid(row=5, column=0)
kvm44IPButton = Button(tab6, text=kvm44IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm44IP)).grid(row=5, column=1)
kvm44LocationLabel = Label(tab6, text=kvm44Loc, font=("Times", 12)).grid(row=5, column=2)
kvm44Status = StringVar()
kvm44StatusButton = Button(tab6, textvariable=kvm44Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm44IP, kvm44Status))
kvm44Status.set("CHECK")
kvm44StatusButton.grid(row=5, column=3)

kvm45NameButton = Button(tab6, text="KVM45", font=("Times", 12), padx=30, command=lambda: editKVM("45")).grid(row=6, column=0)
kvm45IPButton = Button(tab6, text=kvm45IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm45IP)).grid(row=6, column=1)
kvm45LocationLabel = Label(tab6, text=kvm45Loc, font=("Times", 12)).grid(row=6, column=2)
kvm45Status = StringVar()
kvm45StatusButton = Button(tab6, textvariable=kvm45Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm45IP, kvm45Status))
kvm45Status.set("CHECK")
kvm45StatusButton.grid(row=6, column=3)

kvm46NameButton = Button(tab6, text="KVM46", font=("Times", 12), padx=30, command=lambda: editKVM("46")).grid(row=7, column=0)
kvm46IPButton = Button(tab6, text=kvm46IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm46IP)).grid(row=7, column=1)
kvm46LocationLabel = Label(tab6, text=kvm46Loc, font=("Times", 12)).grid(row=7, column=2)
kvm46Status = StringVar()
kvm46StatusButton = Button(tab6, textvariable=kvm46Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm46IP, kvm46Status))
kvm46Status.set("CHECK")
kvm46StatusButton.grid(row=7, column=3)

kvm47NameButton = Button(tab6, text="KVM47", font=("Times", 12), padx=30, command=lambda: editKVM("47")).grid(row=8, column=0)
kvm47IPButton = Button(tab6, text=kvm47IP, font=("Times", 12), padx=1, command=lambda: webIface(kvm47IP)).grid(row=8, column=1)
kvm47LocationLabel = Label(tab6, text=kvm47Loc, font=("Times", 12)).grid(row=8, column=2)
kvm47Status = StringVar()
kvm47StatusButton = Button(tab6, textvariable=kvm47Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm47IP, kvm47Status))
kvm47Status.set("CHECK")
kvm47StatusButton.grid(row=8, column=3)

kvm48NameButton = Button(tab6, text="KVM48", font=("Times", 12), padx=30, command=lambda: editKVM("48")).grid(row=9, column=0)
kvm48IPButton = Button(tab6, text=kvm48IP, font=("Times", 12), padx=5, command=lambda: webIface(kvm48IP)).grid(row=9, column=1)
kvm48LocationLabel = Label(tab6, text=kvm48Loc, font=("Times", 12)).grid(row=9, column=2)
kvm48Status = StringVar()
kvm48StatusButton = Button(tab6, textvariable=kvm48Status, font=("Times", 12), padx=2, command=lambda: kvmPingState(kvm48IP, kvm48Status))
kvm48Status.set("CHECK")
kvm48StatusButton.grid(row=9, column=3)



view.mainloop()


