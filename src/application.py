#!/usr/bin/python

import time, sys

import db_comms
from lighting import Lighting

DB_PATH="/opt/eagleowl"
SLEEP_TIME_IN_SECS=5
COST_PER_HOUR_IN_PENCE=13.37

#Converts KW to RGB based on cost per hour
def kw_to_rgb(kw):
  kw_in_pence=COST_PER_HOUR_IN_PENCE*kw
  print "KW in pence: %s" % kw_in_pence
  rgb_dict=Lighting.GREEN
  if kw_in_pence > 14:
    rgb_dict=Lighting.RED
  elif kw_in_pence < 14:
    rgb_dict=Lighting.GREEN
        
  return rgb_dict


try:
  #Create comms and lighting instances
  comms=db_comms.db_comms(DB_PATH)
  light=Lighting()

  while True:
    kw=comms.get_current_kw() #Get current kw
    rgb_dict=kw_to_rgb(kw) #Get the dictionary for colouring
    light.set_light(rgb_dict) #Set the light value


    if comms.check_comms_status() == False:
      light.set_error()

    #Sleep for a bit before the next update
    time.sleep(SLEEP_TIME_IN_SECS)
   

except KeyboardInterrupt:
    print "" #Clear the current line
    sys.exit()
