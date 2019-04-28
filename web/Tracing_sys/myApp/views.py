from collections import Counter
from django.shortcuts import render
from PIL import Image
import pytesseract
import scipy.misc as misc
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


    # text = pytesseract.image_to_string(Image.open(picture), lang='chi_sim').replace(" ", "")
    # print("feedbackWord function end")
    # print(text)

def select_title_like(words):
    '''
    查询对应的诗文的题目
    :param words: 模糊查询的文字
    :return:
    '''
    # select * from poems where poem_body like '%夜%'
    titles = []
    poems_list = poems.objects.filter(poem_body__contains=words)

    for poem in poems_list:
        titles.append(poem.title)
    print('select_title_like:', titles)
    return titles

def select_title_like_reg(words):
    '''
    查询对应的诗文的所有的内容
    :param words: 模糊查询的文字
    :return:
    '''
    # select * from poems where poem_body like '%夜%'
    titles = []
    poems_list = poems.objects.filter(poem_body__contains=words)
    for poem in poems_list:
        titles.append(poem.title)
    print('select_title_like_reg:', titles)
    return titles

def select_word_like(word):
    '''
    模糊查询的策略如下：
    先将接受文字的前两个字，前一半字，后一半字，后两个字分别作为四组子查询
    将所有的子查询的结果进行组合，获得出现次数的最多的诗名。
    :param word:
    :return:
    '''
    #将中文的逗号转为英文的逗号,并将逗号切下，只取前一句话
    word = word.replace("，",",")
    if word.count(','):
        word = word.split(',')[0]
    title = select_title_like(word)
    if title:
        if isinstance(title, (list,)):
            return title[0]
        return title
    else:
        #
        length = len(word)
        if length > 4:
            b_half = word[:length//2]
            b_two = word[:2]
            a_half = word[length//2:]
            a_two = word[-2:]
            result1 = select_title_like(b_half)
            result2 = select_title_like(b_two)
            result3 = select_title_like(a_half)
            result4 = select_title_like(a_two)
            title_list = result1+result2+result3+result4
            count_dict = get_count_by_counter(title_list)
            # 获得值最大时对应的key值
            title = max(count_dict, key=count_dict.get)

        elif length >= 3:
            b_two = word[:2]
            a_two = word[-2:]
            result1 = select_title_like(a_two)
            result2 = select_title_like(b_two)
            title_list = result1 + result2
            count_dict = get_count_by_counter(title_list)
            title = max(count_dict, key=count_dict.get)
        else:
            title_list = select_title_like_reg(word)
            count_dict = get_count_by_counter(title_list)
            title = max(count_dict, key=count_dict.get)
    if isinstance(title, (list, )):
        return title[0]
    return title


def get_count_by_counter(l):
    '''
    统计列表中的各个元素出现的次数
    :param l: 列表
    :return:
    '''
    count = Counter(l)   #类型： <class 'collections.Counter'>
    count_dict = dict(count)   #类型： <type 'dict'>
    return count_dict



def searchpoems(request):
    # au = request.POST.get('au')
    text = request.POST.get('text')
    find = request.POST.get('find')
    print(text)
    print(find)
    if (find =="dy"):
        poemsList = poems.objects.filter(dynasty__contains = text)[0:10]
    if(find =="author"):
        poemsList = poems.objects.filter(author__contains = text)[0:10]
    return  render(request,'myApp/poems2.html',{"poems":poemsList})


def searchpoems1(request,num):
    number = poems.objects.get(pk=num)
    print(number)
    poemsList = poems.objects.filter(title__contains = number)
    return render(request,'myApp/page_list.html',{"poems":poemsList})



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
    # 获得古诗的title
    title = select_word_like(text)
    print('main::', title)
    poem = poems.objects.filter(title__contains=title)
    print(poem)
    return render(request, 'myApp/page_list.html', {"poems": poem})