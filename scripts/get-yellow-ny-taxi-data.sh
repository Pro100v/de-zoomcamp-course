#!/bin/bash


# Получение абсолютного пути к директории, где находится скрипт
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Указание на папку data относительно директории скрипта
DEST_DIR=$(realpath "$SCRIPT_DIR/../data/csv/yellow")

# Проверка, существует ли папка назначения
if [[ ! -d "$DEST_DIR" ]]; then
  echo "Directory $DEST_DIR does not exist. Creating it..."
  mkdir -p "$DEST_DIR"
fi

# Вывод папки назначения для проверки
echo "Destination directory is set to: $DEST_DIR"
echo "Erase destination directory..."
rm -rIvf "$DEST_DIR/*"


# # URL страницы с файлами
# PAGE_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow"
#
# curl -s "$PAGE_URL" | \
# grep -oP 'https://github\.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/[^"]+\.csv\.gz' |
# echo 
#
# exit 0
# # Получение всех ссылок на файлы и скачивание через wget
# curl -s "$PAGE_URL" | \
# grep -oP 'https://github\.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/[^"]+\.csv\.gz' | \
# while read -r FILE_URL; do
#     wget -P "$DEST_DIR" "$FILE_URL"
# done


# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-02.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-03.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-04.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-05.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-06.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-07.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-08.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-09.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-10.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-11.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-12.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-02.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-03.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-04.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-05.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-06.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-07.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-08.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-09.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-10.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-11.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-12.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-02.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-03.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-04.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-05.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-06.csv.gz
# wget -P "$DEST_DIR" https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-07.csv.gz
#
BASE_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
DOWNLOAD_FILES="yellow_tripdata_2019-01.csv.gz \
yellow_tripdata_2019-02.csv.gz \
yellow_tripdata_2019-03.csv.gz \
yellow_tripdata_2019-04.csv.gz \
yellow_tripdata_2019-05.csv.gz \
yellow_tripdata_2019-06.csv.gz \
yellow_tripdata_2019-07.csv.gz \
yellow_tripdata_2019-08.csv.gz \
yellow_tripdata_2019-09.csv.gz \
yellow_tripdata_2019-10.csv.gz \
yellow_tripdata_2019-11.csv.gz \
yellow_tripdata_2019-12.csv.gz \
yellow_tripdata_2020-01.csv.gz \
yellow_tripdata_2020-02.csv.gz \
yellow_tripdata_2020-03.csv.gz \
yellow_tripdata_2020-04.csv.gz \
yellow_tripdata_2020-05.csv.gz \
yellow_tripdata_2020-06.csv.gz \
yellow_tripdata_2020-07.csv.gz \
yellow_tripdata_2020-08.csv.gz \
yellow_tripdata_2020-09.csv.gz \
yellow_tripdata_2020-10.csv.gz \
yellow_tripdata_2020-11.csv.gz \
yellow_tripdata_2020-12.csv.gz \
yellow_tripdata_2021-01.csv.gz \
yellow_tripdata_2021-02.csv.gz \
yellow_tripdata_2021-03.csv.gz \
yellow_tripdata_2021-04.csv.gz \
yellow_tripdata_2021-05.csv.gz \
yellow_tripdata_2021-06.csv.gz \
yellow_tripdata_2021-07.csv.gz" 

# Скачиваем все файлы 
DOWNLOADS_URLS=$(for f in $DOWNLOAD_FILES; do echo "$BASE_URL/$f"; done | xargs) 
echo "Downloads URL's:"
echo "$DOWNLOADS_URLS" | tr ' ' '\n\t-'
wget -P "$DEST_DIR/" $DOWNLOADS_URLS

# распаковываем все файлы 
gunzip $DEST_DIR/*.gz

echo "Job compleate successfully"

# DOWNLOAD_FILES="yellow_tripdata_2019-01.csv.gz \
# yellow_tripdata_2021-04.csv.gz \
# yellow_tripdata_2021-05.csv.gz \
# yellow_tripdata_2021-06.csv.gz \
# yellow_tripdata_2021-07.csv.gz" 

