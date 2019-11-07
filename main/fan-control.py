#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 100)


temp_list = []
temp_avg_size = 20 

p.start(0)

t = time.time()

FAN_MAX = 100
FAN_MIN = 20

class PID():
    def __init__(self, P=1, I=1, D=1, expect=0):
        self.P = float(P)
        self.I = float(I)
        self.D = float(D)
        self.expect = expect
        self.error = 0
        self.last_error = 0
        self.error_sum = 0

    @property
    def pval(self):
        return self.error

    @property
    def ival(self):
        self.error_sum += self.error
        return self.error_sum

    @property
    def dval(self):
        return self.error - self.last_error

    def run(self, value, mode="PID"):
        self.last_error = self.error
        self.error = value - self.expect
        # print(self.error, self.last_error, self.pval, self.P)
        result_p = self.P * self.pval
        result_i = self.I * self.ival
        result_d = self.D * self.dval
        mode = mode.upper()
        result = 0.0
        if "P" in mode:
            result += result_p
        if "I" in mode:
            result += result_i
        if "D" in mode:
            result += result_d
        return result

def get_cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp = float(f.read())/1000
    if len(temp_list) > temp_avg_size:
        temp_list.pop(0)
    temp_list.append(temp)
    temp = sum(temp_list) / len(temp_list)
    return temp

# def log(msg):
#     print(msg)
#     name = "/home/pi/fan-control/fan-control-log-%s.txt"%t
#     os.system('echo "%s" >> %s'% (msg, name))

# def log_temp(count, temp, dc):
#     msg = "[%4ss] Temp: %.2f'C  DC: %s%%"%(count, temp, dc)
#     log(msg)
#     # name = "log%s.csv"% t
#     name = "/home/pi/fan-control/fan-control-log-%s.csv"%t
#     os.system('echo "%s, %s, %s" >> %s'% (count, temp, dc, name))

def parabola_control():
    '''y = a * ( x - b )^2 + c'''
    a = 0.2
    b = 30
    c = 10

    while True:
        temp = get_cpu_temp()
        dc = a * ((temp - b) ** 2) + c
        dc = min(FAN_MAX, max(FAN_MIN, dc))
        print("Temp: %s'C  DC: %s%%"%(temp, dc))
        p.ChangeDutyCycle(dc)
        time.sleep(1)

def pid_control():
    pid = PID(
        P = 0.5,
        I = 1,
        D = 1,
        expect = 42,
    )
    dc = 100
    i = 0
    while True:
        temp = get_cpu_temp()
        print(temp)
        dc += pid.run(temp, mode="PD")
        dc = min(FAN_MAX, max(FAN_MIN, dc))
        # log_temp(i, temp, dc)
        print(dc )
        p.ChangeDutyCycle(dc)
        i += 1
        time.sleep(1)
        # if i > 3000:
        #     print("finished.")
        #     break

try:
    pid_control()
except Exception as e:
    log(e)
finally:
    p.ChangeDutyCycle(0)