"""
Using I2C LCD 20*04 to show information
Initially for the Orange Pi 5
RC 2023-01-04

2023-01-04 v0.1.0: let's start
"""

import sys
import os
import argparse
from datetime import datetime
from datetime import timedelta
from time import sleep
from time import time
from time import strftime
from time import gmtime
from typing import ChainMap

import socket
import platform
import unicodedata
import psutil

class LCD20CPU:
    """
    This is the class to manage the LCD 20x04
    """
    def __init__(self): 
        
        self.__version__ = "v0.2.0"
                
        description = "LCD20CPU Monitor you Pi with a 20x4 LCD"
        
        lcd_help = "LCD address something like 0x3f"
        i2c_help = "i2cdetect port, 0 or 1, 0 for Orange Pi Zero, 1 for Rasp > V2 or OPi5"
        virtual_lcd_help = "yes or no, yes means no LCD, just print on screen"
        display_mode_help = "set cpu or cpuram or cpudisk or clock"
        
        parser = argparse.ArgumentParser(description = description)
        parser.add_argument("-l","--lcd", type=lambda x: int(x, 0), default=0x3f, help = lcd_help)
        parser.add_argument("-i","--i2c_port", type=int, default=1, help = i2c_help)
        parser.add_argument("-v","--virtual_lcd", type=str, default="yes", help = virtual_lcd_help)
        parser.add_argument("-d","--display_mode", type=str, default="", help = display_mode_help)

        
        try:
            args = parser.parse_args()
        except Exception as e:
            print("Error: " + str(e))
            sys.exit(1)

        if os.getenv('LMS_LCD') is not None:
            args.player_name = os.environ['LMS_LCD']
        if os.getenv('LMS_I2C_PORT') is not None:
            args.i2c_port = os.environ['LMS_I2C_PORT']
        if os.getenv('LMS_VIRTUAL_LCD') is not None:
            args.virtual_lcd = os.environ['LMS_VIRTUAL_LCD']
        if os.getenv('LMS_DISPLAY_MODE') is not None:
            args.display_mode = os.environ['LMS_DISPLAY_MODE'] 
        
        self.display_mode = args.display_mode
        lcd = args.lcd
        i2c_port  = args.i2c_port
        virtual_lcd = args.virtual_lcd
        self.display_mode = args.display_mode

        print("-------------------------------")
        print("LCD20CPU class " + self.__version__ + " started!")
        print("params are")
        print("lcd address : " + str(lcd))
        print("i2c_port    : " + str(i2c_port))
        print("virtual_lcd : " + virtual_lcd)
        print("display_mode: " + self.display_mode)
        print("-------------------------------")



        if "Windows" in platform.platform() or virtual_lcd == "yes":
            import no_lcddriver
            self.lcd = no_lcddriver.lcd(address = lcd, columns=20, lines=4) 
        else:
            import lcddriver
            self.lcd = lcddriver.lcd(address = lcd, columns=20, lines=4, i2c_port=i2c_port)
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("    C&R ID ", 1)
            self.lcd.lcd_display_string("  Audiofolies" , 2)
            sleep(0.5)

        self.pct = 0    # CPU usage
        self.tmp = 0    # CPU temp

    def cpu_usage(self):
        """
        Print the CPU usage lines
        with bargraph for CPU & TEMP
        CLOCK %CPU
        TIME  °TMP
        CPU% __________
        TEMP __________
        """
        self.clock()
        
        # pct = psutil.cpu_percent()
        # tmp = int(psutil.sensors_temperatures()["soc_thermal"][0][1])
        freq = psutil.cpu_freq()
        
        self.lcd.lcd_display_string("CPU% " + chr(255) * int((self.pct / 10))  + chr(95) * (10 -(int(self.pct / 10))), 3) 
        self.lcd.lcd_display_string("TMP" + chr(223) + " " + chr(255)  * round((self.tmp / 10))  + chr(95) * (10 -(round(self.tmp / 10))), 4)
        
        sleep(0.5)
    
    def cpu_core(self):
        """
        Print the CPU Core usage lines
        for each core
            - current Frequency / Min / Max frequency 
            - bargraph for %Usage and %usage
        """
        cpus = psutil.cpu_freq(percpu=True)
        i = 0
        for cpu in cpus:            
            self.clock()

            # Frequency
            instantfcpus = psutil.cpu_freq(percpu=True)
            fcpu = instantfcpus[i]

            # Percent CPU
            instantpcpus = psutil.cpu_percent(percpu=True)
            pcpu = instantpcpus[i]
            if pcpu < 10:
                pct = pcpu
            else:
                pct = round(pcpu)
            
            self.lcd.lcd_display_string("CuMiMx " + str(round(fcpu.current)) + "/" + str(round(fcpu.min)) + "/" + str(round(fcpu.max)), 3)

            self.lcd.lcd_display_string("C" + str(i) + ">" + chr(255) * int((pct / 10)) 
                                        + chr(95) * (10 -(int(pct / 10))) +"<" + " " + str(round(pct,1)) + "%", 4) 
            
            i = i + 1
            sleep(0.5)

    def cpu_temp(self):
        """
        Print the different sensors temperature
        """
        # self.clock()

        temps = psutil.sensors_temperatures()
        i = 1
        for temp in temps:

            self.lcd.lcd_display_string(str(i) + "/" + str(len(temps)) + " " + temp, 1)
            self.lcd.lcd_display_string("current: {}c".format(temps[temp][0][1]), 2)
            if temps[temp][0][2] is not None:
                self.lcd.lcd_display_string("high   : {}c".format(temps[temp][0][2]), 3)
            else:
                self.lcd.lcd_display_string("high   : unknow", 3)
            if temps[temp][0][3] is not None:
                self.lcd.lcd_display_string("criticl: {}c".format(temps[temp][0][3]), 4)
            else:
                self.lcd.lcd_display_string("criticl: unknow", 4)

            sleep(3)
            i = i + 1
    
    def cpu_ram(self):
        """
        Print the 2 RAM usage lines
        """
        self.clock()
        # print("total " + str(psutil.virtual_memory().total / 1024 / 1024))
        # print("avail " + str(psutil.virtual_memory().available / 1024 / 1024))
        total = int(psutil.virtual_memory().total / 1024 / 1024)
        avail = int(psutil.virtual_memory().available / 1024 / 1024)
        used = int(psutil.virtual_memory().used / 1024 / 1024)
        pct = round((total - avail) / total * 100,1)
        # print("pct " + str(round(pct,1)))
        self.lcd.lcd_display_string("RAM: " + str(total)
                                    + "/" + str(used) + " " + str(pct) + "%" , 3)
        # self.lcd.lcd_display_string("use " + str(int(psutil.virtual_memory().used / 1024 / 1024)) 
        # + "Mo " + str(round(pct,1)) + "%" , 4)
        self.lcd.lcd_display_string(chr(255) * int((pct / 5) + 1)  + chr(95) * (20 -(int(pct / 5))), 4) 
                        
        sleep(0.5)

    def cpu_disk(self):
        """
        Print disks info
        """
        hdd = psutil.disk_partitions()
        data = []
        nbdisk = 0
        for partition in hdd:
            device = partition.device
            path = partition.mountpoint
            fstype = partition.fstype

            drive = psutil.disk_usage(path)
            total = drive.total
            total = total / 1000000000
            if total > 1:
                nbdisk = nbdisk + 1
                used = drive.used
                used = used / 1000000000
                free = drive.free
                free = free / 1000000000
                percent = int(drive.percent)
                drives = {
                    "device": device,
                    "path": path,
                    "fstype": fstype,
                    "total": float("{0: .2f}".format(total)),
                    "used": float("{0: .2f}".format(used)),
                    "free": float("{0: .2f}".format(free)),
                    "percent": percent
                }
                self.clock()
                self.lcd.lcd_display_string("Disk " + str(nbdisk) + ": " + str(int(total)) + "G", 3)
                self.lcd.lcd_display_string("part: " + device, 2)
                sleep(2)
                self.clock()
                self.lcd.lcd_display_string("used: " + str(int(used )) + "G*" + str(percent) + "%", 4)
                sleep(5)


    def clock(self):
        today = datetime.today()
        self.pct = psutil.cpu_percent()
        try:
            self.tmp = int(psutil.sensors_temperatures()["soc_thermal"][0][1])
        except:
            self.tmp = 0
        
        if self.pct > 10:
            self.pct = int(self.pct)
        self.lcd.lcd_display_string(today.strftime("Clock %d/%m/%Y") + " " + str(self.pct)+ "%", 1)
        self.lcd.lcd_display_string(today.strftime("Time  %H:%M:%S") + "   " + str(self.tmp) + chr(223), 2)
        # sleep(.8)
    
    def main_loop(self):
        while True:
            if "cpu" in self.display_mode:
                if self.display_mode == "cpuonly":
                    self.cpu_usage()
                elif self.display_mode == "cpuram":
                    self.cpu_ram()
                elif self.display_mode == "cpudisk":
                    self.cpu_disk()
                elif self.display_mode == "cpucore":
                    self.cpu_core()
                elif self.display_mode == "cputemp":
                    self.cpu_temp()
                else:
                    self.cpu_usage()
                    sleep(3)
                    self.cpu_core()
                    self.cpu_ram()
                    sleep(3)
                    self.cpu_disk()

                # sleep(.8)
            else:
                self.clock()
                sleep(.8)

if __name__ == "__main__":
        
    myLcd = LCD20CPU()
    myLcd.main_loop()
