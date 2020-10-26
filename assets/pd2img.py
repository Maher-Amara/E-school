import os
import fitz
from PIL import Image, ImageTk
from io import BytesIO

def pdf2img(page_nbr):
    pdfName = "Cours arduino + TP.pdf"
    pdfPath = "PdfFiles/"
    doc = fitz.open(pdfPath + pdfName)
    zoom_x = 2  # horizontal zoom
    zomm_y = 2  # vertical zoom
    stream = BytesIO(doc.loadPage(page_nbr).getPixmap(matrix=fitz.Matrix(zoom_x, zomm_y)).getPNGData())
    img = Image.open(stream)
    img.show()

pdf2img(2)


def adapt():
    # full screan
    CanvHeight = 610
    CanvWidth = 1232

    old = "assets/old"
    Currnet = "assets/CurrnetPDF/"

    page_list = list()
    for page in os.listdir(old):
        image = Image.open(old + '/' + page, mode='r')
        Width, Height = image.size
        new_image = image.copy()
        if Width > CanvWidth:
            new_image = image.copy()
            new_image.thumbnail((CanvWidth, Height))  # duble check

        Width1, Height1 = new_image.size
        img_list = list()
        if Height1 > CanvHeight:
            pas = 100
            s = 0
            i = 0
            while s + CanvHeight < Height1:
                box = (0, s, Width1, s + CanvHeight)
                image_temp = new_image.crop(box)
                ch = ' ' + '0' * (2 - len(str(i))) + str(i)
                image_temp.save(Currnet + page[:-4] + ch + ".png")
                img_list += [Currnet + page[:-4] + ch + ".png"]
                s += pas
                i += 1
            box = (0, Height1 - CanvHeight, Width1, Height1)
            image_temp = new_image.crop(box)
            ch = ' ' + '0' * (2 - len(str(i))) + str(i)
            image_temp.save(Currnet + page[:-4] + ch + ".png")
            img_list += [Currnet + page[:-4] + ch + ".png"]
        else:
            new_image.save(Currnet + page)
            img_list += [Currnet + page]
        page_list += [img_list]
    return page_list




# print(new_image.size)
# new_image.show()
# new_image = image.resize((400, 400))  # return resized image with no repect to ratio
# new_image = image.thumbnail((400, 400))  # return resized image with no repect to ratio
# box = (150, 200, 600, 600)
# cropped_image = image.crop(box)
