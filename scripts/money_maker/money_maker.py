from S3 import S3Base


class MoneyMaker:
    def __init__(self, s3: S3Base):
        self.__s3 = s3

    def get_files(self, prefix: str, suffix: str = None) -> list:
        list = self.__s3.list_objects("svz-master-pictures-new", prefix)
        if suffix == None:
            return list
        return [o for o in list if o.key[-3:].lower() == suffix.lower()]

    def get_new_db_filename(self, old_filename: str) -> str:
        return old_filename
