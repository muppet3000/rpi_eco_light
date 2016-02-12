import os.path, time

class db_comms:

  def __init__(self, db_location):
    self.__db_location = db_location
    self.__live_location = ".live"
    self.__last_update_time = None
    self.__update_checks = 0
    self.__max_update_checks = 10

  def get_current_kw(self):
    file_object = open(self.__db_location+"/"+self.__live_location, "r")
    line = file_object.readline()
    splits=line.split()
    file_object.close()
    kw=float(splits[3])
    kw=kw/1000 #This is a small tweak because the live file returns W not KW - Stoopid!
    return kw

  def check_comms_status(self):
    ret_val = True #Good
    temp_last_update_time = time.ctime(os.path.getmtime(self.__db_location+"/"+self.__live_location))
    if self.__last_update_time == None: #If not initialised
      self.__last_update_time = temp_last_update_time
    else: #Has been initialised
      if self.__last_update_time != temp_last_update_time: #Last update time is different from new one, therefore all is good
        self.__last_update_time = temp_last_update_time
        self.__update_checks = 0
      else: #Update time has not changed, we should see when it last changed
        self.__update_checks = self.__update_checks + 1
        if self.__update_checks >= self.__max_update_checks: #We've reached our max attempts to query - something's gone wrong
          ret_val = False #Not good
    return ret_val






#This was the original plan, however all we need is the 'live' values
#import sqlite3
#
#conn = sqlite3.connect('/home/pi/git_repos/eagle-owl/bin/arm/eagleowl.db')
#c = conn.cursor()
#
#for row in c.execute('SELECT * FROM energy_history ORDER BY year DESC, month DESC, day DESC, hour DESC, "min" DESC LIMIT 1'):
#  print row
