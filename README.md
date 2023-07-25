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

> 此專案是依據 https://dailyview.tw/ 裡熱門文章功能來製作的範例 API，包括文章、段落新增，圖片的上傳，標籤、引用媒體的設定，以及不同使用者可對各文章進行評論與發表心情等。

## 功能

**測試帳號密碼**

```
帳號： superadmin
密碼： 1qaz@WSX3edc
```

### 主要功能介紹
* 文章(article)：包含基本 crud 功能，可以查詢、新增、修改及刪除文章並能設定其底下之段落、標籤、持有圖片與引用媒體等內容，使用者也可針對各文章發表心情。

* 段落(paragraph)：包含基本 crud 功能，可藉由指定文章或段落之 id 來查詢、新增、修改及刪除文章的段落資料。

* 標籤(tag)：包含基本 crud 功能，用於管理標籤資料表，以利撰寫文章使用。

* 引用媒體(media)：包含基本 crud 功能，用於管理相關媒體的資料，以利設定文章之引用媒體資訊。

* 評論(comment)：包含基本 crud 功能，可藉由指定文章或評論之 id 來查詢、新增、修改及刪除文章的評論資料。

* 心情(emoji)：包含基本 crud 功能，用於管理使用者回饋心情資料表，以利使用者對不同文章發表心情。

* 驗證機制：本專案採用 JWT 來做為驗證機制。

### API 簡介

這裡會簡單介紹 token 的獲取及更新方法，以及文章基本的 crud 功能，詳細 API 資訊請先啟動服務後移至 `http://{ip}:8000/swagger/sample_prj/` 查看。

**獲取 token**

`POST /api/token/`
```
curl -i -H 'Accept: application/json' -X POST -d 'username={username}&password={password}' http://{ip}:8000/api/token/
```
**結果範例**
```
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDI5Njk2MiwiaWF0IjoxNjkwMjk1MTYyLCJqdGkiOiJhNTdmMDY3YWM0ODc0YzkwOGJmNzM4Yzg4Y2U5OTExZSIsInVzZXJfaWQiOjF9.65Zs903KI3e4MJK9KeXYJUD8axyI8uJGx2GVleo0As0",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMjk1NzYyLCJpYXQiOjE2OTAyOTUxNjIsImp0aSI6ImY2YWQ2MDQyMDM4MjQyNWFhM2I5OGMwZGEwMWRlZGNmIiwidXNlcl9pZCI6MX0.3KY06rOJifBlediE-SRecOh_zv-RZ8glnPq9Um6kyiE"
}
```
**更新 token**

`POST /api/token/refresh/`
```
curl -i -H 'Accept: application/json' -X POST -d 'refresh={refresh_token}' http://{ip}:8000/api/token/refresh/
```
**結果範例**
```
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMjk1Nzg4LCJpYXQiOjE2OTAyOTUxNjIsImp0aSI6IjA2MzBlZDIxODU0YTRlYmI5NWQ2YjdiMzVmYjA2ZGRjIiwidXNlcl9pZCI6MX0.kxWQyFv0PSY7G8cAd8B0shKD9jMe00V9S-Z3NFSl8BY"
}
```
**獲取所有文章列表**

`GET /api/sample_prj/article/`
```
curl -i -H 'Accept: application/json' -H "Authorization: Bearer {token}" -X GET http://{ip}:8000/api/sample_prj/article/?is_publish={true_or_false_or_blank}&start_publish_date={date_format}&end_publish_date={date_format}&tags={list[string]}
```
**結果範例**
```
{
    "msg": "獲得文章列表成功",
    "data": [
        {
            "id": 1,
            "author": "superadmin",
            "title": "《乘風2023》十大人氣選手聲量排行　成熟姐姐們魅力霸榜　Ella、A-Lin、美依禮芽你pick誰？",
            "introduction": "誰說只有青春無敵？這些乘風破浪的姐姐們帶你看見不一樣的致命吸引力！",
            "publish_datetime": "2023-06-16T10:00:00+08:00",
            "image_list": [
                {
                    "id": 2,
                    "order": 0,
                    "image": "/static/images/article/1/0/%E4%BC%8A%E5%B8%83.jpg",
                    "name": "測試圖片.jpg",
                    "source": "https://dailyview.tw/"
                }
            ],
            "have_paragraph": [
                {
                    "id": 1,
                    "order": 1
                },
                {
                    "id": 2,
                    "order": 2
                }
            ],
            "have_tag": [
                "乘風2023"
            ],
            "have_comment": [
                1
            ]
        }
    ]
}
```
**獲取單一文章**

`GET /api/sample_prj/article/{id}/`
```
curl -i -H 'Accept: application/json' -H "Authorization: Bearer {token}" -X GET http://{ip}:8000/api/sample_prj/article/{id}/
```
**結果範例**
```
{
    "msg": "獲得單一文章成功",
    "data": {
        "id": 1,
        "author": "superadmin",
        "title": "《乘風2023》十大人氣選手聲量排行　成熟姐姐們魅力霸榜　Ella、A-Lin、美依禮芽你pick誰？",
        "introduction": "誰說只有青春無敵？這些乘風破浪的姐姐們帶你看見不一樣的致命吸引力！",
        "publish_datetime": "2023-06-16T10:00:00+08:00",
        "image_list": [
            {
                "id": 2,
                "order": 0,
                "image": "/static/images/article/1/0/%E4%BC%8A%E5%B8%83.jpg",
                "name": "測試圖片.jpg",
                "source": "https://dailyview.tw/"
            }
        ],
        "have_paragraph": [
            {
                "id": 1,
                "order": 1
            },
            {
                "id": 2,
                "order": 2
            }
        ],
        "have_tag": [
            "乘風2023"
        ],
        "have_comment": [
            1
        ]
    }
}
```
**新增文章**

