from playsound import playsound
  
class Speaker:  
#   Playcustomsound requires two arguments;
#   1. url is the path to the sound file, keep in mind that is is either a .mp3 or .wav file
#   2. notasync is a bool which decides if the sound file plays asynchronously
#      When false, the file plays asynchronously
    
    def PlayCustomSound(self, url, notasync):
        playsound(url, notasync)