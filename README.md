# SunFounder NAS Kit

This script allows you to run the EPD display on SunFounder NAS Kit.

## Dependencies

The only required Python dependencies are the following:
- `RPi.GPIO`
- `spidev`

:warning: You must **NOT** use `Rpi.GPIO2` nor `gpiod`. The script provided by SunFounder does not use these dependencies at all, only the ones listed above. If they are installed on your system, remove them:

- `sudo pip3 uninstall Rpi.GPIO2 gpiod`
- `pip3 uninstall Rpi.GPIO2 gpiod`

## Prerequisites

Make sure SPI is enabled on your Raspberry Pi:

1. `ssh pi@your-ip-address`
2. `sudo raspi-config`
3. Navigate to `5 Interfacing Options` and press Enter
4. Navigate to `P4 SPI` and Press Enter
5. Answer `Yes` to the question
6. Quit raspi-config (Ctrl-C or navigate to exit menu)
5. Reboot your Raspberry Pi: `sudo reboot now`

## Setup

Clone this repo:

- `cd ~`
- `git clone https://github.com/sunfounder/nas-kit`

Go to `nas-kit` root folder and execute setup:

1. `cd ~/nas-kit`
2. `sudo python3 setup.py` (sudo is important, since this script is meant to run at startup later)

That's all! You can now run the script.

## Run

- `cd ~/nas-kit`
- `python3 main/raspi_omv_main.py`

### Launch at startup

**Note:** To start `omv-epd` at NAS startup:

1. `ln -s /home/pi/nas-kit/bin/omv-epd /etc/init.d/omv-epd`
2. `sudo systemctl daemon-reload`
3. `sudo systemctl enable omv-epd`
4. `sudo systemctl start omv-epd`

It should now start the NAS Kit EPD screen display at startup! :tada: 
