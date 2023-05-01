# Creates md tables that can be used to document the DynamoDB PK strategyohhh


data = {
    "PICTURE": """pk,sk,gsi1_pk,gsi1_sk,s3_url
PICTURE,svz-master-pictures/original/1.jpg,x,y,svz-master-pictures/original/1.jpg
1,2,3,4,5
""",
    "GIS_CITY": """pk,sk,gsi1_pk,gsi1_sk
GIS,x
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
        file.write(f"## Table: {type}\n")
        data_rows = table_data.split("\n")
        file.write(format_line(data_rows[0]))
        headers = "|" + "|".join(["--" for c in data_rows[0].split(",")]) + "|\n"
        file.write(headers)
        for row in data_rows[1:]:
            file.write(format_line(row))
        file.write("\n\n")
