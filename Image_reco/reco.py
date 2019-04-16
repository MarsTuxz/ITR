from PIL import Image
import pytesseract
import scipy.misc as misc
import os

class Image_rec(object):
        def size_change(self, address):
                img = misc.imread(address)
                (w, h, n) = img.shape
                if w > 150:
                        w = int(w * 0.3)
                        h = int(h * 0.3)
                        img = misc.imresize(img, (w, h, 3), interp='bilinear')
                        misc.imsave(address, img)
                        print("size changed")
                else:
                        print("size dont need to change")

        def alpha(self,address):
                #转换图片格式为RGBA
                img = Image.open(address)
                img = img.convert("RGBA")
                datas = img.getdata()
                newData = list()
                #通道化
                for item in datas:
                        if item[0] > 100 or item[1] > 100 or item[2] > 100:
                                newData.append((255, 255, 255, 0))
                        else:
                                newData.append((0, 0, 0, 255))
                img.putdata(newData)
                img.save(address)

        def feedbackWord(self,address):
                text = pytesseract.image_to_string(Image.open(address), lang='chi_sim').replace("\n","").replace(" ", "")
                print("feedbackWord function end")
                return text

if __name__ == '__main__':
        address = "a16.jpg"
        # 更改后缀名，转换jpg/jpeg为png
        medi = address
        address = address.replace(".jpg", ".png").replace(".jpeg", ".png")
        os.rename(medi, address)
        #实例化，调用函数
        im = Image_rec()
        im.size_change(address)
        im.alpha(address)
        print(im.feedbackWord(address))