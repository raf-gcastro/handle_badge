#! -*- encoding: utf-8 -*-

from sys import argv, exit
import numpy as np
import cv2


def read_image(img_filename):
    orig = cv2.imread(img_filename, cv2.IMREAD_COLOR)
    img = cv2.imread(img_filename, cv2.IMREAD_GRAYSCALE)

    return img, orig

def remove_borders(img):
    xs,ys = np.where(img < 250)

    return min(xs), max(xs)+1, min(ys), max(ys)+1

def cut_image(img, min_x, max_x, min_y, max_y):
    return img[min_x:max_x,min_y:max_y]

def save_image(output_filename, orig):
    cv2.imwrite(output_filename, orig)

def redistribute(img):
    h, w = img.shape[0:2]

    if (h == w): return img
    elif (w > h):
        diff = w - h
        vect = np.full((1,w,3),255)
        for i in range(int(diff/2)):
            img = np.append(img, vect, axis=0)
        for i in range(diff/2,diff):
            img = np.append(vect, img, axis=0)
    else:
        diff = h - w
        vect = np.full((h,1,3),255)
        for i in range(int(diff/2)):
            img = np.append(img, vect, axis=1)
        for i in range(int(diff/2),diff):
            img = np.append(vect, img, axis=1)

    return img

def main(argv):
    if (len(argv) != 3):
        print('Usage:', argv[0], '<path/to/img.[png|jpg|jpeg]>', '<path/to/output.png>')
        exit (-1)

    img_filename = argv[1]
    output_filename = argv[2]

    img, orig = read_image(img_filename)
    min_x, max_x, min_y, max_y = remove_borders(img)
    orig = cut_image(orig, min_x, max_x, min_y, max_y)
    orig = redistribute(orig)
    save_image(output_filename, orig)

    return 0

if (__name__ == '__main__'):
    main(argv)
