import datetime
import json
import os

#import boto3
#import botocore
#import phonenumbers
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
    View,
)

from common.forms import (
    DocumentForm,
)
from common.models import (
    Document,
    Profile,
    #User,
)

from django.contrib.auth.models import User
def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("common:dashboard")
    return render(request, "landing_page.html", status=200)




class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        #if not request.user.role == "ADMIN":
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "common/doc_list.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        #accounts = Account.objects.filter(status="open")
        # contacts = Contact.objects.all()
        # leads = Lead.objects.exclude(status="converted").exclude(status="closed")
        # opportunities = Opportunity.objects.all()
        print(self.request.user)
        if self.request.user.is_superuser:#self.request.user.role == "ADMIN" or 
            pass
        else:
            pass
       
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "common/profile.html"

    def get_context_data(self, **kwargs):

        context = super(ProfileView, self).get_context_data(**kwargs)
        context["user_obj"] = self.request.user
        return context




@login_required
def document_create(request):
    template_name = "common/doc_create.html"
    users = []
    if  request.user.is_superuser:#request.user.role == "ADMIN" or
        users = User.objects.all()#filter(is_active=True, company=request.company).order_by(
        #     "email"
        # )
    else:
        users = User.objects.all()#filter(role="ADMIN", company=request.company).order_by(
        #     "email"
        # )
    form = DocumentForm(users=users, request_obj=request)
    if request.POST:
        form = DocumentForm(
            request.POST, request.FILES, users=users, request_obj=request
        )
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            #doc.company = request.company
            doc.save()
            if request.POST.getlist("shared_to"):
                doc.shared_to.add(*request.POST.getlist("shared_to"))
            
            data = {"success_url": reverse_lazy("common:doc_list"), "error": False}
            return JsonResponse(data)
        return JsonResponse({"error": True, "errors": form.errors})
    context = {}
    context["doc_form"] = form
    context["users"] = users
   
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist("assigned_to", []) if i
    ]
    context["errors"] = form.errors
    return render(request, template_name, context)


class DocumentListView(LoginRequiredMixin, TemplateView):
    model = Document
    context_object_name = "documents"
    template_name = "common/doc_list_1.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.user.is_superuser : #request.user.role == "ADMIN" or
            queryset = queryset
        else:
            if self.request.user.documents():
                doc_ids = self.request.user.documents().values_list("id", flat=True)
                shared_ids = queryset.filter(
                    Q(status="active") & Q(shared_to__id__in=[self.request.user.id])
                ).values_list("id", flat=True)
                queryset = queryset.filter(Q(id__in=doc_ids) | Q(id__in=shared_ids))
            else:
                queryset = queryset.filter(
                    Q(status="active") & Q(shared_to__id__in=[self.request.user.id])
                )

        request_post = self.request.POST
        if request_post:
            if request_post.get("doc_name"):
                queryset = queryset.filter(
                    title__icontains=request_post.get("doc_name")
                )
            if request_post.get("status"):
                queryset = queryset.filter(status=request_post.get("status"))

            if request_post.getlist("shared_to"):
                queryset = queryset.filter(
                    shared_to__id__in=request_post.getlist("shared_to")
                )
        return queryset#.filter(company=self.request.company)

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(
            is_active=True#, company=self.request.company
        ).order_by("username")
        context["documents"] = self.get_queryset()
        context["status_choices"] = Document.DOCUMENT_STATUS_CHOICE
        context["sharedto_list"] = [
            int(i) for i in self.request.POST.getlist("shared_to", []) if i
        ]
        context["per_page"] = self.request.POST.get("per_page")

        search = False
        if (
            self.request.POST.get("doc_name")
            or self.request.POST.get("status")
            or self.request.POST.get("shared_to")
        ):
            search = True

        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document

    def get(self, request, *args, **kwargs):
        #if not request.user.role == "ADMIN":
        if not request.user == Document.objects.get(id=kwargs["pk"]).created_by:
            raise PermissionDenied
        self.object = self.get_object()
        # if self.object.company != request.company:
        #     raise PermissionDenied
        self.object.delete()
        return redirect("common:doc_list")


