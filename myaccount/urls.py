from django.urls import re_path
from . import views

app_name = "myaccount"
urlpatterns = [
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
    re_path(r'^profile/country-list/$', views.country_list, name="country_list"),
    re_path(r'^profile/city-add/$', views.city_add, name="city_add"),
    # Ajax调用城市清单
    re_path(r'^ajax/load_cities/$', views.ajax_load_cities, name='ajax_load_cities'),
    re_path(r'^profile/add-citys/$', views.add_citys, name='add_citys'),
    re_path(r'^profile/ajax/avatar/$', views.ajax_avatar_upload, name='ajax_avatar_upload'),
    re_path(r'^profile/country-rename/$', views.rename_country, name='rename_country'),
    re_path(r'^profile/city-del/$', views.del_country_city, name='del_city'),
]


"""
http://127.0.0.1:8000/accounts/signup/

http://127.0.0.1:8000/accounts/login/

http://127.0.0.1:8000/accounts/logout/

http://127.0.0.1:8000/accounts/password/reset/
"""