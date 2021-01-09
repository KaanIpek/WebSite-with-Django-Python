from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class CaseInsensitiveFieldMixin:

    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
        'gt' :'>',
        'gte':'>=',
        'lt':'<',
        'lte':'<=',


            }
    def get_lookup(self, lookup_title):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_title, lookup_title)
        return super().get_lookup(converted)

class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass
class CIEmailField(CaseInsensitiveFieldMixin, models.EmailField):
    pass

class Job(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,default="",verbose_name="İşi Veren Kişi")
    title = CICharField(max_length=50,default="",verbose_name="Başlık")
    district = models.CharField(max_length=20,default="",verbose_name="İlçe")
    location = models.CharField(max_length=50,default="",verbose_name="Konum")
    fee = models.CharField(max_length=50,default="",verbose_name="Ödenecek Ücret")
    email = models.CharField(max_length=50,default="",verbose_name="E-Mail")
    telno = models.CharField(max_length=20,default="",verbose_name="Telefon Numarası")
    content = RichTextField(verbose_name="Bilgiler")
    created_date =models.DateTimeField(auto_now_add=True,verbose_name="Tarih")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,verbose_name="İş",related_name="comments")
    comment_author= models.CharField(max_length=50,verbose_name="İsim")
    comment_content = models.CharField(max_length=200,verbose_name="Yorum")
    rate = models.IntegerField(default=0)
    comment_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']

