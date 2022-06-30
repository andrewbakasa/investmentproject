from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from businessforum.forms import BlogItemForm
from common.decorators import admin_only
from django.contrib import messages
from investments_appraisal.models import ModelCategory, UserModel, UserPreference, UserProfile
from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.core.paginator import Paginator

from trading.forms import InvestmentROIForm, InvestmentShareholdingForm, InvestmentStrategyForm, InvestmentSummaryForm, InvestorForm, InvestorFormUpdate, InvestorStatusUpdate, UserInvestmentForm, UserInvestmentFormUpdate
from .models import *
from django.db.models.expressions import F
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group

from django.template.loader import render_to_string

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



@login_required(login_url="account_login")
def investment_blogs(request,id):
    investment = get_object_or_404(Investment,pk=id)
    investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)    
    blogsqueryset=BlogItem.objects.filter(investmentblog=investmentblog)
    # form = UserInvestmentForm(initial={'creater': request.user})
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    else:
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    pertable=request.session['pertable']
    obj_paginator = Paginator(blogsqueryset, pertable)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'current_page':current_page,
        'page_range':page_range,
        "user": request.user,
        "models": blogsqueryset,
        "total": blogsqueryset.count(),
        "user": request.user,
        'investment': investment,
    }
    return render(request, 'businessforum/blog.html', context)

class PostListView(ListView):
    model = BlogItem
    template_name = 'businessforum/blog.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering= ['-date_posted']
    paginate_by =3

    def get_queryset(self):

        if not ('perpage_blogs' in self.request.session):
            obj= UserPreference.objects.filter(user=self.request.user).first()
            if obj:
                self.request.session['perpage_blogs']=obj.perpage_blogs
            else:# nothing in db
                self.request.session['perpage_blogs']= 3
        else:
            obj= UserPreference.objects.filter(user=self.request.user).first()
            if obj:
                self.request.session['perpage_blogs']=obj.perpage_blogs
            else:# nothing in db
                self.request.session['perpage_blogs']= 3      

        perpage_blogs=self.request.session['perpage_blogs']
        self.paginate_by =perpage_blogs
        # i am investment owner or i have investment in the business
        investment = get_object_or_404(Investment, pk=self.kwargs.get('id'))

        investor= investment.userIsInvestor(self.request.user)
        business_owner=investment.userIsOwner(self.request.user)
        if investor or business_owner:
            investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)
            return BlogItem.objects.filter(Q(investmentblog =investmentblog)).order_by('-date_posted')
        
        raise Http404("Your no rights over this page")
       
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        id=self.kwargs.get('id')
        investment = get_object_or_404(Investment,pk=id)
        context["investment"] = investment
        context["investment_id"] = id
        return context
class UserPostListView(ListView):
    model = BlogItem
    template_name = 'businessforum/user_posts.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by =3



    def get_queryset(self):
        if not ('perpage_blogs' in self.request.session):
            obj= UserPreference.objects.filter(user=self.request.user).first()
            if obj:
                self.request.session['perpage_blogs']=obj.perpage_blogs
            else:# nothing in db
                self.request.session['perpage_blogs']= 3
        else:
            obj= UserPreference.objects.filter(user=self.request.user).first()
            if obj:
                self.request.session['perpage_blogs']=obj.perpage_blogs
            else:# nothing in db
                self.request.session['perpage_blogs']= 3      

        perpage_blogs=self.request.session['perpage_blogs']
        self.paginate_by =perpage_blogs

        user = get_object_or_404(User, username=self.kwargs.get('username'))
        investment = get_object_or_404(Investment, pk=self.kwargs.get('id'))
        investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)
        return BlogItem.objects.filter(Q(author=user), Q(investmentblog =investmentblog)).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        id=self.kwargs.get('id')
        investment = get_object_or_404(Investment,pk=id)
        context["investment"] = investment
        context["investment_id"] = id
        return context
class PostDetailView(DetailView):
    model = BlogItem

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["post_id"] = self.kwargs.get('pk')
        blogitem = get_object_or_404(BlogItem, pk=self.kwargs.get('pk'))
        investmentblog_id = blogitem.investmentblog.id
        investmentblog = get_object_or_404(InvestmentBlog, pk=investmentblog_id)

        id=investmentblog.investment.id
        investment = get_object_or_404(Investment,pk=id)
        context["investment"] = investment
        context["investment_id"] = id
        return context
class PostCreateView(LoginRequiredMixin,CreateView):
    model = BlogItem
    form_class = BlogItemForm
    template_name = 'businessforum/post_form.html'

    def get(self, request, *args, **kwargs):
        investment = get_object_or_404(Investment,pk=self.kwargs.get('id'))
        investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)
        form = self.form_class(initial={'investmentblog': investmentblog })
        context={}
        id=investmentblog.investment.id
        investment = get_object_or_404(Investment,pk=id)
        context["investment"] = investment
        context["investment_id"] = id
        context["form"] = form
        return render(request, self.template_name, context)
       

    def form_valid(self, form):
        investment = get_object_or_404(Investment,pk=self.kwargs.get('id'))
        investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)
       
        form.instance.author = self.request.user
        form.instance.investmentblog = investmentblog
        return super().form_valid(form)
   
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = BlogItem
    template_name = 'businessforum/blogitem_form.html'
    form_class = BlogItemForm

    def get(self, request, *args, **kwargs):
        blogitem = get_object_or_404(BlogItem,pk=self.kwargs.get('pk'))
        investmentblog_id = blogitem.investmentblog.id
        investmentblog = get_object_or_404(InvestmentBlog, pk=investmentblog_id)

        form = self.form_class(instance= blogitem)
        context={}
        id=investmentblog.investment.id
        context["investment_id"] = id 
        context["form"] = form
        investment = get_object_or_404(Investment,pk=id)
        context["investment"] = investment
        return render(request, self.template_name, context)
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
  
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = BlogItem
    success_url = "/"
  
    def dispatch(self, *args, **kwargs):
        blogitem = get_object_or_404(BlogItem,pk=self.kwargs.get('pk'))
        id= blogitem.investmentblog.investment.id
        self.success_url = reverse_lazy('investment-blogs', kwargs={'id': id})
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
