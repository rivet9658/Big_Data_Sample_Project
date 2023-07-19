# 啟動步驟
1. 打開cmd指向專案路徑，輸入 docker build -t big_data_sample_project . 建立映像檔。
2. 建立好映像檔後執行 docker save -o big_data_sample_project.tar big_data_sample_project 輸出映像檔的.tar檔。
3. 將2.產出之.tar檔與docker-compose.yml依照deploy.sh的路徑放置，之後執行deploy.sh檔，來啟動服務。

# 功能簡介
1. 包含文章、段落、標籤等資料新建，並且也能依據指定文章進行圖片上傳、評論增加等功能。
2. 有建置swagger，可以查看api列表。
