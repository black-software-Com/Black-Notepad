#!/bin/sh
# Black-Notepad v1.0
#

if [[ "$(id -u)" -ne -0 ]];
then
  echo "
Please, Run This Program as Root!
"
  exit
fi

function Main() {
    printf '\033]2;Black-Notepad/Installing\a'
    clear
    echo " ---[ Black-Notepad ]---"
    sleep 1
    echo "Installing..."
    chmod +x black
    cp black /usr/bin && cp black /usr/local/bin
    sleep 2
    apt install python
    apt install python3
    apt install python3-pip
    pip3 install --upgrade pip3
    pip3 install -r /Core/requirements.txt
    sleep 1
    echo "
Finish...

Usage:
     ./black
    "
}

Main
