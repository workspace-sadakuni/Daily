import json
import logging
import os
import sys
import uuid
from datetime import *
from time import mktime

from django import http
from django.conf import settings
from django.shortcuts import render
from django.template import TemplateDoesNotExist, loader
from django.utils.translation import ugettext
from django.views import debug

from django.conf import settings
from daily.lib import common

logger = logging.getLogger('application')


def page_not_found(request, *args, **kwargs):
    """
        DEBUG=Falseの場合のみ有効となる。
        djangoのデフォルトエラーハンドラー
        django.conf.urls.defaults.page_not_found
        の代わりに404エラーを処理する。
    """
    try:
        template = loader.get_template('404.html')
        next_path = request.path_info if hasattr(request, 'path_info') else ''
        context = {'next_path': next_path, 'title': 'Not Found', 'is_locale_ja': __is_local_ja()}
        return http.HttpResponseServerError(template.render(context))
    except TemplateDoesNotExist as e:
        raise e
    except Exception as e:
        raise e


def server_error(request, *args, **kwargs):
    """
    DEBUG=Falseの場合のみ有効となる。
    djangoのデフォルトエラーハンドラー
    django.conf.urls.defaults.server_error
    の代わりに500エラーを処理する。
    """

    # 開発モードでブラウザに送信されるレスポンスオブジェクトを作成する
    exc_info = sys.exc_info()
    rsp = debug.technical_500_response(request, *exc_info)

    # ログファイル名： path-to-view.timestamp.html
    file_stamp = str(int(mktime(datetime.now().timetuple()))) + str(uuid.uuid4())
    dumpfile = '.'.join([request.path_info.lstrip('/').rstrip('/').replace('/', '-'), file_stamp, 'html'])
    dump_path = os.path.join(settings.CLASH_DUMP_LOG_DIR, dumpfile)

    # レスポンスからHTMLを取り出してログファイルに出力
    try:
        # ファイル出力に失敗した場合はエラーログ出力し終了
        with open(dump_path, 'w') as f:
            f.write(rsp.content.decode('utf-8'))
    except Exception as e:
        logger.exception(e)

    # クラッシュログファイル情報をログに出力（将来的にはメールなどでの通知が望ましい）
    try:
        # clash_log_notification_jsonは将来的にメールなどへ通知するようにjson形式で作成しておく
        clash_log_notification_json = json.dumps({
            'text': '[host:{hostname}][user_id:{user_id}]500エラーが発生しました。{dump_url_dir}/{dumpfile} にエラーログを格納しています。'.format(
                hostname=os.uname()[1],
                user_id=request.user_id,
                dump_url_dir=settings.APP_LOG_DIR,
                dumpfile=dumpfile),
            'user_id': str(request.user_id)
        })
        clash_log_notification = json.loads(clash_log_notification_json)
        logger.error(clash_log_notification)
    except Exception as e:
        logger.exception(e)

    try:
        # クラッシュログファイル名を示す文字列をエラーページで表示する
        template = loader.get_template('500.html')
        context = {'dump_file': dumpfile, 'title': 'System Error', 'is_local_ja': __is_local_ja()}
        # ブラウザへの返却はDjangoに任せる。(500.htmlでページを作成し返却)
        return http.HttpResponseServerError(template.render(context))
    except Exception as e:
        logger.exception(e)
        return http.HttpResponseServerError('<h1>System Error (500)</h1>', content_type='text/html')


def __is_local_ja():
    # ブラウザ言語判定
    return True if (common.is_browser_lang_ja()) else False
