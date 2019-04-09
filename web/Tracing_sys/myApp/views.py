from django.shortcuts import render
from PIL import Image
import pytesseract
import scipy.misc as misc

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("poems")
def detail(request,num,num2):
    return HttpResponse("detail-%s-%s"%(num,num2))

from .models import poems
def tracing_poems(request):
    #获取诗词数据
    poemsList = poems.objects.all()
    #将数据返回给页面
    return render(request,'myApp/poems.html',{"poems":poemsList})
def showsearch(request):
    return render(request,'myApp/poems.html')
def search(request):
    print('ok*****')
    picture = request.FILES.get('picture')
    print(type(picture))
    print(picture)
    print(Image.open(picture))

    class Image_rec(object):
        def size_change(self, address):
            img = misc.imread(address)
            (w, h, n) = img.shape
            w = int(w * 0.3)
            h = int(h * 0.3)
            img = misc.imresize(img, (w, h, 3), interp='bilinear')
            misc.imsave(address, img)
            print("size_change function end")

        def feedbackWord(self, address):
            text = pytesseract.image_to_string(Image.open(address), lang='chi_sim').replace(" ", "")
            print("feedbackWord function end")
            return text
    print('******')
    img = Image_rec()
    print(type(picture))
    text = img.feedbackWord(picture)
    # text = pytesseract.image_to_string(Image.open(picture), lang='chi_sim').replace(" ", "")
    # print("feedbackWord function end")
    # print(text)
    poemsList = poems.objects.filter(poem_body__contains = text)
    # print(poemsList)
    return render(request,'myApp/page_list.html',{"poems":poemsList})


# def searchshow(request,num):
#     number = poems.objects.get(id=num)
#     print(number)
#     poemsList = number.objects.set.all()
#     return render(request,'myApp/poems3.html',{poems:poemsList})