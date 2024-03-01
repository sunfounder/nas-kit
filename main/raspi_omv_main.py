#!/usr/bin/ python3
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import sys
import os
import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
from utils import *
from page import *
import threading

run_command("sudo resize2fs /dev/mmcblk0p2")
#Menu_page_protect
# Menu_page_protect_flag = 0

#background_color
background_color_config = 255

#page_mode and flag
page_mode_val = 0
page_quantity = 3

#button_val
current_page = 1
last_page = -1
back_button_press_val = 0
button_press_protect = 0
ok_button_press_val = 1
menu_button_val = 1

#key_pin_num
KEY_BACK = 6
KEY_OK = 5
KEY_ADD = 13
KEY_SUB = 19

#GPIO_Irq_Init
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_BACK, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(KEY_OK, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(KEY_ADD, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(KEY_SUB, GPIO.IN, GPIO.PUD_UP)

page = Page(background_color_config)
page.timer = 1

menu_image = Image.new('1', (epd.height, epd.width), 255)
menu_draw = ImageDraw.Draw(menu_image)


#KEY_IRQ_FUNC
def KEY_ADD_FUNC(KEY_ADD):
    global current_page, button_press_protect, menu_button_val, Menu_item_len, page_mode_val, page_quantity

    if button_press_protect == 1 and page_mode_val == 1:
        page.change_val(0)
        if current_page < page_quantity:
            current_page += 1
        else:
            current_page = 1

    if button_press_protect == 0:
        page.change_val(0)
        if current_page < page_quantity:
            current_page += 1
        else:
            current_page = 1
        if menu_button_val < Menu_item_len:
            menu_button_val += 1
        else:
            menu_button_val = 1
    # print(current_page)
    # print(button_press_protect)
    button_press_protect = 0


def KEY_SUB_FUNC(KEY_SUB):
    global current_page, button_press_protect, menu_button_val, Menu_item_len, page_mode_val, page_quantity

    if button_press_protect == 1 and page_mode_val == 1:
        page.change_val(0)
        if current_page > 1:
            current_page -= 1
        else:
            current_page = page_quantity

    if button_press_protect == 0:
        page.change_val(0)
        if current_page > 1:
            current_page -= 1
        else:
            current_page = page_quantity

        if menu_button_val > 1:
            menu_button_val -= 1
        else:
            menu_button_val = Menu_item_len
    button_press_protect = 0
    # print(current_page)
    # print(button_press_protect)


def KEY_BACK_FUNC(KEY_BACK):
    global back_button_press_val, button_press_protect, page_mode_val, page_quantity

    # if button_press_protect == 1 and page_mode_val == 1:
    if page_mode_val == 1:
        page.change_val(0)
        back_button_press_val += 1
    #  print(back_button_press_val)
    if back_button_press_val > 2:
        page.change_val(0)
        back_button_press_val = 0

    if button_press_protect == 0:
        # page.change_val(0)
        back_button_press_val += 1

    # print("button_press_protect: ",button_press_protect)
    # print("back_button_press_val: ",back_button_press_val)


def KEY_OK_FUNC(KEY_OK):
    global last_page, button_press_protect, ok_button_press_val, page_mode_val, page_quantity

    if button_press_protect == 0:
        ok_button_press_val = -1 * ok_button_press_val
        if page_mode_val == 0:
            last_page = -1


#Menu class
class Menu_item_templates():
    global back_button_press_val,last_page,current_page,ok_button_press_val,\
    menu_button_val,Menu_item_len,Menu_item_dict,menu_image,menu_draw

    def __init__(self,
                 item_name="item_name",
                 choise_button_one="NO",
                 choice_button_two="YES"):
        self.item_name = item_name
        self.choice_button_one = choise_button_one
        self.choice_button_two = choice_button_two
        # self.menu_image = Image.new('1', (epd.height, epd.width), 255)
        # menu_draw = ImageDraw.Draw(self.menu_image)
        self.his_button_val = -1
        self.choice_button_flag = -1
        self.choice_button_color = 255
        self.linux_cmd_1 = ":"
        self.linux_cmd_2 = ":"
        self.python_cmd_1 = 'None'
        self.python_cmd_2 = 'None'
        self.item_name_length = len(item_name)
        # self.background_color_config = 255
        # self.page_mode_val = 0

    def linux_cmd(self, input_cmd_1=":", input_cmd_2=":"):
        # do(msg=input_msg,cmd='run_command("intput_cmd")')
        self.linux_cmd_1 = input_cmd_1
        self.linux_cmd_2 = input_cmd_2

    def python_cmd(self, input_cmd_1='None', input_cmd_2='None'):
        self.python_cmd_1 = input_cmd_1
        self.python_cmd_2 = input_cmd_2

    def run_linux_cmd(self, linux_cmd):
        run_command(linux_cmd)

    def run_python_cmd(self, python_cmd):
        global page_mode_val, background_color_config
        exec(python_cmd)

    def item_main(self):
        global back_button_press_val
        while True:
            menu_draw.rectangle((0, 95, 250, 120), fill=255)
            if self.his_button_val != menu_button_val:
                self.choice_button_flag *= -1
                self.his_button_val = menu_button_val

            menu_draw.rectangle(
                (40, 100, 100, 120),
                fill=128 - self.choice_button_flag * self.choice_button_color)
            menu_draw.rectangle(
                (160, 100, 220, 120),
                fill=128 + self.choice_button_flag * self.choice_button_color)
            menu_draw.text(
                (48, 100),
                self.choice_button_one,
                font=font(18),
                fill=128 + self.choice_button_flag * self.choice_button_color)
            menu_draw.text(
                (170, 100),
                self.choice_button_two,
                font=font(18),
                fill=128 - self.choice_button_flag * self.choice_button_color)
            epd.displayPartial(epd.getbuffer(menu_image))

            if ok_button_press_val == 1:

                if self.choice_button_flag == -1:
                    self.run_python_cmd(self.python_cmd_2)
                    self.run_linux_cmd(self.linux_cmd_2)
                else:
                    self.run_python_cmd(self.python_cmd_1)
                    self.run_linux_cmd(self.linux_cmd_1)
                menu_draw.rectangle((0, 90, 250, 120), fill=255)
                epd.displayPartial(epd.getbuffer(menu_image))
                back_button_press_val = 0
                break


###linux_item_cmd

##change background color
item_3_cmd_1 = """
global background_color_config  
background_color_config = 255
"""
item_3_cmd_2 = """
global background_color_config  
background_color_config = 0
"""

##change page refresh mode
item_4_cmd_1 = """
global page_mode_val  
page_mode_val = 0
"""
item_4_cmd_2 = """
global page_mode_val  
page_mode_val = 1
"""
###item_object

item_1 = Menu_item_templates(item_name="shutdown",
                             choise_button_one="NO",
                             choice_button_two="YES")
item_1.python_cmd(input_cmd_2="page.shutdown_Animation()")
item_1.linux_cmd(input_cmd_2="sudo poweroff")

item_2 = Menu_item_templates(item_name="reboot",
                             choise_button_one="NO",
                             choice_button_two="YES")
item_2.linux_cmd(input_cmd_2="sudo reboot")

item_3 = Menu_item_templates(item_name="background color",
                             choise_button_one="white",
                             choice_button_two="black")
item_3.python_cmd(item_3_cmd_1, item_3_cmd_2)

item_4 = Menu_item_templates(item_name="page always refresh",
                             choise_button_one="NO",
                             choice_button_two="YES")
item_4.python_cmd(item_4_cmd_1, item_4_cmd_2)

###item_example

# item_5 = Menu_item_templates(item_name = "item_5",choise_button_one = "OK",choice_button_two = "hello")
# item_5.python_cmd("print('item_5_cmd1')","print('item_5_cmd2')")

# item_6 = Menu_item_templates(item_name = "item_6",choise_button_one = "NO",choice_button_two = "YES")
# item_6.python_cmd("print('item_6_cmd1')","print('item_6_cmd2')")

# item_7 = Menu_item_templates(item_name = "item_7",choise_button_one = "NO",choice_button_two = "YES")
# item_7.python_cmd("print('item_7_cmd1')","print('item_7_cmd2')")

###Menu_dict and length
Menu_item_dict = {
    1: item_1.item_name,
    2: item_2.item_name,
    3: item_3.item_name,
    4: item_4.item_name
}
Menu_item_len = len(Menu_item_dict)

#GPIO_IRQ_RELATION
GPIO.add_event_detect(KEY_BACK, GPIO.RISING, KEY_BACK_FUNC, 200)
GPIO.add_event_detect(KEY_OK, GPIO.RISING, KEY_OK_FUNC, 200)
GPIO.add_event_detect(KEY_ADD, GPIO.RISING, KEY_ADD_FUNC, 200)
GPIO.add_event_detect(KEY_SUB, GPIO.RISING, KEY_SUB_FUNC, 200)


###Menu Page
def Menu_Page():
    global back_button_press_val,last_page,current_page,ok_button_press_val,\
    menu_button_val,Menu_item_len,Menu_item_dict,background_color_config

    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(menu_image))
    epd.init(epd.PART_UPDATE)

    menu_button_val = 1
    ok_button_press_val = 1
    back_button_press_val = 0
    choice_button_flag = -1
    # choice_button_color = 255
    # his_button_val = -1

    while (True):
        menu_draw.rectangle((0, 0, 250, 250), fill=255)
        menu_draw.text((80, 0), "MENU INFO", font=font(18), fill=0)
        menu_draw.line([(0, 20), (250, 20)], fill=0, width=2)
        Menu_page_num = (menu_button_val - 1) / 3

        for i in range(1, 4):
            page_item_num = int(i + 3 * int(Menu_page_num))
            if page_item_num <= Menu_item_len:
                menu_draw.text(
                    (10, (2 * i + 1) * 10),
                    str(page_item_num) + '. ' + Menu_item_dict[page_item_num],
                    font=font(18),
                    fill=0)
            else:
                break

        rectangle_coor_num = (menu_button_val - 1) % 3
        menu_draw.rectangle(
            (0, 2 * (rectangle_coor_num + 1) * 10 + 10, 245, 2 *
             (rectangle_coor_num + 1) * 10 + 30),
            outline=0)
        epd.displayPartial(epd.getbuffer(menu_image))

        if ok_button_press_val == -1:
            eval("item_%s.item_main()" % menu_button_val)

            choice_button_flag = -1
            # his_button_val = -3
            menu_button_val = 1
            current_page = 1

        if back_button_press_val > 0:
            back_button_press_val = 0
            break


###Main Service
def main():
    global current_page, last_page, button_press_protect, background_color_config, page_mode_val

    while True:
        page.background_color = background_color_config
        if current_page != last_page:
            print("main_page")
            button_press_protect = 1
            last_page = current_page
            page.mode = page_mode_val
            page(current_page)
        elif back_button_press_val >= 2:
            print("menu_page")
            Menu_Page()
            current_page = 1
            last_page = -3
            print("quit Menu")

        button_press_protect = 0
        time.sleep(0.1)


###main_thread
def main_thread():
    threads = []
    t1 = threading.Thread(target=main)
    threads.append(t1)
    t2 = threading.Thread(target=pid_control)
    threads.append(t2)
    t1.start()
    t2.start()


if __name__ == '__main__':
    try:
        main_thread()
    except KeyboardInterrupt:
        print("quit")
        exit()