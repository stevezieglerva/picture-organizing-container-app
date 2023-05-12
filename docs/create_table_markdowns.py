# Creates md tables that can be used to document the DynamoDB PK strategyohhh


# {
#  "pk": "PICTURE",
#  "sk": "svz-master-pictures-new/original/2014/2014_08_20_Disney_2014_2014_08_20_999_52_-_Copy.jpg",
#  "city": "",
#  "date_added": "2023-05-05 18:25:47.491913+00:00",
#  "date_taken": "2014-08-20 09:21:31",
#  "date_updated": "2023-05-05 18:25:47.491920+00:00",
#  "day": 20,
#  "gis_lat": -1,
#  "gis_long": -1,
#  "gsi1_pk": "LAST_SHOWN#landscape",
#  "gsi1_sk": "2023-05-04_20",
#  "gsi2_pk": "DATE_ADDED#landscape",
#  "gsi2_sk": "2023-05-05T18:25:47.491913+00:00",
#  "gsi3_pk": "ON_THIS_DAY#08-20",
#  "gsi3_sk": "2014-08-20T09:21:31",
#  "gsi4_pk": "UNIQUE_HASH",
#  "gsi4_sk": "d9e20bed789ce3dbdad71003d14ae8d3",
#  "gsi5_pk": "DATE_TAKEN",
#  "gsi5_sk": "2014-08-20T09:21:31",
#  "hash_average_hash": "31fffc6606787830",
#  "hash_crop_resistant": "e7c6c8ccced26142,e644e78787868002,e6c20b3b1a9a9ad8,4c3ca78d97171e18,1001945c6221c14c,5b1b1bbd3c3d1913,fcf9babb93950707",
#  "hash_phash": "c7b24f38364a583e",
#  "hash_unique": "d9e20bed789ce3dbdad71003d14ae8d3",
#  "height": 2304,
#  "last_shown": "2023-05-04 18:25:47.491913+00:00",
#  "layout": "landscape",
#  "model": "Canon EOS REBEL T3i",
#  "month": 8,
#  "s3_url": "svz-master-pictures-new/original/2014/2014_08_20_Disney_2014_2014_08_20_999_52_-_Copy.jpg",
#  "state": "",
#  "ulid": "01GZPJKEF477CYG1ARAH4JPCY3",
#  "update_desc": "05/05/23-created",
#  "view_count": 0,
#  "width": 3456,
#  "year": 2014
# }

data = {
    "PICTURE": """pk,sk,gsi1_pk,gsi1_sk,gsi2_pk,gsi2_sk,gsi3_pk,gsi3_sk,gsi4_pk,gsi4_sk,gsi5_pk,gsi5_sk,s3_url
PICTURE,svz-master-pictures/original/1.jpg,LAST_SHOWN#landscape,2023-05-04_20,DATE_ADDED#landscape,2023-05-05T18:25:47.491913+00:00,ON_THIS_DAY#08-20,2014-08-20T09:21:31,UNIQUE_HASH,d9e20bed789ce3dbdad71003d14ae8d3,DATE_TAKEN,2014-08-20T09:21:31
""",
    "SHOWN_STATS_HISTORY (in mega table)": """pk,sk,gsi1_pk,gsi1_sk,s3_url,user_agent,viewport_height,viewport_width
SHOWN_STATS_HISTORY#2023-05,2023-05-01T01:12:23.868427,ORIGINAL_PICTURE#original/2012/2012_09_17_IMG_1364_-_Copy.jpg,2023-05-01T01:12:23.868427,svz-master-pictures/original/1.jpg,Mozilla,2000,1800
""",
    "GIS_CITY": """pk,sk,gsi1_pk,gsi1_sk,city,state_id,state_name
GIS,LAT_LONG#18;-65__18.1021;-65.4798,CITY#Esperanza,GIS_LAT;LONG#18.1021;-65.4798,Esperanza,CA,California
""",
    "HASH_AVERAGE_HASH": """pk,sk,gsi1_pk,gsi1_sk,gsi2_pk,gsi2_sk,gsi3_pk,gsi3_sk,gsi4_pk,gsi4_sk,average_hash,s3_url
HASH_AVERAGE_HASH,svz-master-pictures/original/1.jpg,AVERAGE_HASH_1,abcd,AVERAGE_HASH_2,efgh,AVERAGE_HASH_3,ijkl,HASH_AVERAGE_HASH_4,lmno,abcdefghijklmn,svz-master-pictures/original/1.jpg
""",
    "HASH_PHASH": """pk,sk,gsi1_pk,gsi1_sk,gsi2_pk,gsi2_sk,gsi3_pk,gsi3_sk,gsi4_pk,gsi4_sk,phash,s3_url
HASH_PHASH,svz-master-pictures/original/1.jpg,PHASH_1,abcd,PHASH_2,efgh,PHASH_3,ijkl,HASH_PHASH_4,lmno,abcdefghijklmn,svz-master-pictures/original/1.jpg
""",
}


def format_line(line: str) -> str:
    new_line = "| " + line.replace(",", "  |  ") + " |\n"
    return new_line


with open("dynamob_tables.md", "w") as file:
    for type, table_data in data.items():
        file.write(f"## Partion Key: {type}\n")
        data_rows = table_data.split("\n")
        file.write(format_line(data_rows[0]))
        headers = "|" + "|".join(["--" for c in data_rows[0].split(",")]) + "|\n"
        file.write(headers)
        for row in data_rows[1:]:
            file.write(format_line(row))
        file.write("\n\n")
