import speech
import time
import funcs
import threading
from say import say
import server
import proccess
from colorama import init
from colorama import Fore, Back, Style

init()

Running = False

def stop_script():
    global Running
    Running = False

def main():
    global Running

    # Startup
    funcs.greet_user()
    thread = threading.Thread(target=server.run_server, args=())
    thread.start()

    time.sleep(2)

    # Main Loop
    while Running: 
        text = input(Fore.GREEN + "User: " + Style.RESET_ALL)
        if text == "" or text == " ":
            print("Ignore")
        else:
            output = proccess.process(text)
            print(Fore.CYAN + "Jarvis: "+output + Style.RESET_ALL)


        time.sleep(0.5)
        if Running == False:
            break

    # On Shutdown
    print("Stopping")
    funcs.say_goodbye()

if __name__ == "__main__":
    Running = True
    main()
