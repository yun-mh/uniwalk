from django.conf import settings
import cv2
import os
import math
import numpy as np


# 足サイズ測定の関数
def analyze(target):
    # A4紙のサイズ宣言
    a4_width = 210
    a4_height = 297
    img_width = 500
    img_height = 707

    # イメージの呼び出し
    image = os.path.join(settings.MEDIA_ROOT, str(target))

    # 原本イメージの表示
    win_name = "scan"
    img = cv2.imread(image)
    cv2.imshow("origin", img)
    cv2.waitKey(0)

    # イメージにガウシアンブラーを入れ、ノイズを除去する
    blur = cv2.GaussianBlur(img, (7, 7), 0)
    cv2.imshow(win_name, blur)
    cv2.waitKey(0)

    # イメージをグレイスケールし、オオツ方法で２進化して黒白にする
    imgray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(imgray, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow(win_name, th)
    cv2.waitKey(0)

    # イメージから足の輪郭を分析する
    contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr = contours[0]

    # 見つけた輪郭を基に全体を囲む長方形を描画する
    x, y, w, h = cv2.boundingRect(contr)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)
    cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
    cv2.circle(img, (x + w, y + h), 3, (0, 255, 0), -1)

    # 最終結果を表示する
    cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 足の足長・足幅のサイズをA4紙のサイズを基に算出する
    width_result = math.ceil(w / img_width * a4_width)
    height_result = math.ceil(h / img_height * a4_height)

    return height_result, width_result
