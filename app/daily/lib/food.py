from datetime import datetime
from pytz import timezone

from daily.lib.food_sql import FOOD_INFO_SQL, FOOD_INFO_SELECT
from daily.models import PostFoods


class FoodInfoDao:
    food_info_sql = FOOD_INFO_SQL
    food_info_select_clause = FOOD_INFO_SELECT
    model_class = PostFoods

    def __init__(self, user_id=None):
        self.user_id = user_id

    def get_food_info(self, start_date='', end_date='') -> list:
        """
        投稿food情報取得クエリ返却
        :param start_date: 検索条件食事日時最短日
        :param end_date: 検索条件食事日時最長日
        :return :
        """
        where_clause = 'WHERE user_id = %s'
        bind_params = [self.user_id]

        if start_date != '' and end_date == '':
            where_clause += 'AND ate_at >= %s'
            bind_params.append(start_date)
        elif start_date == '' and end_date != '':
            where_clause += 'AND ate_at <= %s'
            bind_params.append(end_date)
        elif start_date != '' and end_date != '':
            where_clause += 'AND ate_at BETWEEN %s AND %s'
            bind_params.insert(1, start_date)
            bind_params.insert(2, end_date)

        return self.model_class.objects.raw(
            self.food_info_sql.format(
                **{"SELECT_CLAUSE": self.food_info_select_clause,
                   "WHERE_CLAUSE": where_clause}
            ),
            bind_params
        )
