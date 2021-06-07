import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
import processing as pc
from PIL import Image, ImageTk
import cv2
from crop_img import *

filepath = None
image_file = None
originimage = None
proceimage = None
contrast_index = 4
gamma = 1.0
w_box = 500
h_box = 350

def resize(w, h, w_box, h_box, pil_image):

    f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)

    return pil_image.resize((width, height), Image.ANTIALIAS)

def open_image():
    global image_file
    global filepath
    global r,b,g
    
    filepath = askopenfilename()

    image_file = Image.open(filepath)
    r,b,g = image_file.split()

    w_box = 500
    h_box = 350
    showimg(image_file, imgleft, w_box, h_box)
    showimg(image_file, imgright, w_box, h_box)

def save_image():
    global proceimage
    proceimage.save('images/processed.jpg')

def showimg(PIL_img, master, width, height):

    w, h = PIL_img.size

    img_resize = resize(w, h, width, height, PIL_img)
    Tk_img = ImageTk.PhotoImage(image=img_resize)
    master.config(image=Tk_img)
    master.image = Tk_img

def hst_eql_custom():
    global proceimage
    PIL_eq, PIL_gary = pc.hist_eql_custom(image_file)
    proceimage = PIL_eq
    w_box = 500
    h_box = 350
    showimg(PIL_gary, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)

    showimg(PIL_eq, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def hst_eql_opencv():
    global proceimage
    PIL_eq, PIL_gary = pc.hist_eql_opencv(image_file)
    proceimage = PIL_eq
    w_box = 500
    h_box = 350
    showimg(PIL_gary, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)

    showimg(PIL_eq, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def crop_image():
    global filepath

    top = tk.Toplevel(root)
    top.geometry('%sx%s' % (1100, 700))
    top.title("crop image")  
    top.configure(background='grey')

    # Default selection object options.
    SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='red',
                          outline='')
    img = ImageTk.PhotoImage(Image.open(filepath))
    canvas = tk.Canvas(top, width=img.width(), height=img.height(),
                            borderwidth=0, highlightthickness=0)
    canvas.pack(expand=True)

    canvas.create_image(0, 0, image=img, anchor=tk.NW)
    canvas.img = img  # Keep reference.

    # Create selection object to show current selection boundaries.
    selection_obj = SelectionObject(canvas, SELECT_OPTS)

    # Callback function to update it given two points of its diagonal.
    def on_drag(start, end, **kwarg):  # Must accept these arguments.
        selection_obj.update(start, end)

    # Create mouse position tracker that uses the function.
    posn_tracker = MousePositionTracker(canvas)
    posn_tracker.autodraw(command=on_drag)  # Enable callbacks.

    top.mainloop()

def convert_to_png():
    global image_file

    cv_img = pc.PIL_img2CV_img(image_file)
    png_cv_img = cv2.imwrite('images/output.png', cv_img, [cv2.IMWRITE_PNG_COMPRESSION])
    pil_img = pc.CV_img2PIL_img(png_cv_img)

    showimg(pil_img, imgright, 500, 350)

def bright_up_contrast():
    global proceimage
    global contrast_index

    new_contrast = pc.enhance_constrast(image_file, contrast_index)
    if(contrast_index < 8):
        contrast_index += 1

    proceimage = new_contrast
    w_box = 500
    h_box = 350
    showimg(image_file, imgleft, w_box, h_box)
    
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)

    showimg(new_contrast, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def bright_down_contrast():
    global proceimage
    global contrast_index

    new_contrast = pc.enhance_constrast(image_file, contrast_index)
    if(contrast_index > 1):
        contrast_index -= 1

    proceimage = new_contrast
    w_box = 500
    h_box = 350
    showimg(image_file, imgleft, w_box, h_box)

    showimg(new_contrast, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)    

def negative_transformation():
    global proceimage

    proceimage = pc.negative_img(image_file)

    w_box = 500
    h_box = 350
    showimg(image_file, imgleft, w_box, h_box)

    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_rgb():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_rgb(image_file, r, g, b)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_rbg():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_rbg(image_file, r, g, b)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_brg():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_brg(image_file, r, g, b)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_bgr():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_bgr(image_file, r, g, b)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_grb():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_grb(image_file, r, g, b)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_gbr():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_gbr(image_file, r, g, b)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def color_to_gray():
    global proceimage
    w_box = 500
    h_box = 350
    proceimage = pc.change_color_to_gray(image_file)
    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)
    showimg(proceimage, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)

def resiz(en_wid,en_hei,en_re):
    print(en_wid)
    print(en_hei)
    en_re.destroy()
    resize_img=Tk()
    resize_img.title("New img")
    image=image_file.resize((en_wid,en_hei))
    my_img = ImageTk.PhotoImage(image)
    lbl = tk.Label(resize_img, image = my_img).pack()
    resize_img.mainloop()