`POST /api/sample_prj/article/`
```
curl -i -H 'Accept: application/json' -H "Authorization: Bearer {token}" -X POST -d "title={string}&introduction={string}&is_publish={true_or_false}&publish_datetime={datetime_format}&paragraph_list={list[{title: string, content: string, order: number, style_code: string}]}&tag_list={list[{name: string}]}" http://{ip}:8000/api/sample_prj/article/
```
**結果範例**
```
{
    "msg": "文章新增成功",
    "data": {
        "title": "《乘風2023》十大人氣選手聲量排行　成熟姐姐們魅力霸榜　Ella、A-Lin、美依禮芽你pick誰？",
        "introduction": "誰說只有青春無敵？這些乘風破浪的姐姐們帶你看見不一樣的致命吸引力！",
        "is_publish": true,
        "publish_datetime": "2023-06-16 10:00:00.000000",
        "paragraph_list": [
            {
                "title": "熟齡姐姐魅力無法擋！",
                "content": "由中國芒果TV推出的選秀節目《乘風破浪的姐姐》今年已經來到第四季，不同於以青春少女為主的選秀，《乘風破浪的姐姐》帶大家看見熟齡「姐姐」們獨有的迷人魅力。在第四季節目《乘風2023》中，邀請到33位28歲以上的女性藝人參與，當中也不乏許多來自臺灣的選手...",
                "order": 2,
                "style_code": "1"
            },
            {
                "title": "NO. 10 朱珠（38歲）",
                "content": "IG：zhuzhuclubheaven/n在MTV全球音樂電視臺舉辦的「VJ大賽」（Video Jockey）中獲得北京賽區冠軍的朱珠，自此加入MTV並開始主持音樂節目《MTV天籟村》，之後便開啟了她的歌手之路。在2009年發行首張同名專輯《朱珠》後，朱珠獲得CCTV-MTV音樂盛典內地年度最受歡迎潛力歌手的提名...",
                "order": 2,
                "style_code": "2"
            }
        ],
        "tag_list": [
            {
                "name": "乘風2023"
            }
        ]
    }
}
```
**更新文章**

`PUT /api/sample_prj/article/{id}/`
```
curl -i -H 'Accept: application/json' -H "Authorization: Bearer {token}" -X PUT -d "title={string}&introduction={string}&is_publish={true_or_false}&publish_datetime={datetime_format}&paragraph_list={list[{title: string, content: string, order: number, style_code: string}]}&tag_list={list[{name: string}]}" http://{ip}:8000/api/sample_prj/article/{id}/
```
**結果範例**
```
{
    "msg": "文章更新成功",
    "data": {
        "title": "那些年大家找不到的停車位！揭密讓鄉民最痛苦的共享車租用困擾",
        "introduction": "近年來，共享汽機車逐漸成為大眾日常使用的交通方式，哪些優點最吸引你呢？",
        "is_publish": true,
        "publish_datetime": "2023-07-17 10:00:00.000000",
        "paragraph_list": [
            {
                "title": "新時代交通趨勢",
                "content": "暑假到了，全台各地都湧現出遊潮，你是否也收拾好行李、準備出遊去了呢？隨著科技服務日新月異，許多民眾出遊時的交通工具，比起以往更多了「共享汽機車」這個新選項，共享汽機車隨時租、隨時還的便利性，滿足民眾多樣化的移動需求，這些共享移動服務儼然已深入你我的生活，成為新時代的交通趨勢...",
                "order": 3,
                "style_code": "1"
            },
            {
                "title": "大家喜歡用共享車的原因有哪些？",
                "content": "「移動方式彈性又自由」是共享汽機車最大的優點，有接近6成的民眾都為此被吸引。相較於其他交通工具來說，不必受到班次、發車間距等限制，有需要時就能隨租隨用，不必擔心得在車站苦苦等候發車，或是車次誤點導致後續行程受影響，想臨時改變行程的彈性度較高...",
                "order": 4,
                "style_code": "1"
            },
            {
                "title": "填補大眾運輸網不足",
                "content": "相對於熱鬧的市區，住在郊區環境相對清幽且不擁擠，不過最令人困擾的缺點就是大眾交通工具網可能較不完善。一般通勤路線還好說，但若臨時有其他需求，必須移動到公車、捷運、火車都不好到達的地方時，這時候擁有適合的代步工具就很重要了！這也是共享車能吸引郊區使用者的強勢原因之一...",
                "order": 5,
                "style_code": "1"
            }
        ],
        "tag_list": [
            {
                "name": "旅遊"
            }
        ]
    }
}
```
**刪除文章**

`DELETE /api/sample_prj/article/{id}/`
```
curl -i -H 'Accept: application/json' -H "Authorization: Bearer {token}" -X DELETE http://{ip}:8000/api/sample_prj/article/{id}/
```
**結果範例**
```
{
    "msg": "文章刪除成功",
    "data": {
        "id": "1"
    }
}
```
