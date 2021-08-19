#!/bin/bash
echo " =====  "
echo "=     = "
echo "=     = "
echo " ====== "
echo "      = "
echo "      = "
echo "      = "
echo " ====== "
echo "Hello ninewatt dev"

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install vsftpd -y
sudo apt-get install realvnc-vnc-server -y
sudo apt-get install xscreensaver -y
sudo ln -Tfs /usr/bin/python3.7 /usr/bin/python
sudo systemctl stop touch-beep.service
sudo systemctl disable touch-beep.service
git clone https://github.com/LouieKim/electricity_meter.git

echo "==== Start install python lib ===="
python -m pip install --upgrade pip
sudo python -m pip install pymodbus
sudo python -m pip install supervisor
sudo python -m pip install setproctitle
sudo python -m pip install apscheduler
python -m pip install sqlalchemy
python -m pip install flask_cors
python -m pip install flask_sqlalchemy

sudo echo "@python /home/pi/electricity_meter/__main__.py" >> .config/lxsession/LXDE-pi/autostart
sudo echo "@chromium-browser --disable-pinch --incognito --noerrdialogs --disable-suggestions-service --disable-translate --disable-save-password-bubble --disable-session-crashed-bubble --disable-infobars --touch-events=disabled --disable-gesture-typing --check-for-update-interval=31536000 --kiosk --app=http://localhost:7070" >> /etc/xdg/lxsession/LXDE-pi/autostart 

exit 0
