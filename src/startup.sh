#!/bin/bash
echo "Running App"
cd /opt/eagleowl
/opt/eagleowl/cm160 &> /var/log/cm160.log &
echo "Sleeping"
sleep 20
echo "Done sleeping - starting app"
python /opt/rpi-eco-light/application.py &> /var/log/rpi-eco-light.log &
