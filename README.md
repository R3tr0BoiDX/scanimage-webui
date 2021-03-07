# ScanImage WEB UI

WebUI for linux SANE command `scanimage`. Application is based on Python 
and JavaScript. Runs on localhost:7800 or other specified port. 
This tool enables you to use your USB scanner as network scanner 
for many users. It can be run on Raspberry Pi for example Rapsbian 
Linux system distribution.

## Instalation
```bash
apt update && apt install sane-utils
wget https://gitlab.com/alda78/scanimage-webui/-/archive/master/scanimage-webui-master.tar && \
tar -xf scanimage-webui-master.tar && \
cd scanimage-webui-master/ && \
sudo python3 setup.py install && \
cd ../ &&  \
sudo rm -rf scanimage-webui-master/
```
or simply
```bash
apt update && apt install sane-utils
pip3 install scanimage-webui
```

## Running
```bash
scanimage-webui --help
usage: scanimage-webui [-h] [-p PORT] [-d SCAN_DIRETORY]

Scan Image WEB UI v1.2.3

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  APP server port
  -d SCAN_DIRETORY, --scan-directory SCAN_DIRETORY
                        Directory where scanned images will be stored.
```

## systemd configuration
```bash
echo '[Unit]
Description=ScanImageWebUI

[Service]
ExecStart=/bin/sh "/usr/local/bin/scanimage-webui >> /var/log/scanimage-webui.log 2>&1 &"
ExecStop=killall scanimage-webui
ExecRestart=/bin/sh "killall scanimage-webui && /usr/local/bin/scanimage-webui >> /var/log/scanimage-webui.log 2>&1 &"
ExecStatus=ps -ax | grep scanimage-webui
Type=forking

[Install]
WantedBy=multi-user.target
' > /lib/systemd/system/scanimage-webui.service
systemctl enable scanimage-webui.service
```
after that is possible to use
```bash
systemctl start scanimage-webui.service
```

## Screenshot
![scanimage-webui screenshot](scanimage-webui.png)
