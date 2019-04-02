from django.shortcuts import render

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
