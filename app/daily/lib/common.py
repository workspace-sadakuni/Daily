import os
import pytz
import re
import uuid
from datetime import datetime
from pytz import timezone

from django.utils.translation import get_language

from const import const


def get_browser_lang():
    """
    ブラウザの言語取得
    Description: ブラウザから言語設定を取得し、日本語かそれ以外で返却する
    @return 例）日本語:ja 英語:en
    """
    return get_language()


def is_browser_lang_ja():
    """
    ブラウザの言語が日本語であるか判定
    Description: ブラウザから言語設定を取得し、日本語かそうでないかを返却する
    @return bool
    """
    return get_browser_lang() == const.LANGUAGE_JA


def utc_datetime_to_jst_datetime_format(utc_datetime):
    """
    YYYY-MM-DD HH:MM:SS 形式のUTCをYYYY-MM-DD HH:MM形式のJSTに変換
    :param utc_datetime:
    :return jst_datetime_format:
    """
    jst_datetime = utc_datetime.astimezone(timezone('Asia/Tokyo'))
    jst_datetime_format = jst_datetime.strftime('%Y-%m-%d %H:%M')
    return jst_datetime_format


def jst_string_to_utc_datetime(jst_string):
    """
    YYYY-MM-DD HH:MM 形式のJSTをYYYY-MM-DD HH:MM:SS形式のUTCに変換
    :param jst_string:
    :return jst_datetime_format:
    """
    utc_datetime = ''
    pattern_date = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}$')
    if pattern_date.match(jst_string):
        jst_datetime = datetime.strptime(jst_string, '%Y-%m-%d %H:%M').astimezone(pytz.timezone('Asia/Tokyo'))
        utc_datetime = jst_datetime.astimezone(pytz.timezone('UTC'))

    return utc_datetime
