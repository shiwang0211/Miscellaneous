# -*- coding: utf-8 -*-
"""
Created on Mon Jan 02 15:11:34 2017

@author: swang
"""
import Tkinter
import tkFileDialog
from Tkinter import BOTH, END, BooleanVar, StringVar
import ttk
import sys
import time
sys.path.append('C:\Users\swang\Desktop\selenium-3.0.2\py') # import selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import urllib

def Download_SLD(roadnum):
    
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("http://www2.dot.state.fl.us/Straight-linesOnlineGIS")
    
    #elem = Select(driver.find_element_by_id("cboDistrict"))
    #elem.select_by_visible_text("D1")
    #
    #elem = Select(driver.find_element_by_id("cboCounty"))
    #elem.select_by_visible_text("LEE")
    
    elem = driver.find_element_by_id("cboRoadway")
    all_options = elem.find_elements_by_tag_name("option")
    for option in all_options:
        if roadnum in option.get_attribute("text"): 
            roadnum_string = option.get_attribute("text")
            break
    
    elem = Select(driver.find_element_by_id("cboRoadway"))
    elem.select_by_visible_text(roadnum_string)
    
    driver.find_element_by_id("btnLaunch").click()
    time.sleep(5)
    
    driver.switch_to_window(driver.window_handles[1])
    elem = driver.find_element_by_id("plugin")
    url = elem.get_attribute("src")
    print (url)
    urllib.urlretrieve(url, "test2.pdf")
    driver.close()


class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()

        #ENTRY CELL
        self.entryVariable = StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entryVariable.set(u"") 

        #CLICK BUTTON
        button = Tkinter.Button(self,text=u"Download",command=self.OnButtonClick) 
        button.grid(column=1,row=0)

        
    def OnButtonClick(self):
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        Download_SLD(self.entryVariable.get())
        
    
if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Download Straight Line Diagram')
    app.geometry("250x50+300+100")
    app.mainloop()
