#!/usr/bin/env python3
from version import __version__
from os import geteuid, getlogin
import sys
import time
import threading

if geteuid() != 0:
    print("Script must be run as root. Try 'sudo python3 setup.y'")
    sys.exit(1)


# utils
# =================================================================
def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result


errors = []
at_work_tip_sw = False


def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:
        i = (i + 1) % 4
        sys.stdout.write('\033[?25l')  # cursor invisible
        sys.stdout.write('%s\033[1D' % char[i])
        sys.stdout.flush()
        time.sleep(0.5)

    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h')  # cursor visible
    sys.stdout.flush()


def do(msg="", cmd=""):
    print(" - %s... " % (msg), end='', flush=True)
    # at_work_tip start
    global at_work_tip_sw
    at_work_tip_sw = True
    _thread = threading.Thread(target=working_tip)
    _thread.daemon = True
    _thread.start()
    # process run
    status, result = run_command(cmd)
    # print(status, result)
    # at_work_tip stop
    at_work_tip_sw = False
    _thread.join()  # wait for thread to finish
    # status
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))


def check_devices():
    with open('/proc/device-tree/model', 'r') as f:
        model = f.read()
        if 'Raspberry Pi' in model:
            return "Raspberry Pi"
        elif 'Jetson' in model:
            return "Jetson"
        else:
            return model


# Dependencies
# =================================================================
APT_INSTALL_LIST = [
    "python3-pip",
    "sysstat",  # System performance tools for the Linux operating system
    "i2c-tools",
    # "raspi-config",
    "python3-pil",
    "python3-numpy",
]

PIP_INSTALL_LIST = [
    # 'gpiozero',
    'smbus2',
    'psutil',
    "spidev",
]

model = check_devices()
if model == 'Raspberry Pi':
    PIP_INSTALL_LIST.append('gpiozero')
elif model == 'Jetson':
    PIP_INSTALL_LIST.append('Jetson.GPIO')
else:
    print(f'Unsupported model: {model}')
    sys.exit(1)


def install():
    user_name = getlogin()
    print(f'NAS-Kit installation {__version__} on {model} for {user_name}:')

    if "--no-dep" not in sys.argv:
        ### Rpi_epd_lib
        do(msg="wget BCM2835",
           cmd='wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz'
           )
        do(msg="tar and make install BCM2835",
           cmd=
           'tar zxvf bcm2835-1.60.tar.gz'
           +' && cd bcm2835-1.60/'\
           +' && ./configure'\
           +' && make'\
           +' && make check '\
           +' && make install'
           )

        # =============================
        print("Install dependencies with apt-get:")
        # update apt-get
        do(msg="update apt-get", cmd='sudo apt-get update')
        #
        for dep in APT_INSTALL_LIST:
            do(msg=f"install {dep}", cmd=f'sudo apt-get install {dep} -y')

        # =============================
        print("Install dependencies with pip3:")
        # check whether pip has the option "--break-system-packages"
        _is_bsps = ''
        status, _ = run_command("pip3 help install|grep break-system-packages")
        if status == 0:  # if true
            _is_bsps = "--break-system-packages"
            print(
                "\033[38;5;8m pip3 install with --break-system-packages\033[0m"
            )
        # update pip
        do(msg="update pip3",
           cmd=f'python3 -m pip install --upgrade pip {_is_bsps}')
        #
        for dep in PIP_INSTALL_LIST:
            do(msg=f"install {dep}", cmd=f'pip3 install {dep} {_is_bsps}')

    # Setup interfaces
    # =============================
    print("Setup interfaces")
    do(msg="turn on SPI", cmd='sudo raspi-config nonint do_spi 0')

    # Install service
    # =============================
    print("Install service")
    do(msg='cp nas-kit service file',
       cmd='cp ./bin/nas-kit.service /lib/systemd/system/nas-kit.service' +
       ' && cp ./bin/nas-kit /usr/bin/nas-kit')
    do(msg='chmod', cmd='chmod +x /usr/bin/nas-kit')
    do(msg='systemctl daemon-reload', cmd='systemctl daemon-reload')
    do(msg='enable nas-kit.service', cmd='systemctl enable nas-kit.service')
    do(msg='start nas-kit', cmd='systemctl start nas-kit')

    # Report error
    # =============================
    if len(errors) == 0:
        print("Setup Finished")
    else:
        print("\n\nError happened in install process:")
        for error in errors:
            print(error)
        print(
            "Try to fix it yourself, or contact service@sunfounder.com with this message"
        )
        sys.exit(1)


if __name__ == "__main__":
    try:
        install()
    except KeyboardInterrupt:
        print("Canceled.")
    finally:
        sys.stdout.write(' \033[1D')
        sys.stdout.write('\033[?25h')  # cursor visible
        sys.stdout.flush()
