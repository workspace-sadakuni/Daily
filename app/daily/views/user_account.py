import logging
import os
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string

from django.conf import settings
from const.const import COOKIE_SESSION_KEY
from daily import forms
from daily.models import Users, UserSessions

logger = logging.getLogger('application')


def register(request):
    register_form = forms.RegisterForm(request.POST or None)
    if register_form.is_valid():
        try:
            register_form.save()
            messages.success(request, 'ユーザーを作成しました。')
            return redirect('daily:home')
        except ValidationError as e:
            register_form.add_error('password', e)
    return render(request, 'daily/user_account/register.html', context={'register_form': register_form})


def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                # ログイン処理
                login(request, user)

                response = render(request, 'daily/home.html')
                session_key = get_random_string(64)

                # ログインセッション作成
                UserSessions.objects.create(
                    user_id=user, email=user.email, session_key=session_key, login_at=datetime.now(),
                    last_used_at=datetime.now()
                )
                # ログインセッションをクッキーに設定
                response.set_cookie(COOKIE_SESSION_KEY, session_key)
                return response
            else:
                messages.warning(request, 'ユーザーが存在しません。')
        else:
            messages.warning(request, 'メールアドレスまたはパスワードが間違っています。')
    return render(request, 'daily/user_account/user_login.html', context={'login_form': login_form})


def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('daily:user_login')


def user_detail(request):
    user_info = Users.objects.filter(id=request.user_id)
    if user_info:
        return render(request, 'daily/user_account/user_detail.html', context={'user_info': user_info})
    else:
        raise Http404


def user_edit(request):
    # 現在のユーザー情報を取得
    current_user = get_object_or_404(Users, id=request.user_id)
    user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=current_user)

    if request.method == 'POST':
        # 現在のユーザー画像情報を取得。存在しない場合Noneを代入
        current_picture = str(current_user.picture) if str(current_user.picture) else None

        if user_edit_form.is_valid():
            user_edit_form.save()

            updated_user = get_object_or_404(Users, id=request.user_id)
            # 更新後のユーザー画像情報を取得。存在しない場合Noneを代入
            updated_picture = str(updated_user.picture) if str(updated_user.picture) else None

            # 更新前後でユーザー画像が異なるかつ、更新前画像が存在する場合に更新前画像ファイルを削除
            if current_picture != updated_picture and current_picture is not None:
                try:
                    previous_picture = os.path.join(settings.MEDIA_ROOT, current_picture)
                    os.remove(previous_picture)
                except UnboundLocalError as e:
                    logger.error('---could not parse the previous user file---')
                    logger.error(e)
                except FileNotFoundError as e:
                    logger.error('---the file below was not be found---\n' + previous_picture)
                    logger.error(e)
                except Exception as e:
                    logger.error('---fail to delete the file below---\n' + previous_picture)
                    logger.error(e)
            return redirect('daily:user_detail')
        else:
            return render(request, 'daily/user_account/user_edit.html', context={'user_edit_form': user_edit_form})
    else:
        return render(request, 'daily/user_account/user_edit.html', context={'user_edit_form': user_edit_form})


def change_password(request):
    user = get_object_or_404(Users, id=request.user_id)
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワードの更新が完了しました。')
            # パスワード更新後、セッション情報を更新
            update_session_auth_hash(request, user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(request, 'daily/user_account/change_password.html', context={'password_change_form': password_change_form})