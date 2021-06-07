import cv2
import numpy as np
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt

def PIL_img2CV_img(PILimg):
    CVimg = cv2.cvtColor(np.asarray(PILimg), cv2.COLOR_RGB2BGR)
    return CVimg

def CV_img2PIL_img(CVimg):
    PILimg = Image.fromarray(cv2.cvtColor(CVimg, cv2.COLOR_BGR2RGB))
    return PILimg

def hist_eql_opencv(pil_img):
    cv_img = PIL_img2CV_img(pil_img)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    save_hist(gray, 'left', 'Origin')
    CV_img_eq = cv2.equalizeHist(gray)
    save_hist(CV_img_eq, 'right', 'Histogram equalization in opencv')

    CV_img_eq = cv2.cvtColor(CV_img_eq, cv2.COLOR_GRAY2BGR)
    CV_img_gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    PIL_img_gray = CV_img2PIL_img(CV_img_gray)
    PIL_img_eq = CV_img2PIL_img(CV_img_eq)
    return PIL_img_eq, PIL_img_gray

def save_hist(cv_img, side, title):
    hist = cv2.calcHist([cv_img], [0], None, [256], [0, 256])

    f = plt.figure()
    plt.title(title)
    # plt.xlabel("Bins")
    # plt.ylabel("# of Pixels")
    plt.plot(hist)
    plt.xlim([0, 256])

    plt.savefig('images/temp'+side)
    plt.close()

def save_color_hist(cv_img, side, title):
    color = ('b', 'g', 'r')

    f = plt.figure()
    plt.title(title)
    for i, col in enumerate(color):
        
        histr = cv2.calcHist([cv_img],
                            [i], None, 
                            [256],
                            [0, 256])
        
        plt.plot(histr, color = col)
        plt.xlim([0, 256])
        
    plt.savefig('images/temp'+side)
    plt.close()

def hist_eql_custom(pil_img):
    cv_img = PIL_img2CV_img(pil_img)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    save_hist(gray, 'left', 'Origin')
    
    img_eq = gray.copy()
    histogram = create_histogram(img_eq)
    CV_img_eq = equalize_histogram(img_eq, histogram)

    save_hist(CV_img_eq, 'right', 'Histogram equalization')

    CV_img_eq = cv2.cvtColor(CV_img_eq, cv2.COLOR_GRAY2BGR)
    CV_img_gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    PIL_img_gray = CV_img2PIL_img(CV_img_gray)
    PIL_img_eq = CV_img2PIL_img(CV_img_eq)
    return PIL_img_eq, PIL_img_gray

def create_histogram(img):
    assert len(img.shape) == 2 # check grayscale image
    histogram = [0] * 256 # list of intensity frequencies, 256 zero values
    for row in range(img.shape[0]): # traverse by row (y-axis)
        for col in range(img.shape[1]): # traverse by column (x-axis)
            histogram[img[row, col]] += 1
    return histogram

def equalize_histogram(img, histogram):
    # build H', cumsum
    new_H = [0] * 257
    for i in range(0, len(new_H)):
        new_H[i] = sum(histogram[:i])
    new_H = new_H[1:]
    
    # scale H' to [0, 255]
    max_value = max(new_H)
    min_value = min(new_H)
    new_H = [int(((f-min_value)/(max_value-min_value))*255) for f in new_H]

    # apply H' to img
    for row in range(img.shape[0]): # traverse by row (y-axis)
        for col in range(img.shape[1]): # traverse by column (x-axis)
            img[row, col] = new_H[img[row, col]]
    return img

def enhance_constrast(img, i):
    img_cv2 = PIL_img2CV_img(img)
    save_hist(img_cv2, 'left', 'Origin')

    enhancer = ImageEnhance.Contrast(img)
    factor = i / 4.0
    new_img = enhancer.enhance(factor)
    new_img_cv2 = PIL_img2CV_img(new_img)

    save_hist(new_img_cv2, 'right', 'new constrast')

    return new_img

def negative_img(img):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img_neg = 1 - img_cv2
    PIL_img_eq = CV_img2PIL_img(img_neg)
    save_color_hist(img_neg, 'right', 'Negative Image')

    return PIL_img_eq

def change_color_to_rgb(img, r, g, b):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img = Image.merge("RGB",(r,g,b))

    new_img = PIL_img2CV_img(img)
    save_color_hist(new_img, 'right', 'RBG')

    return img

def change_color_to_rbg(img, r, g, b):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img = Image.merge("RGB",(r,b,g))

    new_img = PIL_img2CV_img(img)
    save_color_hist(new_img, 'right', 'RBG')

    return img

def change_color_to_brg(img, r, g, b):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img = Image.merge("RGB",(b,r,g))

    new_img = PIL_img2CV_img(img)
    save_color_hist(new_img, 'right', 'BRG')

    return img

def change_color_to_bgr(img, r, g, b):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img = Image.merge("RGB",(b,g,r))

    new_img = PIL_img2CV_img(img)
    save_color_hist(new_img, 'right', 'BGR')

    return img

def change_color_to_grb(img, r, g, b):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img = Image.merge("RGB",(g,r,b))

    new_img = PIL_img2CV_img(img)
    save_color_hist(new_img, 'right', 'GRB')

    return img

def change_color_to_gbr(img, r, g, b):

    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')

    img = Image.merge("RGB",(g,b,r))

    new_img = PIL_img2CV_img(img)
    save_color_hist(new_img, 'right', 'GBR')

    return img

def change_color_to_gray(img):
    img_cv2 = PIL_img2CV_img(img)
    save_color_hist(img_cv2, 'left', 'Origin')
    pixels = img.load()
    
    new_img = Image.new(img.mode, img.size)

    pixels_new = new_img.load()
    for i in range(new_img.size[0]):
        for j in range(new_img.size[1]):
            r, b, g = pixels[i,j]
            avg = int(round((r + b + g) / 3))
            pixels_new[i,j] = (avg, avg, avg, 0)

    new_img_pil = PIL_img2CV_img(new_img)
    save_hist(new_img_pil, 'right', 'Gray')

    return new_img

def adjust_image_gamma_lookuptable(image, gamma=1.0):

    img_cv2 = PIL_img2CV_img(image)
    save_color_hist(img_cv2, 'left', 'Origin')
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    table = np.array([((i / 255.0) ** gamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    new_img =  cv2.LUT(img_cv2, table)
    save_color_hist(new_img, 'right', gamma)

    PIL_img = CV_img2PIL_img(new_img)
    return PIL_img