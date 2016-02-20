#!/bin/bash

if [ `whoami` == "root" ]; then
  if [ $# != 0 ]; then
    if [ $1 == "clean" ]; then
      echo "Cleaning existing installation first & disabling services (if running)"
      service cm160 stop
      service rpi-eco-light stop
      rm -rf /opt/eagleowl
      rm -rf /etc/eagleowl.conf
      rm -rf /etc/init/cm160.conf
      rm -rf /etc/init/rpi-eco-light.conf
      rm -rf /opt/rpi-eco-light
      echo "Done cleaning"
    fi
  fi

  echo "Installing dependencies"
  apt-get install -y upstart
  apt-get install -y python-pip python-dev
  pip install unicornhat

  echo "Commencing installation"
  #Install the cm160 application
  if [ ! -e /opt/eagleowl ]; then
    echo "EagleOWL directory doesn't exist, creating and installing"
    mkdir -p /opt/eagleowl
    cp -r bin/arm/* /opt/eagleowl/
  fi

  #Install the eagleowl configuration file
  if [ ! -e /etc/eagleowl.conf ]; then
    echo "EagleOWL conf doesn't exist installing"
    cp etc/eagleowl.conf /etc/eagleowl.conf
  fi

  #Install the init file for eagleconf
  if [ ! -e /etc/init/cm160.conf ]; then
    echo "Installing upstart conf file for EagleOWL/cm160"
    cp etc/init/cm160.conf /etc/init/cm160.conf
  fi

  #Install the rpi-eco-light files
  if [ ! -e /opt/rpi-eco-light ]; then
    echo "rpi-eco-light directory doesn't exist, creating and installing"
    mkdir -p /opt/rpi-eco-light
    cp src/* /opt/rpi-eco-light/
  fi

  #Install the init file for rpi-eco-light
  if [ ! -e /etc/init/rpi-eco-light.conf ]; then
    echo "Installing upstart conf file for rpi-eco-light"
    cp etc/init/rpi-eco-light.conf /etc/init/rpi-eco-light.conf
  fi

  service cm160 restart
  service rpi-eco-light restart

  echo "Installation complete"
else
  echo "Script must be run as root"
fi
