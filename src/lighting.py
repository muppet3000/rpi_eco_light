import time
import unicornhat as UH

class Lighting:
  BLUE=(0, 0, 255)
  GREEN=(0, 255, 0)
  YELLOW=(177, 142, 52)
  ORANGE=(255, 165, 0)
  RED=(255, 0, 0)
  PURPLE=(148, 0, 211)

  def __init__(self):
    self.__current_value=self.BLUE
    UH.brightness(1.0)
    pixels=self.__set_whole_grid(self.__current_value)
    UH.set_pixels(pixels)
    UH.show()

  def set_light(self, target_value):
    set_to_value=self.__current_value
    while set_to_value != target_value:
      set_to_value=self.__fade_between_rgb(set_to_value, target_value,1)
      pixels=self.__set_whole_grid(set_to_value)
      UH.set_pixels(pixels)
      UH.show()
      time.sleep(0.01)
    self.__current_value=set_to_value

  def set_error(self):
    for i in range(0,10):
      UH.off()
      pixels=self.__set_whole_grid(self.PURPLE)
      UH.set_pixels(pixels)
      UH.show()
      time.sleep(0.4)
    self.__current_value=self.PURPLE
    self.__log("ERROR")

  def __log(self, message):
     print(str(message))
#    with open("/tmp/rpi-eco-light.txt", "a") as log_file:
#      log_file.write(str(message)+"\n")
#      log_file.close()

  def __set_whole_grid(self, rgb_val):
    pixels=[]
    for y in range(8):
      pixels.append([])
      for x in range(8):
        pixels[len(pixels)-1].append(rgb_val)
    return pixels

  def __fade_between_rgb(self, current_rgb, desired_rgb, change_step=2):
    r=0
    g=0
    b=0
    for i in range(0, change_step):
      r=self.__inc_dec(current_rgb[0],desired_rgb[0])
      g=self.__inc_dec(current_rgb[1],desired_rgb[1])
      b=self.__inc_dec(current_rgb[2],desired_rgb[2])
    return (r,g,b)

  def __inc_dec(self, curr_val, des_val):
    ret_val=curr_val
    if curr_val < des_val:
      ret_val+=1
    elif curr_val > des_val:
      ret_val-=1
    return ret_val