@login_required
def document_update(request, pk):
    template_name = "common/doc_create.html"
    users = []
    # if request.user.role == "ADMIN" or request.user.is_superuser:
    #     users = User.objects.filter(is_active=True).order_by("email")
    # else:
    #     users = User.objects.filter(role="ADMIN").order_by("email")
    # document = Document.objects.filter(id=pk).first()

    # if document.company != request.company:
    #     raise PermissionDenied

    form = DocumentForm(users=users, instance=document, request_obj=request)

    if request.POST:
        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document,
            users=users,
            request_obj=request,
        )
        if form.is_valid():
            doc = form.save(commit=False)
            doc.save()

            doc.shared_to.clear()
            if request.POST.getlist("shared_to"):
                doc.shared_to.add(*request.POST.getlist("shared_to"))

           

            data = {"success_url": reverse_lazy("common:doc_list"), "error": False}
            return JsonResponse(data)
        return JsonResponse({"error": True, "errors": form.errors})
    context = {}
    context["doc_obj"] = document
    context["doc_form"] = form
    context["doc_file_name"] = context["doc_obj"].document_file.name.split("/")[-1]
    context["users"] = users#.filter(company=request.company)
  
    context["sharedto_list"] = [
        int(i) for i in request.POST.getlist("shared_to", []) if i
    ]
    context["errors"] = form.errors
    return render(request, template_name, context)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "common/doc_detail.html"

    def dispatch(self, request, *args, **kwargs):
        # if self.get_object().company != request.company:
        #     raise PermissionDenied

        #if not request.user.role == "ADMIN":
        if not request.user == Document.objects.get(id=kwargs["pk"]).created_by:
            raise PermissionDenied

        return super(DocumentDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        # documents = Document.objects.all()
        context.update(
            {"file_type_code": self.object.file_type()[1], "doc_obj": self.object,}
        )
        return context


def download_document(request, pk):
    # doc_obj = Document.objects.filter(id=pk).last()
    doc_obj = Document.objects.get(id=pk)
    if doc_obj:
        #if not request.user.role == "ADMIN":
        if (
            not request.user == doc_obj.created_by
            and request.user not in doc_obj.shared_to.all()
        ):
            raise PermissionDenied
        if settings.STORAGE_TYPE == "normal":
            path = doc_obj.document_file.path
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, "rb") as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel"
                    )
                    response[
                        "Content-Disposition"
                    ] = "inline; filename=" + os.path.basename(file_path)
                    return response
        else:
            file_path = doc_obj.document_file
            file_name = doc_obj.title
            BUCKET_NAME = "django-crm-demo"
            KEY = str(file_path)
            s3 = boto3.resource("s3")
            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, file_name)
                with open(file_name, "rb") as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel"
                    )
                    response[
                        "Content-Disposition"
                    ] = "inline; filename=" + os.path.basename(file_name)
                os.remove(file_name)
                return response
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    print("The object does not exist.")
                else:
                    raise

            return path
    raise Http404


def download_attachment(request, pk):  # pragma: no cover
    attachment_obj = Attachments.objects.filter(id=pk).last()
    if attachment_obj:
        if settings.STORAGE_TYPE == "normal":
            path = attachment_obj.attachment.path
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, "rb") as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel"
                    )
                    response[
                        "Content-Disposition"
                    ] = "inline; filename=" + os.path.basename(file_path)
                    return response
        else:
            file_path = attachment_obj.attachment
            file_name = attachment_obj.file_name
            BUCKET_NAME = "django-crm-demo"
            KEY = str(file_path)
            s3 = boto3.resource("s3")
            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, file_name)
                with open(file_name, "rb") as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel"
                    )
                    response[
                        "Content-Disposition"
                    ] = "inline; filename=" + os.path.basename(file_name)
                os.remove(file_name)
                return response
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    print("The object does not exist.")
                else:
                    raise
    raise Http404

