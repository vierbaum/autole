#!/usr/bin/bash

git pull --all

sudo cp autostart.service /etc/systemd/system/
sudo systemctl enable autostart.service

while true
do
    python server.py
done
