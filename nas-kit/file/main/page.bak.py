import RPi.GPIO as GPIO
import sys
import os
import logging
import time 
from PIL import Image,ImageDraw,ImageFont 
import traceback
from utils import *


fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from epd_lib import epd2in13_V2 

epd = epd2in13_V2.EPD()

font8 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 8) 
font14 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 14)
font16 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 16)
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
font21 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 21)
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)

page_change_flag = 1   

def page_1(page1_background_color,mode = 0): 
    global page_change_flag

    time_image = Image.new('1', (epd.height, epd.width), page1_background_color)
    time_draw = ImageDraw.Draw(time_image)
    
    
    epd.init(epd.FULL_UPDATE) 
    epd.displayPartBaseImage(epd.getbuffer(time_image)) 
    epd.init(epd.PART_UPDATE)
    
    refresh_num = 0
    pi_msg ={}
    
    while (page_change_flag): 
        pi_msg = pi_read()
        fan_control(int((float(cpu_temperature())+float(gpu_temperature()))/2.0))
        
        time_draw = ImageDraw.Draw(time_image)
        time_draw.text((80, 0), "BASIC INFO", font = font18, fill = 255-page1_background_color)
        time_draw.line([(0,22),(250,22)], fill = 255-page1_background_color,width = 2)
        
        time_draw.rectangle((0, 23, 150, 47), fill = 255-page1_background_color)
        time_draw.text((0, 26), 'IP: ' + str(getIP()), font = font18, fill = page1_background_color)
        
        time_draw.rectangle((42, 53, 105, 73), fill = page1_background_color)
        time_draw.text((0, 53), 'CPU: ' + pi_msg['cpu_usage'] + '%', font = font18, fill = 255-page1_background_color)
        time_draw.rectangle((0, 75, 234, 85), outline = 255-page1_background_color)
        time_draw.rectangle((0, 75, 234 * float(pi_msg['cpu_usage'])/100, 85), fill = 255-page1_background_color)

        Ram_usage = round(pi_msg['ram'][1] / pi_msg['ram'][0],2)
        time_draw.rectangle((42, 88, 105, 108), fill = page1_background_color)
        time_draw.rectangle((175, 88, 230, 108), fill = page1_background_color)
        time_draw.text((0, 88), 'RAM: ' + str(Ram_usage) + '%', font = font18, fill = 255-page1_background_color)
        time_draw.text((130, 88), 'total: ' + str(pi_msg['ram'][0]), font = font18, fill = 255-page1_background_color)
        time_draw.rectangle((0, 110, 234, 120), outline = 255-page1_background_color)
        time_draw.rectangle((0, 110, 234 * Ram_usage/100, 120), fill = 255-page1_background_color) 
       
        epd.displayPartial(epd.getbuffer(time_image))  
        refresh_num = refresh_num + 1
        if refresh_num == 5 and mode == 0:
            break
    if mode == 1:
        change_val(1)

def page_2(page2_background_color,mode = 0):
    refresh_num = 0
    global page_change_flag
    Detailed_image = Image.new('1', (epd.height, epd.width), page2_background_color)  # 255: clear the frame
    Detailed_draw = ImageDraw.Draw(Detailed_image)

    epd.init(epd.FULL_UPDATE) 
    epd.displayPartBaseImage(epd.getbuffer(Detailed_image))
    epd.init(epd.PART_UPDATE)
    
    Detailed_draw.text((65, 0), "DETAILED INFO", font = font18, fill = 255-page2_background_color)
    Detailed_draw.line([(0,25),(250,25)], fill = 255-page2_background_color,width = 2)
    Detailed_draw.text((9, 48), 'CPU', font = font18, fill = 255-page2_background_color)
    Detailed_draw.text((100, 48), 'GPU', font = font18, fill = 255-page2_background_color)
    Detailed_draw.text((198, 48), 'FAN', font = font18, fill = 255-page2_background_color)
    epd.displayPartial(epd.getbuffer(Detailed_image))
    
    while page_change_flag:
        pi_msg = pi_read()
        fan_control(int((float(cpu_temperature())+float(gpu_temperature()))/2.0))
        # Detailed_draw.rectangle((0, 80, 250, 100), fill = page2_background_color)

        Detailed_draw.arc((8,73,16,81),180,360, fill = 255-page2_background_color)
        Detailed_draw.line([(8,77),(8,93)], fill = 255-page2_background_color,width = 1)
        Detailed_draw.line([(16,77),(16,93)], fill = 255-page2_background_color,width = 1)
        Detailed_draw.arc((2,93,22,112),-60,247, fill = 255-page2_background_color)

        Detailed_draw.ellipse((8,97,16,105),fill = 255-page2_background_color)
        Detailed_draw.line([(12.5,81),(12.5,100)], fill = 255-page2_background_color,width = 1) 

        Detailed_draw.arc((95,73,103,81),180,360, fill = 255-page2_background_color)
        Detailed_draw.line([(95,77),(95,93)], fill = 255-page2_background_color,width = 1)
        Detailed_draw.line([(103,77),(103,93)], fill = 255-page2_background_color,width = 1)
        Detailed_draw.arc((89,93,109,112),-60,247, fill =255- page2_background_color)

        Detailed_draw.ellipse((95,97,103,105),fill = 255-page2_background_color)
        Detailed_draw.line([(99,81),(99,100)], fill = 255-page2_background_color,width = 1)

        Detailed_draw.ellipse((170,74,202,106),fill = 255-page2_background_color)
        Detailed_draw.pieslice((174,78,198,102),0+refresh_num*60,60+refresh_num*60, fill = page2_background_color)
        Detailed_draw.pieslice((174,78,198,102),120+refresh_num*60,180+refresh_num*60, fill = page2_background_color)
        Detailed_draw.pieslice((174,78,198,102),240+refresh_num*60,300+refresh_num*60, fill = page2_background_color)
        Detailed_draw.ellipse((182,86,190,94),fill = 255-page2_background_color)
        Detailed_draw.ellipse((184,88,188,92),fill = page2_background_color)
       
        Detailed_draw.text((24, 80), pi_msg['cpu_temperature'] + 'C', font = font14, fill = 255-page2_background_color)
        Detailed_draw.text((111, 80), pi_msg['gpu_temperature'] + 'C', font = font14, fill = 255-page2_background_color)

        Detailed_draw.text((210, 80), str(fan_power_read()) + '%', font = font14, fill = 255-page2_background_color)
        epd.displayPartial(epd.getbuffer(Detailed_image)) 
        refresh_num = refresh_num + 1
        if refresh_num == 5 and mode == 0:
            break
    if mode == 1:
        change_val(1)

