import tkinter
from PIL import Image
from tkinter import filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *



def run():
    global anhbia
    anhbia.destroy()
anhbia = tkinter.Tk()
anhbia.geometry("1200x720")
# ten cua so cua anh bia
anhbia.title("Brain Tumor Detection")
# mo hinh anh bia
anh=Image.open("BIA.jpg")
# chinh kich thuoc anh bia
resizeimage=anh.resize((1200, 720))
a = ImageTk.PhotoImage(resizeimage)
img=tkinter.Label(image=a)
img.grid(column=0,row=0)
Btn=tkinter.Button(anhbia,text="RUN",font=("Times New Romen",20),command= run )
Btn.grid(column=0,row=0)
anhbia.mainloop()


class Gui:
    #Thiết lập ban đầu
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        
        #Gobal(toàn cục)
        global MainWindow
        #Tạo một cửa sổ bằng lệnh TK()
        MainWindow = tkinter.Tk()
        #kích thước
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)
        self.thresh = None


        self.DT = DisplayTumor()
        self.fileName = tkinter.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        #thêm fisrtFrame vào listOfWinFrame
        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))
        
        # mo hinh anh lena
        anh=Image.open("anhbia.png")
        # chinh kich thuoc anh lena
        resizeimage=anh.resize((500, 350))
        a = ImageTk.PhotoImage(resizeimage)
        img=tkinter.Label(image=a)
        img.place(x=50,y=320)

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=50, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check)
        RB2.place(x=50, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=700, y=600)


        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        global mriImage
        #print(mriImage)
        if (self.val.get() == 1):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)
            confidence_score_tumor = round(float(res) * 100,3)
            confidence_score_no_tumor = round(float(1 - res) * 100,3)
            print(res)
            
            if res > 0.5:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Detection Tumor", height=1, width=20)
                resLabel.configure(background="White", font=("Cambria", 20, "bold"), fg="red")

                accLabel = tkinter.Label(self.FirstFrame.getFrames(), 
                              text= ("Confidence", "Score:", confidence_score_tumor,'%'), width=24)
                accLabel.configure(background="black", font=("Cambria", 20, "bold"), fg="pink")
                accLabel.place(x=700,y=500)

            else:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="No Tumor Brain", height=1, width=20)
                resLabel.configure(background="White", font=("Cambria", 20, "bold"), fg="green")

                accLabel = tkinter.Label(self.FirstFrame.getFrames(), 
                              text= ("Confidence", "Score:", confidence_score_no_tumor,'%'), width=24)
                accLabel.configure(background="black", font=("Cambria", 20, "bold"), fg="pink")
                accLabel.place(x=700,y=500)

            resLabel.place(x=700, y=450)

        elif (self.val.get() == 2):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)


            for i in range(len(self.listOfWinFrame)):
                if (i != 0):
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if (len(self.listOfWinFrame) > 1):
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")

mainObj = Gui()