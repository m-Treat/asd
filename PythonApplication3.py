from PyQt5 import QtWidgets,QtGui,QtCore
from lab import Ui_MainWindow1 
import sys,time,datetime,urllib.request,threading,psutil,time
from pynput import keyboard
from win32.win32gui import GetForegroundWindow,GetWindowText



def Hidebuttons(x):
        for y in x:
            btnindex = x.index(y)
            x[btnindex].hide()
  
def buttonimage(x):
        current_time = datetime.datetime.utcnow()
        url = "https://www.poelab.com/wp-content/labfiles/"+str(current_time.year)+"-"+str(current_time.strftime("%m"))+"-"+str(current_time.strftime("%d"))+diff[x]
        data = urllib.request.urlopen(url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        uipicture.setPixmap(QtGui.QPixmap(image))

class mywindow1(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow1, self).__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.btn1Clicked)
        self.ui.pushButton_2.clicked.connect(self.btn2Clicked)
        self.ui.pushButton_3.clicked.connect(self.btn3Clicked)
        self.ui.pushButton_4.clicked.connect(self.btn4Clicked)
        self.ui.pushButton_5.clicked.connect(self.btn5Clicked)
        global buttons,diff,uipicture
        uipicture = self.ui.picture
        diff = ["_normal.jpg","_cruel.jpg","_merciless.jpg","_uber.jpg"]
        buttons = [self.ui.pushButton,self.ui.pushButton_2,self.ui.pushButton_3,self.ui.pushButton_4]
        for dif in diff:
                current_time = datetime.datetime.utcnow()
                url = "https://www.poelab.com/wp-content/labfiles/"+str(current_time.year)+"-"+str(current_time.strftime("%m"))+"-"+str(current_time.strftime("%d"))+dif
                difindex = diff.index(dif)
                buttons[difindex].setStyleSheet("background-color: green")
                try:
                    code = urllib.request.urlopen(url)
                except urllib.error.HTTPError as err:
                    if err.code > 400:
                        buttons[difindex].setStyleSheet("background-color: red")
                        buttons[difindex].setEnabled(False)
                    else:
                        pass




    def btn1Clicked(self):
        global apphidden
        buttonimage(0)
        Hidebuttons(buttons)
        apphidden = 1
        application.hide()
        
    def btn2Clicked(self):
        global apphidden
        buttonimage(1)
        Hidebuttons(buttons)
        apphidden = 1
        application.hide()

    def btn3Clicked(self):
        global apphidden
        buttonimage(2)
        Hidebuttons(buttons)
        apphidden = 1
        application.hide()

    def btn4Clicked(self):
        global apphidden
        buttonimage(3)
        Hidebuttons(buttons)
        apphidden = 1
        application.hide()
        

    def btn5Clicked(self):
        global apphidden
        apphidden = 1
        application.hide()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

POErunning=0

while POErunning == 0:
    for process in psutil.process_iter():
            try:
                if "pathofexile" in process.name().lower():
                    POErunning = 1
            except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                time.sleep(1)
                



global application
apphidden = 2           
app = QtWidgets.QApplication([])
application = mywindow1()
application.show()
application.hide()

def on_press(key):
    global apphidden
    activewindow = GetWindowText(GetForegroundWindow())
    if key == keyboard.Key.tab and apphidden == 0 and "Path of Exile" in activewindow:
            application.hide()
            apphidden = 1
    elif key == keyboard.Key.tab and apphidden == 1 and "Path of Exile" in activewindow:
            application.show()
            apphidden = 0
def listener():
    listener1 = keyboard.Listener(on_press=on_press)
    listener1.start()


poepath = ""
def readfile():
    global poepath
    if poepath == "":
        for process in psutil.process_iter():
            tmppath = ""
            if "pathofexile" in process.name().lower(): 
                try:
                    exepath = psutil.Process(process.pid).exe()
                    for a in str(exepath).split("\\")[:-1]:
                        tmppath=tmppath+a+"\\"
                        poepath = tmppath+"logs\Client.txt"
                except:
                    pass
    #print(poepath)
    with open(poepath,"r",encoding="utf8") as l:
        tmpline = l.readlines()[-1]
    return tmpline


tmplog = ""

def logloop():   
    while True:
        if POErunning == 1:
            global tmplog
            log = readfile()
            if tmplog != log:
                print(str(log))
                locations = ["Aspirants' Plaza",'Basilica Annex','Basilica Atrium','Basilica Halls','Basilica Passage','Domain Crossing','Domain Enclosure','Domain Path','Domain Walkways','Estate Crossing','Estate Enclosure','Estate Path','Estate Walkway','Mansion Annex','Mansion Atrium','Mansion Halls','Mansion Passage','Sanitorium Annex','Sanitorium Atrium','Sanitorium Halls','Sanitorium Passage','Sepulchre Annex','Sepulchre Atrium','Sepulchre Halls','Sepulchre Passage',"Aspirant's Trial"]
                if "You have entered Aspirants' Plaza" in log:
                    application.show()
                else:
                    for loc in locations:
                        if "You have entered" in log and str(loc) not in log and apphidden != 2:
                            app.quit()
                            break
            tmplog = log
            time.sleep(1)
t2 = threading.Thread(target=listener)
t = threading.Thread(target=logloop)
t.start()
t2.start()


sys.exit(app.exec_())
 



