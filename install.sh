#!/bin/bash

#TODO Install dependencies - upstart & libusb-dev (building only I think)

if [ `whoami` == "root" ]; then
  if [ $# != 0 ]; then
    if [ $1 == "clean" ]; then
      echo "Cleaning existing installation first"
      rm -rf /opt/eagleowl
      rm -rf /etc/eagleowl.conf
      rm -rf /etc/init.d/rpi-eco-light.conf
      rm -rf /opt/rpi-eco-light
      echo "Done cleaning"
    fi
  fi

  echo "Commencing installation"
  #Install the cm160 application
  if [ ! -e /opt/eagleowl ]; then
    mkdir -p /opt/eagleowl
    cp -r bin/arm/* /opt/eagleowl/
  fi

  #Install the eagleowl configuration file
  if [ ! -e /etc/eagleowl.conf ]; then
    cp etc/eagleowl.conf /etc/eagleowl.conf
  fi

  #Install the rpi-eco-light files
  if [ ! -e /opt/rpi-eco-light ]; then
    mkdir -p /opt/rpi-eco-light
    cp src/* /opt/rpi-eco-light/
  fi

  #Install the init file for rpi-eco-light
  if [ ! -e /etc/init/rpi-eco-light.conf ]; then
    cp etc/init/rpi-eco-light.conf /etc/init/rpi-eco-light.conf
  fi

  echo "Installation complete"
else
  echo "Script must be run as root"
fi
