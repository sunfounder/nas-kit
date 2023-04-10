# NAS Kit

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

Install OpenMediaVault

``` bash
wget -O - https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/install | sudo bash
```

