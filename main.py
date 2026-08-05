import tkinter as tk
from PIL import Image, ImageTk
import cv2
import random
import numpy as np
import classes
from tkinter import filedialog
import sys, os

# פונקציה למציאת נתיב נכון (גם בתוך exe)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


file_path = None   

print("tamar")

window = tk.Tk()
window.title("פאזל")
window.minsize(500,800)
new_label = tk.Label(window, text="ברוכים הבאים למשחק פאזל\n בחרו תמונה למשחק") 
new_label.grid(row=0, column=0, columnspan=2, pady=10)

# טעינת התמונות דרך resource_path
img1 = Image.open(resource_path('pic/baice.jpg'))
img1 = img1.resize((200, 130)) 
pic1 = ImageTk.PhotoImage(img1)
btn = tk.Button(window, image=pic1, command=lambda p='baice.jpg': beginGame(resource_path("pic/"+p)))
btn.image = pic1
btn.grid(row=1, column=0, padx=5, pady=5)

img1 = Image.open(resource_path('pic/forest.jpg'))
img1 = img1.resize((200, 130)) 
pic1 = ImageTk.PhotoImage(img1)
btn = tk.Button(window, image=pic1, command=lambda p='forest.jpg': beginGame(resource_path("pic/"+p)))
btn.image = pic1
btn.grid(row=1, column=1, padx=5, pady=5) 

img1 = Image.open(resource_path('pic/park.jpg'))
img1 = img1.resize((200, 130)) 
pic1 = ImageTk.PhotoImage(img1)
btn = tk.Button(window, image=pic1, command=lambda p='park.jpg': beginGame(resource_path("pic/"+p)))
btn.image = pic1
btn.grid(row=2, column=0, padx=5, pady=5)

img1 = Image.open(resource_path('pic/train.jpg'))
img1 = img1.resize((200, 130)) 
pic1 = ImageTk.PhotoImage(img1)
btn = tk.Button(window, image=pic1, command=lambda p='train.jpg': beginGame(resource_path("pic/"+p)))
btn.image = pic1
btn.grid(row=2, column=1, padx=5, pady=5) 

