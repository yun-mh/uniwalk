import cv2
import os
from django.conf import settings
import numpy as np


def analyze(target):
    # A4紙のサイズ宣言
    a4_width = 210
    a4_height = 297

    # イメージの呼び出し
    image = os.path.join(settings.MEDIA_ROOT, str(target))

    win_name = "scan"
    img = cv2.imread(image)
    cv2.imshow("origin", img)
    cv2.waitKey(0)

    blur = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imshow(win_name, blur)
    cv2.waitKey(0)

    imgray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    cv2.imshow(win_name, th)
    cv2.waitKey(0)

    contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr = contours[0]

    x, y, w, h = cv2.boundingRect(contr)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)

    cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # med_val = np.median(gray)
    # lower = int(max(0, 0.7 * med_val))
    # upper = int(min(255, 1.3 * med_val))

    # edged = cv2.Canny(gray, 75, 200)
    # cv2.imshow(win_name, edged)
    # cv2.waitKey(0)

    # (cnts, _) = cv2.findContours(
    #     edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    # )

    # cv2.drawContours(draw, cnts, -1, (0, 255, 0))
    # cv2.imshow(win_name, draw)
    # cv2.waitKey(0)

    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    # for c in cnts:
    #     peri = cv2.arcLength(c, True)
    #     vertices = cv2.approxPolyDP(c, 0.02 * peri, True)
    #     if len(vertices) == 4:
    #         break
    # pts = vertices.reshape(4, 2)
    # for x, y in pts:
    #     cv2.circle(draw, (x, y), 10, (0, 255, 0), -1)
    # cv2.imshow(win_name, draw)
    # cv2.waitKey(0)
    # merged = np.hstack((img, draw))

    # sm = pts.sum(axis=1)
    # diff = np.diff(pts, axis=1)

    # topLeft = pts[np.argmin(sm)]
    # bottomRight = pts[np.argmax(sm)]
    # topRight = pts[np.argmin(diff)]
    # bottomLeft = pts[np.argmax(diff)]

    # pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

    # w1 = abs(bottomRight[0] - bottomLeft[0])
    # w2 = abs(topRight[0] - topLeft[0])
    # h1 = abs(topRight[1] - bottomRight[1])
    # h2 = abs(topLeft[1] - bottomLeft[1])
    # width = max([w1, w2])
    # height = max([h1, h2])

    # pts2 = np.float32(
    #     [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]
    # )

    # mtrx = cv2.getPerspectiveTransform(pts1, pts2)

    # result = cv2.warpPerspective(img, mtrx, (width, height))
    # cv2.imshow(win_name, result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
