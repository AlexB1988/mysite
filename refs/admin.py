from django.contrib import admin

from .models import *

class ReflistAdmin(admin.ModelAdmin):
    list_display = ('id','title','file','time_create','cat')
    list_display_links = ('id','title','file')
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    search_fields = ('name',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','content')
    list_display_links = ('id','name','email','content')
    search_fields = ('email',)

admin.site.register(Reflist,ReflistAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Contact,ContactAdmin)