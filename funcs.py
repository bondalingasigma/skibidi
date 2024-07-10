import os
from datetime import datetime
from say import say
import requests
import speedtest
from youtubesearchpython import VideosSearch

# Vars
STRPATH = os.path.join(os.getcwd(), "Storage")
USERNAME = "Kaiden"
BOTNAME = "JARVIS"

# File System
def newfile(filename, file_type, dir=""):
    # Create the directory if it doesn't exist
    os.makedirs(STRPATH, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(STRPATH,dir, f"{filename}.{file_type}")
    f = open(file_path, "a")
    return "Successfuly Created File"

def readfile(filename, dir=""):
    file_path = os.path.join(STRPATH,dir, filename)
    
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found in '{STRPATH}'")
        return None
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return None

def writefile(filename, content, dir=""):

    file_path = os.path.join(STRPATH,dir, filename)
    
    try:
        # Open the file in write mode ("w")
        with open(file_path, "w") as f:
            f.write(content)
        return "Successfully Wrote To File"
    except IOError as e:
        return f"erorr {e}"

def clearfile(filename, dir=""):
    file_path = os.path.join(STRPATH,dir, filename)
    with open(file_path, "w") as f:
        f.write("")

def newdir(dirname, dir=""):
    file_path = os.path.join(STRPATH,dirname, dir)
    os.mkdir(file_path)
    return "Successfuly Created Folder"


def deldir(dirname, dir=""):

    file_path = os.path.join(STRPATH,dir, dirname)
    os.rmdir(file_path)

# Others
def greet_user():
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.strftime("%I:%M %p")
    hour = datetime.now().hour

    if (hour >= 6) and (hour < 12):
        say(f"Good Morning Sir. The Date is {current_date}, At {current_time}")
    elif (hour >= 12) and (hour < 16):
        say(f"Good afternoon Sir... The Date is {current_date}, At {current_time}")
    elif (hour >= 16) and (hour < 19):
        say(f"Good Evening Sir. The Date is {current_date}, At {current_time}")
    else:
        say(f"Hello Sir... The Date is {current_date}, At {current_time}")

def say_goodbye():
    say(f"Goodbye Sir.")


def my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def randomadvice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

def current_time():
    # Get the current time
    current_time = datetime.now()

    # Format the time as a string in 12-hour format with AM/PM
    formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p")

    return formatted_time

import speedtest

def internet_speed():
    try:
        st = speedtest.Speedtest()
        say("Testing Internet.")

        # Perform the download speed test
        download_speed = st.download() / 1000000  # Convert to Mbps

        # Perform the upload speed test
        upload_speed = st.upload() / 1000000  # Convert to Mbps

        # Print the results
        result = "Download Speed: {:.2f} Mbps\n".format(download_speed)
        result += "Upload Speed: {:.2f} Mbps".format(upload_speed)
        return result

    except speedtest.SpeedtestException as e:
        print("An error occurred during the speed test:", str(e))


def run_script(file_name, dir=""):
    file_path = os.path.join(STRPATH,dir,file_name)
    try:
        os.system(f'python {file_path}')
    except Exception as e:
        print(f"Error running Python script '{file_path}': {e}")

def search_yt(prompt):
    textToSearch = prompt
    videosSearch = VideosSearch(textToSearch, limit=5)

    results = videosSearch.result()
    videos = []
    for video in results['result']:
        title = video['title']
        link = video['link']
        videos.append(f"Title: {title}\nLink: {link}\n")
    return '\n'.join(videos)

