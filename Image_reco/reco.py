from PIL import Image
import pytesseract
import scipy.misc as misc

class Image_rec(object):
        def size_change(self, address):
                img = misc.imread(address)
                (w, h, n) = img.shape
                w = int(w * 0.3)
                h = int(h * 0.3)
                img = misc.imresize(img, (w, h, 3), interp='bilinear')
                misc.imsave(address, img)
                print("size_change function end")

        def feedbackWord(self,address):
                text = pytesseract.image_to_string(Image.open(address), lang='chi_sim').replace(" ", "")
                print("feedbackWord function end")
                return text