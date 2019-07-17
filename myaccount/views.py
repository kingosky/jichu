from django.shortcuts import render, get_object_or_404
from .models import UserProfile, City, Country
from .forms import ProfileForm, CountryForm, IngCityFormSet, CityForm, AvatarUploadForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid
from PIL import Image
import os
import json
# Create your views here.


@login_required
@require_POST
@csrf_exempt
def del_country_city(request):
    city_id = int(request.POST['city_id'])
    try:
        line = City.objects.get(id=city_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required
@require_POST
@csrf_exempt
def rename_country(request):
    country_name = request.POST["country_name"]
    country_id = int(request.POST['country_id'])
    try:
        countrys = Country.objects.filter(name=country_name)
        if countrys:
            return HttpResponse('2')
        else:
            line = Country.objects.get(id=country_id)
            line.name = country_name
            line.save()
            return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required
def ajax_avatar_upload(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == "POST":
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['avatar_file']  # 获取上传图片
            data = request.POST['avatar_data']  # 获取ajax返回图片坐标

            if img.size/1024 > 700:
                return JsonResponse({"message": "图片尺寸应小于900 X 1200 像素, 请重新上传。", })

            current_avatar = user_profile.avatar
            cropped_avatar = crop_image(current_avatar, img, data, user.id)
            user_profile.avatar = cropped_avatar

            # 将图片路径修改到当前会员数据库
            user_profile.save()

            # 向前台返回一个json，result值是图片路径
            data = {"result": user_profile.avatar.url, }
            return JsonResponse(data)
        else:
            return JsonResponse({"msg": "请重新上传。只能上传图片"})

    return HttpResponseRedirect(reverse('myaccount:profile'))


def crop_image(current_avatar, file, data, uid):
    # 随机生成新的图片名，自定义路径。
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    cropped_avatar = os.path.join(str(uid), "avatar", file_name)

    # 相对根目录路径
    file_path = os.path.join("media", str(uid), "avatar", file_name)

    # 获取Ajax发送的裁剪参数data，先用json解析。
    coords = json.loads(data)
    t_x = int(coords['x'])
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']

    # 裁剪图片,压缩尺寸为400*400。
    img = Image.open(file)
    crop_im = img.crop((t_x, t_y, t_width, t_height)).resize((400, 400), Image.ANTIALIAS).rotate(t_rotate)
    # 返回目录名
    directory = os.path.dirname(file_path)

    # 验证目录存在
    if os.path.exists(directory):
        crop_im.save(file_path)
    else:
        os.makedirs(directory)
        crop_im.save(file_path)

    # 如果头像不是默认头像，删除老头像图片, 节省空间
    if not current_avatar == os.path.join("avatar", "default.jpg"):
        # .url 拿到imagefield类型数据，os.path.basename拿到文件名
        current_avatar_path = os.path.join("media", str(uid), "avatar", os.path.basename(current_avatar.url))
        os.remove(current_avatar_path)

    return cropped_avatar


@login_required
def add_citys(request):
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            ingcity_formset = IngCityFormSet(request.POST, instance=country)
            if ingcity_formset.is_valid():
                ingcity_formset.save()
                return HttpResponseRedirect(reverse('myaccount:country_list'))
    else:
        form = CountryForm()
        ingcity_formset = IngCityFormSet()

    return render(request, 'myaccount/citys_add.html', {'form': form, 'ingcity_formset': ingcity_formset})


def ajax_load_cities(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id', None)
        if country_id:
            data = list(City.objects.filter(country_id=country_id).values("id", "name"))
            return JsonResponse(data, safe=False)


@login_required
@csrf_exempt
def city_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        country_id = int(request.POST['country_id'])
        country = get_object_or_404(Country, pk=country_id)
        try:
            City.objects.create(name=name, country=country)
            return HttpResponse('1')
        except:
            return HttpResponse('3')


@login_required
@csrf_exempt
def country_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        ob = Country.objects.filter(name=name)
        if ob.exists():
            return HttpResponse('2')
        try:
            Country.objects.create(name=name)
            return HttpResponse('1')
        except:
            return HttpResponse('3')
    else:
        countrys = Country.objects.all()
        country_form = CountryForm()
        city_form = CityForm()
        return render(request, 'myaccount/country_list.html', {"countrys":countrys, "city_form":city_form,
                                                               "country_form":country_form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


@login_required
def profile_update(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            country_id = request.POST.getlist('country')
            # print(country_id)
            city_id = request.POST.getlist('city')
            # print(city_id)
            country = Country.objects.get(id=country_id[0])
            city = City.objects.get(id=city_id[0])
            user_profile.country = country
            user_profile.city = city
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']

            user_profile.save()

            return HttpResponseRedirect(reverse('myaccount:profile'))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone,
                        'country':user_profile.country, 'city':user_profile.city}
        form = ProfileForm(default_data)

    return render(request, 'account/profile_update.html', {'form': form, 'user': user})