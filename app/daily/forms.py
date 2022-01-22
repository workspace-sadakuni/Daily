from django import forms
from django.contrib.auth.password_validation import validate_password

from daily.models import Users, PostFoods
from django.conf import settings


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード確認', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢')
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)

    def clean_picture(self):
        limit_picture_size = settings.DATA_UPLOAD_MAX_NUMBER_FIELDS
        picture = self.cleaned_data['picture']
        if picture:
            if picture.size > limit_picture_size:
                raise forms.ValidationError('Picture is over capacity( ~ 1MB)')
        return picture

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture')


class PasswordChangeForm(forms.ModelForm):

    password = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード確認', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ('password',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class FoodInputForm(forms.ModelForm):
    title = forms.CharField(label='タイトル (必須) ', widget=forms.TextInput(attrs={'placeholder': '魚のフライに挑戦！'}))
    food_name = forms.CharField(label='料理名 (必須) ', widget=forms.TextInput(attrs={'placeholder': '白身魚のフライ'}))
    content = forms.CharField(label='内容', required=False, widget=forms.Textarea(attrs={'placeholder': '白身魚のフライにタルタルソースを添えて料理したよ！'}))
    image = forms.FileField(label='写真', required=False)
    ate_at = forms.DateTimeField(label='食事日時 (必須) ', widget=forms.DateTimeInput(attrs={'placeholder': '2022-01-01 18:00'}))

    def clean_image(self):
        limit_picture_size = settings.DATA_UPLOAD_MAX_NUMBER_FIELDS
        image = self.cleaned_data['image']
        if image:
            if image.size > limit_picture_size:
                raise forms.ValidationError('Picture is over capacity( ~ 1MB)')
        return image

    class Meta:
        model = PostFoods
        fields = ('title', 'food_name', 'content', 'image', 'ate_at')
