FOOD_INFO_SQL = '''
    {SELECT_CLAUSE}
    FROM
        post_foods
    {WHERE_CLAUSE}
    ORDER BY ate_at DESC
    LIMIT 999;
'''

FOOD_INFO_SELECT = '''
    SELECT
        id
        , title
        , food_name
        , ate_at
        , created_at
'''
