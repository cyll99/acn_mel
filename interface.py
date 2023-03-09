from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import os

from tensorflow.keras.models import Sequential, model_from_json
import cv2
import numpy as np

global path
path = ""

# load json and create model
json_file = open('model_01.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_01.h5")
print("Loaded model from disk")

IMG_SIZE = 180

def change_image(path):
# change the given picture into an array in order to make prediction
  img_array = cv2.imread(path ,cv2.IMREAD_GRAYSCALE)  # convert to array
  new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
  return np.array(new_array).reshape(-1,IMG_SIZE, IMG_SIZE, 1)      # reformat the features

def scan():
    
	CATEGORIES = ["acne", "melanoma"]          
	prediction = loaded_model.predict(change_image(path))
	print(path)
	print(CATEGORIES[int(prediction[0][0])])
        # the label for user_name
	result = Label(root,
                  text = CATEGORIES[int(prediction[0][0])]).place(x = 40,
                                           y = 500) 
	# result.pack()
   


def showImage():
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="select image file", 
                                     filetypes=(("JPG file", "*.jpg"), ("JPEG file", "*jpeg"),
                                                ("PNG file", "*.png"), ("All Files", "*.*")))
    result = Label(root,text = "").place(x = 40, y = 500)
    
    global path
    path = fln
    img = Image.open(fln)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img

root = Tk()
root.title("Scan me")
root.geometry("800x600")

frm = Frame(root)
frm.pack(side = BOTTOM, padx = 15, pady = 15)

lbl = Label(root)
lbl.pack()


btn = Button(frm, text="Browse", command=showImage)
btn.pack(side=LEFT)

btn = Button(frm, text="Scan", command=scan)
btn.pack(side=RIGHT)

root.mainloop()