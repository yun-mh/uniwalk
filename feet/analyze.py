from django.conf import settings
import cv2
import os
import math
import numpy as np


def analyze(target):
    # A4紙のサイズ宣言
    a4_width = 210
    a4_height = 297
    img_width = 500
    img_height = 707

    # イメージの呼び出し
    image = os.path.join(settings.MEDIA_ROOT, str(target))

    win_name = "scan"
    img = cv2.imread(image)
    cv2.imshow("origin", img)
    cv2.waitKey(0)

    blur = cv2.GaussianBlur(img, (7, 7), 0)
    cv2.imshow(win_name, blur)
    cv2.waitKey(0)

    imgray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(imgray, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow(win_name, th)
    cv2.waitKey(0)

    contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr = contours[0]

    x, y, w, h = cv2.boundingRect(contr)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)
    cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
    cv2.circle(img, (x + w, y + h), 3, (0, 255, 0), -1)

    cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    width_result = math.ceil(w / img_width * a4_width)
    height_result = math.ceil(h / img_height * a4_height)

    print(width_result, height_result)
    return height_result, width_result
