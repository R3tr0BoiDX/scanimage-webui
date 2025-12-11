#!/bin/bash

while true; do
    sudo python3 setup.py install
    scanimage-webui
done