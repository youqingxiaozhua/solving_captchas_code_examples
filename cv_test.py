# coding: utf-8
import math

import cv2


# import Image
# import pytesseract
import imutils


def del_noise(im_cut):
    """
    variable：bins：灰度直方图bin的数目
                  num_gray:像素间隔
    method：1.找到灰度直方图中像素第二多所对应的像素，即second_max,因为图像空白处比较多所以第一多的应该是空白，第二多的才是我们想要的内容。
            2.计算mode
            3.除了在mode+-一定范围内的，全部变为空白。
    """
    bins = 3
    delta = 60
    num_gray = math.ceil(256 / bins)
    a = cv2.medianBlur(im_cut, 1)
    # cv2.imshow('a', a)
    # b = cv2.GaussianBlur(im_cut, (3, 3), 0)
    # cv2.imshow('b', b)
    im_cut = a
    hist = cv2.calcHist([im_cut], [0], None, [bins], [0, 256])
    lists = []
    for i in range(len(hist)):
        # print hist[i][0]
        lists.append(hist[i][0])
    second_max = sorted(lists)[-2]
    bins_second_max = lists.index(second_max)

    mode = (bins_second_max + 0.5) * num_gray

    for i in range(len(im_cut)):
        for j in range(len(im_cut[0])):
            a = im_cut[i][j]
            if not (mode - delta) < a[0] < (mode + delta):
                # print im_cut[i][j]
                im_cut[i][j] = 255
    # cv2.imshow('before', im_cut)
    im_cut = cv2.cvtColor(im_cut, cv2.COLOR_BGR2GRAY)
    im_cut = cv2.GaussianBlur(im_cut, (3, 3), 0)
    im_cut = cv2.threshold(im_cut, 200, 255, cv2.THRESH_BINARY_INV)[1]
    return im_cut


def image_segment(image):
    contours = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # # cv2.drawContours(thresh, contours, -1, (0, 0, 255), 3)
    #
    # cv2.imshow("img", thresh)

    # Hack for compatibility with different OpenCV versions
    contours = contours[1] if imutils.is_cv3() else contours[0]

    letter_image_regions = []

    # Now we can loop through each of the four contours and extract the letter
    # inside of each one
    big_region = []
    for index, contour in enumerate(contours):
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        if w <= 2 or h <= 2 or w * h <= 40:
            continue
        if w <= 10 and h <= 10:
            continue

        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        if w / h > 1.4:
            big_region.append((contour, index))
        else:
            letter_image_regions.append((x, y, w, h))
    if len(big_region) * 2 + len(letter_image_regions) == 4:
        for contour, index in big_region:
            (x, y, w, h) = cv2.boundingRect(contour)
            half_width = int(w / 2)
            letter_image_regions.insert(index, (x, y, half_width, h))
            letter_image_regions.insert(index + 1, (x + half_width, y, half_width, h))
    else:
        for contour, index in big_region:
            (x, y, w, h) = cv2.boundingRect(contour)
            letter_image_regions.insert(index, (x, y, w, h))

    # if len(letter_image_regions) != 4:
    #     for x, y, w, h in letter_image_regions:
    #         cv2.rectangle(image, (x - 2, y - 2), (x + w + 4, y + h + 4), (255, 0, 0), 1)
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])
    return letter_image_regions


if __name__ == '__main__':
    src = cv2.imread("captcha_images/xuanwu/2qck.jpg")
    # src = cv2.imread("captcha_images/xuanwu/usjt.jpg")
    # cv.imshow("原来", src)
    im = del_noise(src)
    cv2.imshow('threshold', im)
    border = image_segment(im)
    for x,y,w,h in border:
        cv2.rectangle(src, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
    cv2.imshow('border', src)
    print(border)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

