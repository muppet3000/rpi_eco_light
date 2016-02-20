#!/usr/bin/python

import time, sys, signal

import db_comms
from lighting import Lighting

DB_PATH="/opt/eagleowl"
SLEEP_TIME_IN_SECS=5
COST_PER_HOUR_IN_PENCE=13.37

def signal_term_handler(signal, frame):
    print 'got SIGTERM'
    sys.exit(0)

#Converts KW to RGB based on cost per hour
def kw_to_rgb(kw):
  kw_in_pence=COST_PER_HOUR_IN_PENCE*kw
  print "KW in pence: %s" % kw_in_pence
  rgb_dict=Lighting.GREEN
  if kw_in_pence >= 20:
    print(">= 20 = RED")
    rgb_dict=Lighting.RED
  elif kw_in_pence >= 15:
    print("< 20 && >= 15 = ORANGE")
    rgb_dict=Lighting.ORANGE
  elif kw_in_pence >= 10:
    print("< 15 && >= 10 = YELLOW")
    rgb_dict=Lighting.YELLOW
  elif kw_in_pence >= 8:
    print("< 10 && >= 8 = GREEN")
    rgb_dict=Lighting.GREEN
  elif kw_in_pence < 8:
    print("< 8 = BLUE")
    rgb_dict=Lighting.BLUE
        
  return rgb_dict


try:
  signal.signal(signal.SIGTERM, signal_term_handler)

  #Create comms and lighting instances
  comms=db_comms.db_comms(DB_PATH)
  light=Lighting()

  while True:
    if comms.check_comms_status() == False:
      light.set_error()
    else:
      kw=comms.get_current_kw() #Get current kw
      rgb_dict=kw_to_rgb(kw) #Get the dictionary for colouring
      light.set_light(rgb_dict) #Set the light value

    #Flush the stdout each time round the loop
    sys.stdout.flush()

    #Sleep for a bit before the next update
    time.sleep(SLEEP_TIME_IN_SECS)
   

except KeyboardInterrupt:
    print "" #Clear the current line
    sys.exit(0)
