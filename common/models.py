
import binascii
import datetime
import os
import time
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.contrib.auth.models import User
from common.templatetags.common_tags import (
    is_document_file_image,
    is_document_file_audio,
    is_document_file_video,
    is_document_file_pdf,
    is_document_file_code,
    is_document_file_text,
    is_document_file_sheet,
    is_document_file_zip,
)

from django.utils import timezone


def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)



# class User(AbstractBaseUser, PermissionsMixin):
#     file_prepend = "users/profile_pics"
#     username = models.CharField(max_length=100, unique=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     last_name = models.CharField(max_length=150, blank=True)
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(("date joined"), auto_now_add=True)
#     #role = models.CharField(max_length=50, choices=ROLES)
#     profile_pic = models.FileField(
#         max_length=1000, upload_to=img_url, null=True, blank=True
#     )
#     has_sales_access = models.BooleanField(default=False)
#     has_marketing_access = models.BooleanField(default=False)
    
#     # other access.....
#     # has_locomotives_access = models.BooleanField(default=False)
#     # has_wagons_access = models.BooleanField(default=False)
#     # has_financial_access = models.BooleanField(default=False)
    
#     # company = models.ForeignKey(
#     #     Company, on_delete=models.CASCADE, null=True, blank=True
#     # )

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = [
#         "username",
#     ]

#     objects = UserManager()

#     def get_short_name(self):
#         return self.username

#     @property
#     def get_app_name(self):
#         if self.company:
#             return self.company.sub_domain + "." + settings.APPLICATION_NAME
#         else:
#             return settings.APPLICATION_NAME

#     def documents(self):
#         #related name
#         #return self.document_set.all()
#         return self.document_uploaded.all()

#     def get_full_name(self):
#         full_name = None
#         if self.first_name or self.last_name:
#             full_name = self.first_name + " " + self.last_name
#         elif self.username:
#             full_name = self.username
#         else:
#             full_name = self.email
#         return full_name

#     def __str__(self):
#         return self.email

#     class Meta:
#         ordering = ["-is_active"]


# class Address(models.Model):
#     address_line = models.CharField(_("Address"), max_length=255, blank=True, null=True)
#     street = models.CharField(_("Street"), max_length=55, blank=True, null=True)
#     city = models.CharField(_("City"), max_length=255, blank=True, null=True)
#     state = models.CharField(_("State"), max_length=255, blank=True, null=True)
#     postcode = models.CharField(
#         _("Post/Zip-code"), max_length=64, blank=True, null=True
#     )
#     country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)

#     def __str__(self):
#         return self.city if self.city else ""

#     def get_complete_address(self):
#         address = ""
#         if self.address_line:
#             address += self.address_line
#         if self.street:
#             if address:
#                 address += ", " + self.street
#             else:
#                 address += self.street
#         if self.city:
#             if address:
#                 address += ", " + self.city
#             else:
#                 address += self.city
#         if self.state:
#             if address:
#                 address += ", " + self.state
#             else:
#                 address += self.state
#         if self.postcode:
#             if address:
#                 address += ", " + self.postcode
#             else:
#                 address += self.postcode
#         if self.country:
#             if address:
#                 address += ", " + self.get_country_display()
#             else:
#                 address += self.get_country_display()
#         return address

class UserAdditions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file_prepend = "users/profile_pics"
    
    date_joined = models.DateTimeField(("date joined"), auto_now_add=True)
    profile_pic = models.FileField(
        max_length=1000, upload_to=img_url, null=True, blank=True
    )

    def documents(self):
        #related name
        #return self.document_set.all()
        return self.user.document_uploaded.all()
  
    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-date_joined"]


def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)


class Document(models.Model):

    DOCUMENT_STATUS_CHOICE = (("active", "active"), ("inactive", "inactive"))

    title = models.CharField(max_length=1000, blank=True, null=True)
    document_file = models.FileField(upload_to=document_path, max_length=5000)
    created_by = models.ForeignKey(
        User, related_name="document_uploaded", on_delete=models.SET_NULL, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="active"
    )
    shared_to = models.ManyToManyField(User, related_name="document_shared_to")
    # company = models.ForeignKey(
    #     Company, on_delete=models.SET_NULL, null=True, blank=True
    # )

    class Meta:
        ordering = ("-created_on",)

    def file_type(self):
        name_ext_list = self.document_file.url.split(".")
        if len(name_ext_list) > 1:
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa-file-word-o")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file-o")
        return ("file", "fa fa-file-o")

    def __str__(self):
        return self.title

   
  

def generate_key():
    return binascii.hexlify(os.urandom(8)).decode()


class Profile(models.Model):
    """ this model is used for activating the user within a particular expiration time """

    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE
    )  # 1 to 1 link with Django User
    activation_key = models.CharField(max_length=50)
    key_expires = models.DateTimeField()

   
    def save(self, *args, **kwargs):
        """ by default the expiration time is set to 2 hours """
        self.key_expires = timezone.now() + datetime.timedelta(hours=2)
        super(Profile, self).save(*args, **kwargs)


class ModifiedRecordQuerySet(models.QuerySet):
    
    def date_range(self, dstart, dend):
        # filter or
        return self.filter(date_created__gte=dstart, date_created__lte=dend)

    def last_10(self):
        return self.order_by('-date_created')[:10]
    

class ModifiedRecord(models.Model):
    model_name =  models.CharField(max_length=150)
    model_pk = models.IntegerField()
    model_dict =  models.TextField()
    is_deleted = models.BooleanField(default=False)
    is_modified = models.BooleanField(default=False)
    is_added = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    # user_list

    def __str__(self):
        if self.created_by:
            return str(self.model_name) + " by " + str(self.created_by) + " on " + str(self.date_created)
        else:
            return str(self.model_name)+ " by " + str(self.date_created)

    class Meta:
        ordering = ['-date_created']    

    objects = ModifiedRecordQuerySet.as_manager() 