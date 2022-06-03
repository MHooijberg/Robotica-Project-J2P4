from playsound import playsound
  
class Speaker:  
    # TODO: Add the right URL Paths:
    #       The following methods are examples, you are free to modify those and add new ones
    #       Keep the following in mind, when adding new sound methods;
    #       1. Within __init__ determine the URL path of the audio file and assing it to a variable
    #       2. Then, in the corresponding method, use self. + the previously assigned variable as the first argument
    #          for the "playsound" method
    #       3. The second argument can either be true or false. When no second argument is given,
    #          true will be automatically be assigned
    #          When false is chosen, the audio will play asynchronously, contrarely to true.
    #       Keep in mind that this library only supports .wav and .mp3 files
    def __init__(self):
        hello = '/Voices/Hello.mp3'
        pitch = '/Voices/Pitch.mp3'
        music = '/Voices/track.mp3'
        farewell = '/Voices/farewell.mp3'
        catchphrase = '/Voices/catchphrase.mp3'

    def Greet(self):
        playsound(self.hello, False)

    def Pitch(self):
        playsound(self.pitch, False)

    def PlayMusic(self):
        playsound(self.music, False)

    def Greet2(self):
        playsound(self.farewell, False)
    
    def Catchphrase(self):
        playsound(self.catchphrase, False)