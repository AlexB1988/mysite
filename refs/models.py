from django.db import models
from django.urls import reverse
from captcha.fields import CaptchaField
from django.core.validators import FileExtensionValidator

class Reflist(models.Model):
    title=models.CharField(max_length=255, verbose_name='Заголовок')
    file=models.FileField(upload_to='ref_files/%Y/%m/%d', validators=[FileExtensionValidator(['pdf','doc','docx','rtf'])], verbose_name='Файл')
    time_create=models.DateTimeField(auto_now_add=True)
    cat=models.ForeignKey('Category', on_delete=models.PROTECT,verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('work', kwargs={'work_id':self.pk})

    class Meta:
        verbose_name='Список работ'
        verbose_name_plural='Список работ'
        ordering=['-time_create']


class Category(models.Model):
    name=models.CharField(max_length=100,db_index=True, verbose_name='Категория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name='Категории'
        verbose_name_plural='Категории'

class Contact(models.Model):
    name=models.CharField(max_length=255,verbose_name='Имя')
    email=models.EmailField(verbose_name='Email')
    content=models.TextField(max_length=1000,verbose_name='Содержание')
   # captcha=CaptchaField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Форма обратной связи'
        verbose_name_plural='Формы обратной связи'