def resize_box():
    en_re = Tk()
    en_re.config(background="#2b2b2b")
    en_re.wm_title("Resize")
    tx_wid=Label(en_re,text="Width",font="Tahoma 12 bold",fg="white",bg='#2b2b2b')
    tx_wid.grid(row=0,pady=(10,4),padx=(20,4))
    en_wid=Entry(en_re,width=15,fg="white",bg="#2b2b2b",borderwidth=3,font="Tahoma 12",insertbackground="white")
    en_wid.grid(row=0,column=1,padx=(4,4),pady=(10,4))

    tx_hei=Label(en_re,text="Height",font="Tahoma 12 bold",fg="white",bg='#2b2b2b')
    tx_hei.grid(row=0,column=2,pady=(10,4),padx=(20,4))
    en_hei=Entry(en_re,width=15,fg="white",bg="#2b2b2b",borderwidth=3,font="Tahoma 12",insertbackground="white")
    en_hei.grid(row=0,column=3,padx=(4,20),pady=(10,4))

    en_btn=Button(en_re,text="Resize",relief='ridge',width=10,font="Tahoma 12 bold",fg="white",bg="#2b2b2b",command=lambda : resiz(int(en_wid.get()),int(en_hei.get()),en_re))
    en_btn.grid(row=1,columnspan=4,padx="5px",pady=(10,10))
   

def change_brightness(gamma_change):
    global gamma
    gamma += gamma_change
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    new_img = pc.adjust_image_gamma_lookuptable(image_file, gamma)

    showimg(image_file, imgleft, w_box, h_box)
    histO = Image.open('images/templeft.png')
    showimg(histO, histleft, w_box, h_box)

    showimg(new_img, imgright, w_box, h_box)
    histE = Image.open('images/tempright.png')
    showimg(histE, histright, w_box, h_box)


root = tk.Tk()
root.title('luongvanquyen')
root.geometry('1100x700')
root.config(bg='white')


menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Open Image', command=open_image)
filemenu.add_command(label='Save Image', command=save_image)

histogram = tk.Menu(menubar, tearoff=0)
histogram.add_command(label='Histogram equalization', command=hst_eql_custom)
histogram.add_command(label='Histogram Equalization in OpenCV', command=hst_eql_opencv)

color = tk.Menu(menubar, tearoff=0)
color.add_command(label='Negative',command=negative_transformation)
color.add_command(label='RGB',command=color_to_rgb)
color.add_command(label='RBG',command=color_to_rbg)
color.add_command(label='BRG',command=color_to_brg)
color.add_command(label='BGR',command=color_to_bgr)
color.add_command(label='GRB',command=color_to_grb)
color.add_command(label='GBR',command=color_to_gbr)
color.add_command(label='Gray',command=color_to_gray)

transforms = tk.Menu(menubar, tearoff=0)
transforms.add_command(label='Crop Image', command=crop_image)
transforms.add_command(label='Resize', command=resize_box)

contrast = tk.Menu(menubar, tearoff=0)
contrast.add_command(label='Up', command=bright_up_contrast)
contrast.add_command(label='Down', command=bright_down_contrast)

brightness = tk.Menu(menubar, tearoff=0)

brightness.add_command(label='+0.1', command=lambda : change_brightness(gamma_change=0.1))
brightness.add_command(label='+0.5', command=lambda : change_brightness(gamma_change=0.5))
brightness.add_command(label='+1', command=lambda : change_brightness(gamma_change=1.0))
brightness.add_command(label='-0.1', command=lambda : change_brightness(gamma_change=-0.1))
brightness.add_command(label='-0.5', command=lambda : change_brightness(gamma_change=-0.5))
brightness.add_command(label='-1', command=lambda : change_brightness(gamma_change=-1.0))

menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Histogram', menu=histogram)
menubar.add_cascade(label='Color', menu=color)
menubar.add_cascade(label='Contrast', menu=contrast)
menubar.add_cascade(label='Brightness', menu=brightness)
menubar.add_cascade(label='Transforms', menu=transforms)


frm = tk.Frame(root, bg='white')
frm.pack()
frm_left = tk.Frame(frm, bg='white')
frm_right = tk.Frame(frm, bg='white')
frm_left.pack(side='left')
frm_right.pack(side='right')

imgleft = tk.Label(frm_left, bg='white')
histleft = tk.Label(frm_left, bg='white')

imgright = tk.Label(frm_right, bg='white')
histright = tk.Label(frm_right, bg='white')
imgleft.pack()
histleft.pack()
imgright.pack()
histright.pack()

root.config(menu=menubar)
root.mainloop()
