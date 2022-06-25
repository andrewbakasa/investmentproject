from django.db import models
from django.urls import reverse

from trading.models import Investment
from django.contrib.auth.models import User
# Create your models here.
class InvestmentBlog(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   	
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.investment) 

class BlogItem(models.Model):
    investmentblog = models.ForeignKey(InvestmentBlog, on_delete=models.SET_NULL, null=True) 
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Post Content',null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return str(self.title) 


  
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk':self.pk})

 