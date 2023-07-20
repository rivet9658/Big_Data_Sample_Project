# 啟動步驟
1. 請先至 .env 檔將 DOMAINS 等設定進行調整，如果要調整 DB 設定的話，也需一併調整 docker-compose.yml 裡 db 的 environment 的各項參數。
2. 打開cmd指向專案路徑，輸入 docker build -t big_data_sample_project . 建立映像檔。
3. 建立好映像檔後執行 docker save -o big_data_sample_project.tar big_data_sample_project 輸出映像檔的.tar檔。
4. 將 2. 產出之 .tar 檔與 docker-compose.yml 加入 linux(這裡是用 ubuntu 23.04)機器上，並將 docker-compose.yml 放入 deploy.sh 檔第 3 行所指向的路徑與將 .tar 檔放入跟 deploy.sh 相同的路徑，設置好後請執行 sh deploy.sh 來啟動服務。

# 功能簡介
1. 包含文章、段落、標籤等資料新建，並且也能依據指定文章進行圖片上傳、評論增加等功能。
2. 有建置swagger，可以查看api列表。
