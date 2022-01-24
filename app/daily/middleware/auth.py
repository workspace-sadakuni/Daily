import datetime, time, pytz, json, logging

from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, reverse

from daily.models import Users, UserSessions, UserAccessLogs
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
                    user_data = UserSessions.objects.select_related('user_id').get(session_key=getcookie)
                    # request.userに取得したusersテーブルのinstanceを保持させ、アクセスログ書き込み時に使用する。
                    request.user = user_data.user_id
                    request.user_id = user_data.user_id.id
                    request.username = user_data.user_id.username
                    request.user_email = user_data.user_id.email
                    request.session_id = user_data.id

                    UserSessions.objects.filter(session_key=getcookie).update(last_used_at=now)

                    # 現在時刻をrequestに保持（process_responce側でこの時刻を使ってログに処理時間を記録）
                    request.logging_start_dt = now

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

    def process_response(self, request, response):
        """view処理後"""
        # Access Log書き込み
        # logging_start_dtが設定されている場合（有効なセッションが存在）のみ書き込む
        if getattr(request, 'logging_start_dt', 0) != 0:
            delta = datetime.datetime.now(datetime.timezone.utc) - request.logging_start_dt
            response.logging_response_time = delta.seconds * 1000 + delta.microseconds / 1000
            access_log(request, response)

        return response


def access_log(request, response):
    """Acess Logの書き込み処理"""

    # リクエスト情報を取得
    request_url = request.path_info
    request_method = request.META["REQUEST_METHOD"] if 'REQUEST_METHOD' in request.META else ''
    referer = request.META["HTTP_REFERER"] if 'HTTP_REFERER' in request.META else ''
    user_agent = request.META["HTTP_USER_AGENT"] if 'HTTP_USER_AGENT' in request.META else ''

    source_ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
    if source_ip_list:
        # ip_listに記録されたIPアドレスが複数ある場合、ネットワーク構成などを考慮して添字を指定する。
        source_ip = source_ip_list.split(',')[0]
    else:
        source_ip = request.META.get('REMOTE_ADDR')
        if source_ip is None:
            source_ip = ''

    user = Users.objects.filter(id=request.user_id)

    # ユーザーが存在する場合のみアクセスログを記録。ユーザー削除時にはユーザーは存在せずDBエラーとなるため記録しない。
    if len(user):
        log = UserAccessLogs(
            request_at=request.logging_start_dt,
            response_at=datetime.datetime.now(datetime.timezone.utc),
            user_id=request.user,
            username=request.username,
            user_email=request.user_email,
            request_method=request_method,
            request_url=request_url,
            referer=referer,
            source_ip=source_ip,
            user_agent=user_agent,
            session_id=request.session_id,
            session_key=request.COOKIES.get('daily-session-key'),
            response_time=response.logging_response_time,
            status_code=getattr(response, 'status_code', 0)
        )
        log.save()
