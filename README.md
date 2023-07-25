# 更新紀錄
1. 2023-07-21 13:00:00 更新部分 api return 結果。

# 服務配置
1. Python: 3.7.9
2. Django 3.2.20
3. MariaDB: 10.11.4

# 啟動步驟
1. 請先至 .env 檔將 DOMAINS 等設定進行調整，如果要調整 DB 設定的話，也需一併調整 docker-compose.yml 裡 db 的 environment 的各項參數。
2. 打開cmd指向專案路徑，輸入 docker build -t big_data_sample_project . 建立映像檔。
3. 建立好映像檔後執行 docker save -o big_data_sample_project.tar big_data_sample_project 輸出映像檔的.tar檔。
4. 將 3. 產出之 .tar 檔與 docker-compose.yml 加入 linux(這裡是用 ubuntu 23.04)機器上，並將 docker-compose.yml 放入 deploy.sh 檔第 3 行所指向的路徑與將 .tar 檔放入跟 deploy.sh 相同的路徑，設置好後請執行 sh deploy.sh 來啟動服務。
5. 正常情況下會自動新建一個 superuser，帳號：superadmin，密碼請參考 .env 裡的 SUPERADMIN_PASSWORD，並自動連結資料庫，若發生預期外的狀況，請嘗試以下 6.、7.。
6. 如果發現 django service 沒有連到 mariaDB，請幫我進入 big_data_sample_project 這個容器內(django service)，然後執行 mysql -h db -u root -p，密碼在 docker-compose 設定檔裡。
7. 如果發現沒有成功建立預設的 superuser，一樣請幫我進入 big_data_sample_project 這個容器內(django service)，然後執行 python manage.py createsuperuser 來建立 superuser。

# 功能簡介
1. 包含文章、段落、標籤等資料新建，並且也能依據指定文章進行圖片上傳、評論增加等功能，參考自 https://dailyview.tw/history 的熱門文章部份。
2. 以 jwt token 來驗證，請打 http://服務運行的ip:8000/api/token/ ，來獲取 jwt token，之後各 api 請在 header 帶入 "Bearer 你的token" 這樣的格式來請求 api。
3. 如果要 refresh token 請打 http://服務運行的ip:8000/api/token/refresh/ 並帶入你的 refresh token 來重新獲得 access toekn。
4. 詳細的 API 說明請參考 swagger 文檔，路徑為 http://服務運行的ip:8000/swagger/sample_prj/。

# Big Data Co., Ltd. 範例專案

> 此專案為 https://dailyview.tw/ 裡熱門文章功能的範例 API，包刮文章、段落新增，圖片的上傳，標籤、引用媒體的設定，以及不同使用者可對各文章進行評論等。

## 功能

**測試帳號密碼**

```
帳號： superadmin
密碼： 1qaz@WSX3edc
```

### 主要功能介紹
* 文章(article)：包含基本

* 段落(paragraph)：包含基本

* 標籤(tag)：包含基本

* 引用媒體(media)：包含基本

* 評論(comment)：包含基本

* 心情(emoji)：包含基本

* 驗證機制：
以 JWT 作為驗證機制，請使用以下 API 來獲取及更新 token

獲取 token
`POST /api/token/`
```
curl -i -H 'Accept: application/json' -d 'username={your username}&password={your password}' http://{your ip}:8000/api/token/
```
結果範例
```
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDI5Njk2MiwiaWF0IjoxNjkwMjk1MTYyLCJqdGkiOiJhNTdmMDY3YWM0ODc0YzkwOGJmNzM4Yzg4Y2U5OTExZSIsInVzZXJfaWQiOjF9.65Zs903KI3e4MJK9KeXYJUD8axyI8uJGx2GVleo0As0",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMjk1NzYyLCJpYXQiOjE2OTAyOTUxNjIsImp0aSI6ImY2YWQ2MDQyMDM4MjQyNWFhM2I5OGMwZGEwMWRlZGNmIiwidXNlcl9pZCI6MX0.3KY06rOJifBlediE-SRecOh_zv-RZ8glnPq9Um6kyiE"
}
```
更新 token
`POST /api/token/refresh/`
```
curl -i -H 'Accept: application/json' -d 'refresh={your refresh token}' http://{your ip}:8000/api/token/refresh/
```
結果範例
```
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMjk1Nzg4LCJpYXQiOjE2OTAyOTUxNjIsImp0aSI6IjA2MzBlZDIxODU0YTRlYmI5NWQ2YjdiMzVmYjA2ZGRjIiwidXNlcl9pZCI6MX0.kxWQyFv0PSY7G8cAd8B0shKD9jMe00V9S-Z3NFSl8BY"
}
```
