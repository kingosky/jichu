from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
import uuid
import os
# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(str(instance.user.id), sub_folder, filename)


class Country(models.Model):
    name = models.CharField(verbose_name="国家", max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(verbose_name="城市", max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="国家",)

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    org = models.CharField(
       'Organization', max_length=128, blank=True)

    telephone = models.CharField(
       'Telephone', max_length=50, blank=True)

    mod_date = models.DateTimeField('Last modified', auto_now=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="国家")

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="城市")

    avatar = models.ImageField(upload_to=user_directory_path, default=os.path.join("avatar", "default.jpg"),
                               verbose_name="头像", blank=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


class Client(models.Model):
    name = models.CharField(verbose_name="客户", max_length=50)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="国家")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="城市")

    def __str__(self):
        return self.name

