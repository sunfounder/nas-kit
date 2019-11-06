import subprocess
import os
import RPi.GPIO as GPIO
import time


FAN_PWM = 18
LED_PWM = 26
fan_pwn_freq = 100
led_pwn_freq = 1

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
output_list = [FAN_PWM,LED_PWM]
GPIO.setup(output_list, GPIO.OUT)

fan_pwm_pin = GPIO.PWM(FAN_PWM, fan_pwn_freq)
led_pwm_pin = GPIO.PWM(LED_PWM, led_pwn_freq)
fan_pwm_pin.start(0)
led_pwm_pin.start(50)

#run_command linux
def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    # print(result)
    # print(status)
    return status, result

def do(msg="", cmd=""):
    print(" - %s..." % (msg), end='\r')
    print(" - %s... " % (msg), end='')
    status, result = eval(cmd)
    # print(status, result)
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

def cpu_temperature():          # cpu_temperature
    raw_cpu_temperature = subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp") 
    cpu_temperature = round(float(raw_cpu_temperature)/1000,1)               # convert unit
    cpu_temperature = str(cpu_temperature)
    return cpu_temperature

def gpu_temperature():          # gpu_temperature(
    raw_gpu_temperature = subprocess.getoutput( '/opt/vc/bin/vcgencmd measure_temp' )
    gpu_temperature = round(float(raw_gpu_temperature.replace( 'temp=', '' ).replace( '\'C', '' )), 1)
    gpu_temperature = str(gpu_temperature)
    return gpu_temperature

def cpu_usage():                # cpu_usage
    # result = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print($2)}'").readline().strip())
    result = os.popen("mpstat").read().strip()
    result = result.split('\n')[-1].split(' ')[-1]
    result = round(100 - float(result), 2)
    result = str(result)
    # print(result)
    return result

def disk_space():               # disk_space
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()         
        if i==2:
            return line.split()[1:5] 

def portable_hard_disk_info():
    disk_num = os.popen("df -h | grep '/dev/sd' -c")
    phd = os.popen("df -h | grep '/dev/sd'") 
    i = 0
    phd_line = disk_num.readline()

    line_list = []
    if int(phd_line) != 0:
        while 1:
            i = i +1
            line = phd.readline()
            line_list.append(line.split()[0:6])        
            if i==int(phd_line):
                return line_list
    else:
        return []

def ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return list(map(lambda x:round(int(x) / 1000,1), line.split()[1:4]))   

def pi_read():
    result = {
        "cpu_temperature": cpu_temperature(), 
        "gpu_temperature": gpu_temperature(),
        "cpu_usage": cpu_usage(), 
        "disk": disk_space(), 
        "ram": ram_info(), 
        # "battery": power_read(), 
    }
    return result 

def fan_control(temp = 0):
    if temp >=68:
        fan_duty_cycle = round(float(temp-67)*30,1)
        led_freq = int(temp-67)
        if  fan_duty_cycle >= 100:
            fan_duty_cycle = 100
        
        fan_pwm_pin.ChangeDutyCycle(fan_duty_cycle)
        led_pwm_pin.ChangeDutyCycle(100)  
        
    else:
        fan_pwm_pin.ChangeDutyCycle(0)
        led_pwm_pin.ChangeDutyCycle(0) 

def fan_power_read():
    average_temp = int((float(cpu_temperature())+float(gpu_temperature()))/2.0)
    if average_temp >= 68:
        return round(float(average_temp-67)*30,1)
    else:
        return 0

def fan_led_stop():
    fan_pwm_pin.ChangeDutyCycle(0)
    led_pwm_pin.ChangeDutyCycle(0)  
    GPIO.cleanup()

def getIP(ifaces=['wlan0', 'eth0']):
    import re
    if isinstance(ifaces, str):
        ifaces = [ifaces]
    for iface in list(ifaces):
        search_str = 'ip addr show {}'.format(iface)
        result = os.popen(search_str).read()
        com = re.compile(r'(?<=inet )(.*)(?=\/)', re.M)
        ipv4 = re.search(com, result)
        if ipv4:
            ipv4 = ipv4.groups()[0]
            return ipv4
    return False

if __name__ == '__main__':
    print(portable_hard_disk_info())
