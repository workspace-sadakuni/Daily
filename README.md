# Daily

### コンセプト
日々の食事を投稿し記録するサービス 


### 開発環境構築
#下記コマンドにてコンテナ作成後、appサーバーでmigrateを実行。  
1. $docker-compose up -d --build  
2. $docker exec -it django bash  
3. $python3 manage.py makemigrations daily #念のため実施  
4. $python3 manage.py migrate  
#ブラウザより下記へ遷移  
http://127.0.0.1:8000/  
http://localhost/  


#### docker-composeコマンド一覧

#コンテナ作成&ビルド  
$docker-compose up -d --build  
#コンテナ停止&削除  
$docker-compose down -v  
#コンテナ起動  
$docker-compose start  
#コンテナ停止  
$docker-compose stop  
#apサーバーコンソールログ確認  
$docker logs -f django  
#コンテナ内へ接続(django=コンテナ名)  
$docker exec -it django bash  


#### 本番環境サーバー起動方法
#linux上で下記環境変数に使用する設定ファイルを定義  
export DJANGO_SETTINGS_MODULE=config.settings.production  
#上記環境変数定義後、サーバーを起動  
python3 manage.py runserver 0.0.0.0:8000  
