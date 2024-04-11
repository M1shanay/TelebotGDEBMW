from PIL import Image
import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
preprocess = "thresh"

def read_image_Tesseract(filepath):
  image = cv2.imread(filepath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  filename = "{}.png".format(os.getpid())
  cv2.imwrite(filename, gray)

  text = pytesseract.image_to_string(Image.open(filename))
  os.remove(filename)
  return text