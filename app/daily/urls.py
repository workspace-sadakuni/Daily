from django.urls import path

from daily.views import views
from daily.views import user_account
from daily.views import food

app_name = 'daily'

urlpatterns = [
    path('', user_account.user_login, name='user_login'),
    path('home', views.home, name='home'),
    path('register', user_account.register, name='register'),
    path('user_logout', user_account.user_logout, name='user_logout'),
    path('user_detail', user_account.user_detail, name='user_detail'),
    path('user_edit', user_account.user_edit, name='user_edit'),
    path('change_password', user_account.change_password, name='change_password'),
    path('user_delete', user_account.user_delete, name='user_delete'),

    path('food_input', food.food_input, name='food_input'),
    path('food_complete/<int:food_id>', food.food_complete, name='food_complete'),
    path('food_index', food.food_index, name='food_index'),
    path('food_search', food.food_search, name='food_search'),
    path('food_detail/<int:food_id>', food.food_detail, name='food_detail'),
    path('food_edit/<int:food_id>', food.food_edit, name='food_edit'),
    path('food_delete/<int:food_id>', food.food_delete, name='food_delete'),
    path('make_food_download_file', food.make_food_download_file, name='make_food_download_file'),
    path('make_food_detail_download_file/<int:food_id>', food.make_food_detail_download_file, name='make_food_detail_download_file'),
]
