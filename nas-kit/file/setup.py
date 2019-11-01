
errors = []

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

def install():
    do(msg="wget BCM2835",
        cmd='run_command("wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz")')
    do(msg="tar and make install BCM2835",
        cmd='run_command("tar zxvf bcm2835-1.60.tar.gz && cd bcm2835-1.60/ && sudo ./configure && sudo make && sudo make check && sudo make install")')
    do(msg="install wiringpi",
        cmd='run_command("sudo apt-get install wiringpi && cd /tmp && wget https://project-downloads.drogon.net/wiringpi-latest.deb && sudo dpkg -i wiringpi-latest.deb")')
    do(msg="apt-get update",
        cmd='run_command("sudo apt-get update")')
    do(msg="apt-get install python3-pip",
        cmd='run_command("sudo apt-get install python3-pip")')
    do(msg="apt-get install python3-pil",
        cmd='run_command("sudo apt-get install python3-pil")')
    do(msg="apt-get install python3-numpy",
        cmd='run_command("sudo apt-get install python3-numpy")')
    do(msg="apt-get install RPi.GPIO",
        cmd='run_command("sudo pip3 install RPi.GPIO")')
    do(msg="apt-get install spidev",
        cmd='run_command("sudo pip3 install spidev")')
### Setup OMV env and install OMV
    do(msg="Nas-build",
        cmd='run_command("sudo ./Nas-build")')
    do(msg="install openmediavault",
        cmd='run_command("sudo apt-get install openmediavault-keyring openmediavault")')
    do(msg="Populate the database",
        cmd='run_command("omv-confdbadm populate")')

### install epd
    do(msg="install nas-kit",
        cmd='run_command("sudo git clone https://github.com/sunfounder/nas-kit")')
        
    if len(errors) == 0:
        print("Finished")
    else:
        print("\n\nError happened in install process:")
        for error in errors:
            print(error)
        print("Try to fix it yourself, or contact service@sunfounder.com with this message")

if __name__ =="__main__":
    install()