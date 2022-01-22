import datetime, time, pytz, json, logging

from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, reverse

from daily.models import UserSessions
from daily.views import user_account
from django.conf import settings

logger = logging.getLogger('application')


class SessionCheck(MiddlewareMixin):
    """セッションチェック用ミドルウェア"""
    def process_request(self, request):
        """urls.py到達前"""
        logger.debug('process_request_path:' + request.path)
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """実行view関数決定後"""
        logger.debug('process_view_path:' + request.path)

        request.user_id = ''
        getcookie = request.COOKIES.get('daily-session-key')

        if getcookie:
            logger.debug('Cookieにdaily-session-key情報あり')

            sessions = UserSessions.objects.filter(session_key=getcookie).values()
            if sessions:
                logger.debug('DBにセッション情報存在')

                now = datetime.datetime.now(datetime.timezone.utc)
                now_unixtime = int(time.mktime(now.timetuple()))
                last_used_at = sessions[0].get('last_used_at')
                last_used_unixtime = int(time.mktime(last_used_at.timetuple()))
                time_diff = now_unixtime - last_used_unixtime
                logger.debug('now time:' + now.strftime('%Y/%m/%d %H:%M:%S'))
                logger.debug('now time unixtime:' + str(now_unixtime))
                logger.debug('last_used_at:' + last_used_at.strftime('%Y/%m/%d %H:%M:%S'))
                logger.debug('last_used_at unixtime' + str(last_used_unixtime))
                logger.debug('time_diff' + str(time_diff))
                timer = settings.SESSION_TIMER
                # タイムアウト判定
                if time_diff > timer:
                    logger.debug('timeout')
                    request.user_id = ''
                    UserSessions.objects.filter(session_key=getcookie).delete()
                    response = redirect_to_login(request.path, '/user_logout')
                    response.delete_cookie('daily-session-key')
                    if request.is_ajax():
                        return HttpResponseForbidden()
                    else:
                        logger.debug(response.status_code)
                        return response
                else:
                    # ユーザー情報取得
                    user_data = UserSessions.objects.filter(session_key=getcookie).values(
                        'id',
                        'last_used_at',
                        'user_id__id',  # users.id
                        'user_id__email'  # users.email
                    )[0]
                    request.session_id = user_data['id']
                    request.user_id = user_data['user_id__id']
                    request.email = user_data['user_id__email']

                    UserSessions.objects.filter(session_key=getcookie).update(last_used_at=now)

                    if view_func == user_account.user_login:
                        logger.debug('ログインへのアクセスだがsessionを保持しているためホーム画面へ繊維')
                        return HttpResponseRedirect('/home')
                    elif view_func == user_account.user_logout:
                        logger.debug('ログアウトセッション削除')
                        UserSessions.objects.filter(session_key=getcookie).delete()
                        response = redirect_to_login(request.path, '/')
                        response.delete_cookie('daily-session-key')
                        return response
                    else:
                        logger.debug('要求ページへ遷移')
                        return None
            else:
                logger.debug('有効なセッションなし')
                request.user_id = ''
                if view_func == user_account.user_login:
                    return None
                elif request.is_ajax():
                    # ajaxからのリクエストの場合、403エラーを返却
                    return HttpResponseForbidden()
                else:
                    return redirect_to_login(request.path, '/')
        else:
            logger.debug('Cookie取得失敗')
            request.user_id = ''
            if view_func == user_account.user_login:
                return None
            elif view_func == user_account.register:
                return None
            elif request.is_ajax():
                # ajaxからのリクエストの場合、403エラーを返却
                return HttpResponseForbidden()
            else:
                return redirect_to_login(request.path, '/')
