## Partion Key: PICTURE
| pk  |  sk  |  gsi1_pk  |  gsi1_sk  |  gsi2_pk  |  gsi2_sk  |  gsi3_pk  |  gsi3_sk  |  gsi4_pk  |  gsi4_sk  |  gsi5_pk  |  gsi5_sk  |  s3_url |
|--|--|--|--|--|--|--|--|--|--|--|--|--|
| PICTURE  |  svz-master-pictures/original/1.jpg  |  LAST_SHOWN#landscape  |  2023-05-04_20  |  DATE_ADDED#landscape  |  2023-05-05T18:25:47.491913+00:00  |  ON_THIS_DAY#08-20  |  2014-08-20T09:21:31  |  UNIQUE_HASH  |  d9e20bed789ce3dbdad71003d14ae8d3  |  DATE_TAKEN  |  2014-08-20T09:21:31 |
|  |


## Partion Key: SHOWN_STATS_HISTORY (in mega table)
| pk  |  sk  |  gsi1_pk  |  gsi1_sk  |  s3_url  |  user_agent  |  viewport_height  |  viewport_width |
|--|--|--|--|--|--|--|--|
| SHOWN_STATS_HISTORY#2023-05  |  2023-05-01T01:12:23.868427  |  ORIGINAL_PICTURE#original/2012/2012_09_17_IMG_1364_-_Copy.jpg  |  2023-05-01T01:12:23.868427  |  svz-master-pictures/original/1.jpg  |  Mozilla  |  2000  |  1800 |
|  |


## Partion Key: GIS_CITY
| pk  |  sk  |  gsi1_pk  |  gsi1_sk  |  city  |  state_id  |  state_name |
|--|--|--|--|--|--|--|
| GIS  |  LAT_LONG#18;-65__18.1021;-65.4798  |  CITY#Esperanza  |  GIS_LAT;LONG#18.1021;-65.4798  |  Esperanza  |  CA  |  California |
|  |


## Partion Key: HASH_AVERAGE_HASH
| pk  |  sk  |  gsi1_pk  |  gsi1_sk  |  gsi2_pk  |  gsi2_sk  |  gsi3_pk  |  gsi3_sk  |  gsi4_pk  |  gsi4_sk  |  average_hash  |  s3_url |
|--|--|--|--|--|--|--|--|--|--|--|--|
| HASH_AVERAGE_HASH  |  svz-master-pictures/original/1.jpg  |  AVERAGE_HASH_1  |  abcd  |  AVERAGE_HASH_2  |  efgh  |  AVERAGE_HASH_3  |  ijkl  |  HASH_AVERAGE_HASH_4  |  lmno  |  abcdefghijklmn  |  svz-master-pictures/original/1.jpg |
|  |


## Partion Key: HASH_PHASH
| pk  |  sk  |  gsi1_pk  |  gsi1_sk  |  gsi2_pk  |  gsi2_sk  |  gsi3_pk  |  gsi3_sk  |  gsi4_pk  |  gsi4_sk  |  phash  |  s3_url |
|--|--|--|--|--|--|--|--|--|--|--|--|
| HASH_PHASH  |  svz-master-pictures/original/1.jpg  |  PHASH_1  |  abcd  |  PHASH_2  |  efgh  |  PHASH_3  |  ijkl  |  HASH_PHASH_4  |  lmno  |  abcdefghijklmn  |  svz-master-pictures/original/1.jpg |
|  |


