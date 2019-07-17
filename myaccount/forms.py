from django import forms
from .models import UserProfile, Country, City, Client


class AvatarUploadForm(forms.Form):
    avatar_file = forms.ImageField()


ALLCOUNTRY = Country.objects.all()
ALLCITY = City.objects.all()


class ProfileForm(forms.Form):

    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)
    telephone = forms.CharField(label='Telephone', max_length=50, required=False)
    country = forms.ModelChoiceField(queryset=ALLCOUNTRY, empty_label='请选择国家', required=False)
    city = forms.ModelChoiceField(queryset=ALLCITY, empty_label='请选择城市', required=False)


class SignupForm(forms.Form):

    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user.save()
        user_profile.save()


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("name",)

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     ob = Country.objects.filter(name = name)
    #     if ob.exists():
    #         raise forms.ValidationError("Country is already setted.")
        # return name


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name',)


class BaseCityFormSet(forms.BaseFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            return
            titles = []
            for form in self.forms:
                title = form.cleaned_data['name']
                if title in titles:
                    raise forms.ValidationError("Articles in a set must have distinct titles.")
            titles.append(title)



IngCityFormSet = forms.inlineformset_factory(
    Country,
    City,
    fields=('name',),
    extra=3,
    can_delete=False,
    max_num=5,
    # formset=BaseCityFormSet
)