from PIL import Image
import pytesseract
class Image_rec(object):
    def feedbackWord(self,address):
        text = pytesseract.image_to_string(Image.open(address), lang='chi_sim').replace(" ", "")
        return text