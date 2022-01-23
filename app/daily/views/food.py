import csv
import logging
import os
import urllib.parse
from datetime import datetime
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from pytz import timezone

from django.conf import settings
from daily import forms
from daily.lib.common import utc_datetime_to_jst_datetime_format, jst_string_to_utc_datetime, delete_media_file
from daily.lib.food import FoodInfoDao
from daily.models import Users, PostFoods

logger = logging.getLogger('application')


def food_input(request):
    user = get_object_or_404(Users, id=request.user_id)
    food_input_form = forms.FoodInputForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if food_input_form.is_valid():
            food = food_input_form.save(commit=False)
            food.user_id = user
            food.save()
            return redirect('daily:food_complete', food_id=food.id)
        else:
            return render(request, 'daily/food/food_input.html', context={'food_input_form': food_input_form})
    else:
        return render(request, 'daily/food/food_input.html', context={'food_input_form': food_input_form})


def food_complete(request, food_id):
    return render(request, 'daily/food/food_complete.html', context={'food_id': food_id})


def food_index(request):
    return render(request, 'daily/food/food_index.html')


def food_search(request):
    if not request.method == "POST":
        return JsonResponse(status=400, data={})

    food_list = []
    food_lists = {}

    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    food_info_dao = FoodInfoDao(user_id=request.user_id)

    if start_date is None and end_date is None:
        # 投稿一覧画面テーブル初期表示処理
        post_foods = food_info_dao.get_food_info()
    else:
        # 食事日時検索条件指定処理
        start_date = jst_string_to_utc_datetime(start_date)
        end_date = jst_string_to_utc_datetime(end_date)
        post_foods = food_info_dao.get_food_info(start_date=start_date, end_date=end_date)

    if not post_foods:
        return JsonResponse(status=404, data={})
    else:
        for post_food in post_foods:
            food_list_dict = {}
            food_list_dict['href'] = "/food_detail/" + str(post_food.id)
            food_list_dict['title'] = post_food.title
            food_list_dict['food_name'] = post_food.food_name
            food_list_dict['ate_at'] = utc_datetime_to_jst_datetime_format(post_food.ate_at)
            food_list_dict['created_at'] = utc_datetime_to_jst_datetime_format(post_food.created_at)
            food_list.append(food_list_dict)
            food_lists['data'] = food_list
        return JsonResponse(food_lists)


def food_detail(request, food_id):
    food_info = get_object_or_404(PostFoods, id=food_id, user_id=request.user_id)
    return render(request, 'daily/food/food_detail.html', context={'food_info': food_info})


def food_edit(request, food_id):
    # 現在の食事投稿情報を取得
    current_food = get_object_or_404(PostFoods, id=food_id, user_id=request.user_id)
    # 画面表示用に食事日時をフォーマット
    current_food.ate_at = utc_datetime_to_jst_datetime_format(current_food.ate_at)
    food_edit_form = forms.FoodInputForm(request.POST or None, request.FILES or None, instance=current_food)

    if request.method == 'POST':
        # 現在の食事投稿画像情報を取得。存在しない場合Noneを代入
        current_image = str(current_food.image) if str(current_food.image) else None

        if food_edit_form.is_valid():
            food_edit_form.save()

            updated_food = get_object_or_404(PostFoods, id=food_id, user_id=request.user_id)
            # 更新後の食事投稿画像情報を取得。存在しない場合Noneを代入
            updated_image = str(updated_food.image) if str(updated_food.image) else None

            # 更新前後で食事投稿画像が異なるかつ、更新前画像が存在する場合に更新前画像ファイルを削除
            if current_image != updated_image and current_image is not None:
                delete_media_file(current_image)
            return redirect('daily:food_detail', food_id=food_id)
        else:
            return render(request, 'daily/food/food_edit.html', context={'food_edit_form': food_edit_form})
    else:
        return render(request, 'daily/food/food_edit.html', context={'food_edit_form': food_edit_form})


def food_delete(request, food_id):
    food_info = get_object_or_404(PostFoods, id=food_id, user_id=request.user_id)

    if request.method == "POST":
        # 削除する食事投稿画像情報を取得。存在しない場合Noneを代入
        food_image = str(food_info.image) if str(food_info.image) else None
        delete_media_file(food_image)

        try:
            food_info.delete()
        except Exception as e:
            logger.error(f'---food_id: {food_id} could not be deleted---')
            logger.error(e)
            raise Exception
        else:
            logger.info(f'---food_id:{food_id} was successfully deleted---')

        return HttpResponse(status=200)
    else:
        return render(request, 'daily/food/food_delete.html', context={'food_info': food_info})


def make_food_download_file(request):
    download_filename = 'food_file_'
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']

    food_info_dao = FoodInfoDao(user_id=request.user_id)

    if start_date != '' or end_date != '':
        # 食事日時検索条件あり投稿一覧を取得
        start_date = jst_string_to_utc_datetime(start_date)
        end_date = jst_string_to_utc_datetime(end_date)
        post_foods = food_info_dao.get_food_info(start_date=start_date, end_date=end_date)
    else:
        # 食事日時検索条件なし投稿一覧を取得
        post_foods = food_info_dao.get_food_info()

    if not post_foods:
        raise Http404

    try:
        return make_food_download_csv(download_filename, post_foods)
    except Exception as e:
        logger.error(e)
        raise Exception


def make_food_detail_download_file(request, food_id):
    download_filename = 'food_detail_file_'

    try:
        food_info_rows = PostFoods.objects.filter(id=food_id, user_id=request.user_id)
        if not food_info_rows:
            raise Http404
        return make_food_download_csv(download_filename, food_info_rows)
    except Exception as e:
        logger.error(e)
        raise Exception


def make_food_download_csv(download_filename, rows):
    file_contents = []
    file_content = []

    # ダウンロード用csvファイル名設定
    current_date = datetime.now()
    current_date_str = current_date.strftime('%Y%m%d%H%M')
    filename = download_filename + current_date_str + '.csv'

    # csvヘッダ設定
    csv_header = [
        'id',
        'タイトル',
        '料理名',
        '内容',
        '食事日時',
        '投稿日時'
    ]

    file_contents.append(csv_header)

    # csv内容設定
    for i, row in enumerate(rows, start=1):
        file_content.append(i)
        file_content.append(row.title)
        file_content.append(row.food_name)
        file_content.append(row.content)
        ate_at = utc_datetime_to_jst_datetime_format(row.ate_at)
        file_content.append(ate_at)
        created_at = utc_datetime_to_jst_datetime_format(row.created_at)
        file_content.append(created_at)

        file_contents.append(file_content)
        file_content = []

    # csv出力
    response = HttpResponse(content_type='text/csv;')
    response['Content-Disposition'] = "attachment; filename*=utf-8''%s" % urllib.parse.quote(filename, encoding='utf-8')

    writer = csv.writer(response)
    for line in file_contents:
        writer.writerow(line)

    return response
