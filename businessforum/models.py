from django.db import models
from django.urls import reverse

from trading.models import Investment
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
#from comment.models import Comment
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

         # comment app
    #comments = GenericRelation(Comment)
    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return str(self.title) 


  
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk':self.pk})

 
    @property
    def comments_count(self):
        #comments_qs = Comment.objects.filter_parents_by_object(self) 
        
        return  10#comments_qs.count()
    
    @property
    def comments_count_attr(self):
        #comments_qs = Comment.objects.filter_parents_by_object(self) 
        x= 0#comments_qs.count()
        if x>0:
            return  f'| {x} comment(s)'
        else:
            return ''
    #comments_qs = Comment.objects.filter_parents_by_object(obj) 

    """ 
    data = pd.DataFrame({"x1":range(5, 10),          # Create pandas DataFrame
                     "x2":["a", "b", "c", "d", "e"],
                     "x3":range(10, 5, - 1)})
    print(data)   
    
    """    