def page_3(page3_background_color,mode = 0):
    refresh_num = 0
    global page_change_flag
    disk_image = Image.new('1', (epd.height, epd.width), page3_background_color)
    disk_draw = ImageDraw.Draw(disk_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(disk_image)) 
    epd.init(epd.PART_UPDATE)

    pi_msg ={}

    while (page_change_flag):
        pi_msg = pi_read()
        fan_control(int((float(cpu_temperature())+float(gpu_temperature()))/2.0))
        disk_draw.rectangle((0, 0, 250, 250), fill = page3_background_color)
        disk_draw.text((80, 0), "DISK INFO", font = font18, fill = 255-page3_background_color)
        disk_draw.line([(0,25),(250,25)], fill = 255-page3_background_color,width = 2)
        disk_draw.text((6, 30), 'Disk: ' + pi_msg['disk'][3], font = font18, fill = 255-page3_background_color)
        disk_draw.rectangle((2, 53, 234, 63), outline = 255-page3_background_color)
        disk_draw.rectangle((3, 53, 234 * float(pi_msg['disk'][3].replace('%', ''))/100, 63), fill = 255-page3_background_color)
        epd.displayPartial(epd.getbuffer(disk_image)) 
        refresh_num = refresh_num + 1
        if refresh_num == 5 and mode == 0:
            break
    if mode == 1: 
        change_val(1)
        
def shutdown_Animation():
    Rocket_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    Rocket_draw = ImageDraw.Draw(Rocket_image)

    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(Rocket_image))
    epd.init(epd.PART_UPDATE)

    Rocket_draw.rectangle((0, 0, 250, 250), fill = 255) 
    epd.displayPartial(epd.getbuffer(Rocket_image))
    
    for i in range(4):
        wod = i*76
        Rocket_draw.rectangle((wod, 25, 135+wod, 95), outline = 0)
        Rocket_draw.polygon([(135+wod,25),(135+wod,95),(175+wod,60)],fill = 0)

        Rocket_draw.polygon([(wod,25),(wod,45+i*5),(wod-15-i*10,36-i*12)],fill = 0)
        Rocket_draw.polygon([(wod,48-i*4),(wod,71+i*4),(wod-20-i*20,60)],fill = 0)
        Rocket_draw.polygon([(wod,71-i*5),(wod,95),(wod-15-i*10,83+i*12)],fill = 0)
        Rocket_draw.text((10+wod, 35), 'Goodbye ! Sir', font = font18, fill = 0)
        Rocket_draw.text((10+wod, 65), 'Sunfounder', font = font18, fill = 0)
        epd.displayPartial(epd.getbuffer(Rocket_image))
        time.sleep(0.8)

        Rocket_draw.rectangle((0, 0, 250, 250), fill = 255)
        epd.displayPartial(epd.getbuffer(Rocket_image))

def change_val(x = 0):
    global page_change_flag
    page_change_flag = x
    return page_change_flag