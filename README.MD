# NAS Kit

This is the E ink display software for the NAS Kit. It only deals with eink display with system information and fan control.
If you need OMV, install it manually.

> OMV needs to be install in a lite version of Raspberry Pi OS. If you have installed OMV on a full version of Raspberry Pi OS, you need to reinstall it.

## Installation guide

Update apt list
    
``` bash
sudo apt update
```

Install dependencies

``` bash
sudo apt install git python3 python3-pip -y
```

Install nas kit
    
``` bash
git clone --depth=1 https://github.com/sunfounder/nas-kit.git
cd nas-kit
sudo python3 setup.py
sudo cp ./bin/omv-epd /etc/init.d/omv-epd
sudo chmod 755 /etc/init.d/omv-epd
sudo update-rc.d omv-epd defaults
```

Enable SPI

``` bash
sudo raspi-config nonint do_spi 0
```

Reboot to apply changes

``` bash
sudo reboot
```

## Install OMV 6

Get Raspberry Pi IP address and remember it.

``` bash
hostname -I
```

Install OpenMediaVault 6

``` bash
wget -O - https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/install | sudo bash
```

After installation done, Reboot your Raspberry Pi

``` bash
sudo reboot
```

After reboot, you can access OMV web interface with the IP address you got before.

```
http://<IP address>
```

After the eeb interface loaded, you will be asked to log in to be able to proceed.

The default username is `admin`, and the default password is `openmediavault`.

Done!, now you can use OMV on your Raspberry Pi.
