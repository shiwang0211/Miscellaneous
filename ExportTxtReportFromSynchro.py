import subprocess
import time
import os
import sys
import glob
sys.path.append('C:/Python27/ArcGIS10.2/Lib')
import pyautogui

scenarios = ['AM_0', 'AM_1','AM_2','AM_3','AM_4','PM_0','PM_1','PM_2','PM_3','PM_4','PM_5']

path = os.getcwd()
for file in glob.glob(path + '//*.syn'):
    #subprocess.Popen(['start', file], shell=True)
    time.sleep(5)
    for scenario in scenarios:
        
        pyautogui.hotkey('alt', 't')
        time.sleep(1)
        pyautogui.press('right')
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)  
            
        pyautogui.typewrite(scenario+'.csv') 
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(3)
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(1)
        pyautogui.hotkey('alt', 't')
        time.sleep(3)
        pyautogui.typewrite(scenario+'_HCM2000.txt') 
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)
        
        pyautogui.hotkey('ctrl', 's')
        time.sleep(10)