def openWindow():
    global file_path
    file_path = filedialog.askopenfilename(
        title="בחר תמונה",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    beginGame(file_path)
    print(file_path)

label = tk.Label(window, text=f"או בחר תמונה ")
label.grid(row=3, column=0, columnspan=2, pady=10)
botn = tk.Button(window, text="בחר תמונה", command=openWindow)
botn.grid(row=4, column=0, columnspan=2, pady=10)

label = tk.Label(window, text=f" בחר לכמה חלקים לחלק\n לאורך")
label.grid(row=5, column=0, columnspan=2, pady=10)

entry1 = tk.Entry(window)
entry1.insert(0,'?')
entry1.grid(row=6, column=0, columnspan=2, pady=10)

label = tk.Label(window, text=f" לרוחב")
label.grid(row=7, column=0, columnspan=2, pady=10)

entry2 = tk.Entry(window)
entry2.insert(0,'?')
entry2.grid(row=8, column=0, columnspan=2, pady=10)


currPic='train.jpg'
def beginGame(pic):
    global currPic
    currPic=pic


countWidth = 5
countHeight = 4

def handle_input():
    global countWidth,countHeight
    countHeight = entry1.get()
    print(" hהמשתמש הקליד:", countHeight)
    countWidth = entry2.get()
    print(" wהמשתמש הקליד:", countWidth)
    # source = entry.get()
    # if source:
    #     beginGame(source)
    try:
        countHeight = int(entry1.get())
        countWidth = int(entry2.get())
        window.destroy()
        start()
    except ValueError:
        print("הכנס מספרים תקינים בלבד")


button = tk.Button(window, text="שחק", command=handle_input)
button.grid(row=9, column=0, columnspan=2)

screen=None
mat=None
resultMat=None
resultRefs=None
photo_refs = None
grayPic=None
pinkPic=None
count=0
countSuccess=0
def start():
    global firstClick, mat, resultMat, resultRefs,screen
    global countWidth,countHeight, currPic, grayPic,pinkPic
    currPic = cv2.imread(resource_path(picName))
    screen = tk.Tk()
    screen.title("פאזל")
    screen.minsize(700,1000)
 
    pil_img = Image.open(currPic).convert("RGB")
    img = np.array(pil_img)[:, :, ::-1]  # הופך מ-RGB ל-BGR בשביל OpenCV
    # img = cv2.imread(currPic)
    height, width = img.shape[:2]
    height = int(height / (width / 500))
    width = 500
    print("Width:", width)
    print("Height:", height)
    img = cv2.resize(img, (width, height))

    mat = [[0 for _ in range(countWidth)] for _ in range(countHeight)]
    partWidth = int(width/countWidth)
    partHeight = int(height/countHeight)

    for i in range(countHeight):
        for j in range(countWidth):
            mat[i][j] = {"key": (i, j, 1), "pic": img[i*partHeight : (i+1)*partHeight , j*partWidth : (j+1)*partWidth]}
    
    label = tk.Label(screen, text=f" התאימו בין החלקים למעלה למקומם למטה")
    label.grid(row=countHeight, column=0, columnspan=3, pady=10)
    pinkPic = np.full((partHeight, partWidth, 3), (255, 150, 230), dtype=np.uint8)
    
    for j in range(countWidth):
        arr=[]
        for i in range(countHeight):
            arr.append(mat[i][j])
        random.shuffle(arr)
        for i in range(countHeight):
            mat[i][j]=arr[i]
    global photo_refs
    photo_refs = []
    for row_index, line in enumerate(mat):
        random.shuffle(line)
        row_photos = []
        for col_index, part in enumerate(line):
            pic = cv2.cvtColor(part["pic"], cv2.COLOR_BGR2RGB)
            pic_pil = Image.fromarray(pic)
            pic_tk = ImageTk.PhotoImage(pic_pil)
            key = part["key"]
            label = tk.Button(screen, image=pic_tk,command=lambda k=key: my_function(k))
            label.grid(row=row_index, column=col_index)
            part["button"] = label
            row_photos.append(pic_tk)
        photo_refs.append(row_photos)

    resultMat = [[0 for _ in range(countWidth)] for _ in range(countHeight)]

    grayPic = np.full((partHeight, partWidth, 3), 128, dtype=np.uint8)
    resultRefs = []
    for i in range(countHeight):
        row_photos = []
        for j in range(countWidth):
            pic = cv2.cvtColor(grayPic, cv2.COLOR_BGR2RGB)
            pic_pil = Image.fromarray(pic)
            pic_tk = ImageTk.PhotoImage(pic_pil)
            key = (i, j, 2)
            label = tk.Button(screen, image=pic_tk,command=lambda k=key: my_function(k))
            resultMat[i][j] = {"key": (i, j, 2), "pic": grayPic, "button": label}
            label.grid(row=i + countHeight + 1, column=j)
            row_photos.append(pic_tk)
        resultRefs.append(row_photos)


firstClick = (0, 0, 0)
def my_function(key):
    print("You clicked on key:", key)
    global firstClick, mat, resultMat, resultRefs
    global screen,grayPic,pinkPic,count,countSuccess
    a, b, c = key
    if c == 1:
        firstClick = key
        print("c = 1")
    else:
        a1, b1, c1 = firstClick
        if a1 == a and b1 == b:
            currentPart = next((cell for row in mat for cell in row if cell["key"] == (a, b, 1)), None)
            resultMat[a][b]["pic"] = currentPart["pic"]
            currentPart["pic"]=pinkPic

            new_gry = cv2.cvtColor(currentPart["pic"], cv2.COLOR_BGR2RGB)
            new_gpil = Image.fromarray(new_gry)
            new_gimgtk = ImageTk.PhotoImage(new_gpil)
            currentPart["pic"] = new_gimgtk
            currentPart["button"].configure(image=new_gimgtk)
         
            new_pic = cv2.cvtColor(resultMat[a][b]["pic"], cv2.COLOR_BGR2RGB)
            new_pil = Image.fromarray(new_pic)
            new_imgtk = ImageTk.PhotoImage(new_pil)
            resultRefs[a][b] = new_imgtk
            resultMat[a][b]["button"].configure(image=new_imgtk)
            countSuccess+=1
            if countSuccess==(countWidth*countHeight):
                seyResult()       
        else:
            count=count+1

def seyResult():
    # screen.after(1000, screen.destroy) 
    end = tk.Tk()
    end.title("תוצאות")
    end.minsize(300,400)                  
    new_label = tk.Label(end, text = f"הצלחת! כל הכבוד\n מספר פעמים שניסית ללא הצלחה: {count}" ) 
    new_label.pack()
    end.mainloop()     
    
            


window.mainloop()
screen.mainloop()