#!/bin/sh
# Black-Notepad v1.0
#
if [[ "$(id -u)" -ne 0 ]];
then
  echo "
Please, Run This Program as Root !
"
  exit
fi

function Main() {
        printf '\033]2;Black-Notepad/Installing\a'
        clear
        echo "-----[ Black-Notepad ]-----"
        echo " "
        chmod +x black
        sleep 2
        apt install python
        apt install python3
        apt install python3-pip
        pip3 install --upgrade pip
        python3 -m pip install -r requirements.txt
        sleep 2
        cp black /usr/bin && cp black /usr/local/bin
        echo "Finish...!"
        echo "
Usage:
      black
"
        sleep 1
        exit
}
Main
