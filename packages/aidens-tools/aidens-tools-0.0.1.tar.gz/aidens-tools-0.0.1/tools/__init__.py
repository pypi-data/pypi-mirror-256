import os
import math
import threading
import pathlib
import pyttsx3
import urllib
import requests

class Math():
    def add(x, y):
        """
        Adds together x and y and returns the result.
        """
        return x + y

    def sub(x, y):
        """
        Subtracts y from x and returns the result.
        """
        return x - y

    def mul(x, y):
        """
        Multiplies x by y and returns the result.
        """
        return x * y

    def div(x, y):
        """
        Divides x by y and returns the result.
        """
        if y == 0:
            raise Exception("Cannot divide by 0!")
        return x / y

    def pow(x, y):
        """
        Raises x to the power of y and returns the result.
        """
        return x**y

    def clamp(n, smallest, largest):
        """
        Clamps a number between smallest and largest
        """
        return max(smallest, min(n, largest))

class File():
    def open(path, mode=None, buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        """
        Opens a file and returns the file descriptor
        """
        file = open(path, mode, buffering, encoding, errors, newline, closefd, opener)
        return file

    def get_files_in_directory(path, recursive=False, ext=None):
        """
        Returns every file in a given directory with extension filtering and recursiveness
        """
        if ext != None:
            if recursive:
                return list(pathlib.Path(path).rglob("*." + ext))

            return list(pathlib.Path(path).glob("*." + ext))

        if recursive:
            return list(pathlib.Path(path).rglob("*"))

        return list(pathlib.Path(path).glob("*"))

    def get_directories_in_directory(path, recursive=False):
        """
        Returns every folder inside a given directory
        """
        if recursive:
            return [f.path for f in os.scandir(path) if f.is_dir()]

        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

class Random():
    def coin_flip():
        """
        Flips a coin and returns True for Heads and False for Tails
        """
        return random.randint(0, 1) == 0

    def roll_die(lim=6):
        """
        Rolls a die and has a limit determined by the user
        """
        return random.randint(0, lim)

    def rng(x, y):
        """
        Retuns a random number from x to y
        """
        return random.randint(x, y)

class TTS():
    def __init__(self):
        self.engine = pyttsx3.init()

    def say(self, text, wait=False):
        """
        Says a string using pyttsx3
        """
        self.engine.say(text)
        if wait:
            self.engine.runAndWait()

    def get_rate(self):
        """
        Gets the TTS voice rate
        """
        return self.engine.getProperty('rate')

    def set_rate(self, rate=200):
        """
        Sets the TTS voice rate
        """
        self.engine.setProperty('rate', rate)
        return self.engine.getProperty('rate')

    def get_volume(self):
        """
        Gets the TTS voice volume
        """
        return self.engine.getProperty('volume')

    def set_volume(self, vol=1.0):
        """
        Sets the TTS voice volume
        """
        vol = Math.clamp(vol, 0.0, 1.0)
        self.engine.setProperty('volume', vol)
        return self.engine.getProperty('volume')

    def get_voices(self):
        """
        Gets the TTS voices
        """
        return self.engine.getProperty('voices')

    def set_voice(self, voice=0):
        """
        Sets the TTS voice
        """
        voices = self.engine.getProperty('voices')
        voice = Math.clamp(voice, 0, len(voices)-1)
        self.engine.setProperty('voice', voices[voice].id)
        return self.engine.getProperty('voices')

    def get_voice_info(self, voice=0):
        """
        Gets a TTS voices info
        """
        voices = self.engine.getProperty('voices')
        voice = Math.clamp(voice, 0, len(voices)-1)
        return [voices[voice].age, voices[voice].gender, voices[voice].id, voices[voice].languages, voices[voice].name]
    
    def save_to_file(self, text, path):
        """
        Saves a TTS clip to a file
        """
        self.engine.save_to_file(text, path)
        self.engine.runAndWait()
        return path

class Web():
    def get_internet_status(timeout=5):
        """
        Checks if the device is connected to the internet, True if connected else False
        """
        try:
            urllib.request.urlopen('https://8.8.8.8/', timeout=timeout)
            return True
        except urllib.request.URLError as err:
            return False

    def get_website_status_code(website="https://google.com"):
        """
        Gets the status code of a website
        """
        try:
            r = requests.get(website)
            return r.status_code
        except Exception as e:
            print(e)
            return None

    def download_website_html(website="https://google.com", path="download.html"):
        """
        Download and return the path of a downloaded website html file
        """
        try:
            filename, headers = urllib.request.urlretrieve(website, path)
            if filename:
                return path
        except Exception as e:
            print(e)
            return None

class Input():
    def get_number_input_int(message="Please input a number: ", allow_fail=True):
        if allow_fail:
            while True:
                inp = input(message)
                if inp.isdigit():
                    num = int(inp)
                    return num

        inp = input(message)
        if inp.isdigit():
            num = int(inp)
            return num

    def get_number_input_float(message="Please input a float: ", allow_fail=True):
        if allow_fail:
            while True:
                inp = input(message)
                if inp.replace(".", "", 1).isdigit():
                    num = float(inp)
                    return num

        inp = input(message)
        if inp.replace(".", "", 1).isdigit():
            num = float(inp)
            return num

    def get_string_input(message="Please input a string: "):
        string = input(message)
        return str(string)

    def ask_for_item_in_list(message="Select by number: ", lst=["example", "list!", 120, 852.6], allow_fail=True):
        x = 1
        for item in lst:
            print(str(x) + ". " + str(item))
            x += 1

        if allow_fail:
            while True:
                inp = input(message)
                if inp.isdigit():
                    num = int(inp)
                    if 1 <= num < len(lst)+1:
                        return lst[num-1]
                    
                    print("Option not inside list!")
                    continue

        inp = input(message)
        if inp.isdigit():
            num = int(inp)
            if 1 <= num < len(lst)+1:
                return lst[num-1]

            print("Option not inside list!")
            return None

class Threading():
    def delayed_thread(func, delay=0.5, *args, **kwargs):
        threading.Timer(delay, lambda: func(*args, **kwargs)).start()
