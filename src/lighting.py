class Lighting:
  #TODO Implement colours
  RED={'red': 255, 'green': 0, 'blue': 0}
  GREEN={'red': 0, 'green': 255, 'blue': 0}

  def __init__(self):
    None

  #TODO Implement light setting features
  def set_light(self, light_dict):
    self.__log(light_dict)

  #TODO Set error colour/pattern
  def set_error(self):
    self.__log("ERROR")

  def __log(self, message):
    filehandle=open("/tmp/rpi-eco-light.txt", "a")
    filehandle.write(str(message)+"\n")
    filehandle.close()
