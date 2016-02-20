import os.path, time

class db_comms:

  def __init__(self, db_location):
    self.__db_location = db_location
    self.__live_location = ".live"
    self.__last_update_time = None
    self.__update_checks = 0
    self.__max_update_checks = 10

  def get_current_kw(self):
    with open("{}/{}".format(self.__db_location,
                             self.__live_location),
              "r") as live_file:
      line = live_file.readline()
      splits=line.split()
      kw=0
      if len(splits) >= 4:
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
          print "Max update checks reached, last update time: %s" % (temp_last_update_time)
          ret_val = False #Not good
    return ret_val

