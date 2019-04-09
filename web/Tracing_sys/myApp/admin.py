from django.contrib import admin

# Register your models here.
from .models import poems

#注册
@admin.register(poems)
class poemsAdmin(admin.ModelAdmin):
     # 列表页属性
    list_display = ['pk','title','author','poem_body','dynasty','tac','appreciation'
        ,'background','self_intro']
    list_filter = ['title']
    search_fields = ['title']
    list_per_page = 5
    # 添加、修改页属性
    # fields = ['title','poem_body','author','tac','dynasty']
    fieldsets = [
        ("num",{"fields":['title','author','poem_body']}),
        ("base",{"fields":['dynasty','tac','appreciation' ,'background','self_intro']}),
    ]
# admin.site.register(poems,poemsAdmin)
