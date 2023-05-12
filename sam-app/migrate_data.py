import json

from domain.Picture import ImageIOS3, Picture
from infrastructure.repository.CatalogRepo import PictureCatalogRepo
from infrastructure.repository.DynamoDB import DynamoDB
from infrastructure.repository.S3 import S3
from infrastructure.system.Clock import RealClock
from use_cases.AddNewPicture import AddNewPicture, add_new_picture_from_s3

with open("error_log.txt", "w") as file:
    s3_files = S3().list_objects("svz-master-pictures-new", "original/2023")
    for count, s3_obj in enumerate(s3_files):
        try:
            print(f"#{count+1:<4} {s3_obj.key}")
            results = add_new_picture_from_s3(
                s3_obj.bucket + "/" + s3_obj.key, "master-pictures-catalog"
            )
        except Exception as e:
            print()
print(f"Processed: {len(s3_files)}")

# # Act
# repo = PictureCatalogRepo(DynamoDB("master-pictures-catalog"), RealClock())
# results = repo.get_recently_added()
# print(f"Found recently added: {len(results)}")
