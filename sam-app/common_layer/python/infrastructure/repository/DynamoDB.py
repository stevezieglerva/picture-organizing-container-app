import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import time

import boto3


class RecordNotFound(Exception):
    pass


class UsingDynamoDB(ABC):
    @abstractmethod
    def __init__(self, table_name) -> None:
        raise NotImplemented

    @abstractmethod
    def put_item(self, record: dict) -> None:
        raise NotImplemented

    @abstractmethod
    def get_item(self, key: dict) -> dict:
        raise NotImplemented

    @abstractmethod
    def delete_item(self, ke: dict) -> None:
        raise NotImplemented

    @abstractmethod
    def query_table_equal(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    @abstractmethod
    def query_table_greater_than(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    @abstractmethod
    def query_table_begins(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    @abstractmethod
    def query_table_between(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> list:
        raise NotImplemented

    @abstractmethod
    def query_index_begins(self, index_name, key) -> list:
        raise NotImplemented

    @abstractmethod
    def scan_full(self) -> list:
        raise NotImplemented

    def _set_key_fields(self):
        table_resp = self._db.describe_table(TableName=self.table_name)
        key_schema = table_resp["Table"]["KeySchema"]
        self.key_fields = [k["AttributeName"] for k in key_schema]

    def set_ttl_seconds(self, seconds):
        self._ttl = seconds

    def convert_to_dynamodb_format(self, record):
        results = {}
        for k, v in record.items():
            data_type = ""
            new_value = str(v)
            if type(v) == str:
                data_type = "S"
            if type(v) == int or type(v) == float:
                data_type = "N"
            if type(v) == datetime:
                data_type = "N"
            if type(v) == dict:
                # convert to string for storage instead of using complicated dynamobd format for dicts
                data_type = "S"
                new_value = json.dumps(str(v), indent=3, default=str)
            if data_type == "":
                raise ValueError(f"no data type mapping for {type(v)}")

            new_field_value = {}
            new_field_value[data_type] = new_value
            results[k] = new_field_value
        return results

    def convert_from_dynamodb_format(self, db_record):
        return self.convert_from_dict_format(db_record["Item"])

    def convert_from_dict_format(self, dict):
        results = {}
        for k, v in dict.items():
            field_name = k
            for sub_k, sub_v in v.items():
                type = sub_k
                field_value = sub_v
                # try to convert to dict
                if type == "S":
                    if "{" in field_value:
                        try:
                            json_str = field_value.replace("'", '"')
                            json_str = json_str[1:]
                            json_str = json_str[:-1]
                            field_dict = json.loads(json_str)
                            field_value = field_dict
                        except json.decoder.JSONDecodeError:
                            # field is not JSON
                            pass
                if type == "N":
                    field_value = float(field_value)
            results[field_name] = field_value
        return results

    def convert_list_from_dynamodb_format(self, query_results):
        converted_results = []
        for item in query_results["Items"]:
            converted_results.append(self.convert_from_dict_format(item))
        return converted_results


class DynamoDB(UsingDynamoDB):
    def __init__(self, table_name):
        self._db = boto3.client("dynamodb")
        self.table_name = table_name
        self._set_key_fields()
        self._ttl = None
        self.limit = 2000

    def _set_key_fields(self):
        table_resp = self._db.describe_table(TableName=self.table_name)
        key_schema = table_resp["Table"]["KeySchema"]
        self.key_fields = [k["AttributeName"] for k in key_schema]

    def put_item(self, record) -> None:
        assert type(record) == dict, "record parameter needs to a dict"
        if self._ttl != None:
            ttl = self._calculate_ttl_epoch()
            record["ttl"] = ttl
        # print(f"record: {record}")
        db_format = self.convert_to_dynamodb_format(record)
        self._db.put_item(TableName=self.table_name, Item=db_format)
        # print(f"put item successful: {db_format}")

    def _calculate_ttl_epoch(self):
        future_time = datetime.now() + timedelta(self._ttl)
        return int(future_time.strftime("%s"))

        converted_results = []
        for item in query_results["Items"]:
            converted_results.append(self.convert_from_dict_format(item))
        return converted_results

    def get_item(self, key) -> dict:
        assert type(key) == dict, "Expecting key to be of type dict"
        db_format = self.convert_to_dynamodb_format(key)
        # print(f"Getting: {db_format}")
        db_record = self._db.get_item(TableName=self.table_name, Key=db_format)
        if "Item" not in db_record:
            raise RecordNotFound(f"key '{key}' not found")
        results = self.convert_from_dynamodb_format(db_record)
        return results

    def delete_item(self, key) -> None:
        assert type(key) == dict, "Expecting key to be of type dict"
        db_format = self.convert_to_dynamodb_format(key)
        # print(f"Deleting: {db_format}")
        db_record = self._db.delete_item(TableName=self.table_name, Key=db_format)

    def query_table_equal(
        self, key, index_name="", scan_index_forward: bool = True
    ) -> dict:
        expression_names_mapping = {}
        for count, key_name in enumerate(key.keys()):
            expression_names_mapping[key_name] = f"#{key_name}"
        key_condition_exp_parts = [
            f"{expression_names_mapping[k]} = :{k}" for k in key.keys()
        ]
        key_condition_exp = " AND ".join(key_condition_exp_parts)
        # print(f"key_condition_exp: {key_condition_exp}")
        return self._query_table_by_operator(
            key, key_condition_exp, index_name, scan_index_forward
        )

    def query_table_greater_than(
        self, key, index_name="", scan_index_forward: bool = True
    ):
        expression_names_mapping = {}

        for count, key_name in enumerate(key.keys()):
            expression_names_mapping[key_name] = f"#{key_name}"
        operators = ["=", ">="]
        key_condition_exp_parts = [
            f"{expression_names_mapping[k]} {operators[count]} :{k}"
            for count, k in enumerate(key.keys())
        ]
        key_condition_exp = " AND ".join(key_condition_exp_parts)
        # print(f"key_condition_exp: {key_condition_exp}")
        return self._query_table_by_operator(
            key, key_condition_exp, index_name, scan_index_forward
        )

    def query_table_begins(self, key, index_name="", scan_index_forward: bool = True):
        key_names = list(key.keys())
        if len(key_names) == 1:
            field_name = key_names[0]
            key_condition_exp = f"begins_with( {field_name}, :{field_name} )"
        if len(key_names) == 2:
            field_name_1 = key_names[0]
            field_name_2 = key_names[1]
            key_condition_exp = f"#{field_name_1} = :{field_name_1} AND begins_with( #{field_name_2}, :{field_name_2})"
        # print(f"key_condition_exp: {key_condition_exp}")
        return self._query_table_by_operator(
            key, key_condition_exp, index_name, scan_index_forward
        )

    def query_table_between(self, key, index_name="", scan_index_forward: bool = True):
        key_names = list(key.keys())
        assert len(key_names) == 2, f"Expected key to have the pk and sk: {key}"
        if len(key_names) == 1:
            field_name = key_names[0]
            key_condition_exp = f"begins_with( {field_name}, :{field_name} )"
        if len(key_names) == 2:
            field_name_1 = key_names[0]
            field_name_2 = key_names[1]
            key_condition_exp = f"#{field_name_1} = :{field_name_1} AND #{field_name_2} between :{field_name_2}_val_1 AND :{field_name_2}_val_2"
        # print(f"key_condition_exp: {key_condition_exp}")
        return self._query_table_by_operator(
            key, key_condition_exp, index_name, scan_index_forward
        )

    def query_index_begins(self, index_name, key):
        return self.query_table_begins(key, index_name)

    def scan_full(self):
        scan_results = self._db.scan(TableName=self.table_name)
        return self.convert_list_from_dynamodb_format(scan_results)

    def _query_table_by_operator(
        self, key, key_condition_exp, index_name="", scan_index_forward: bool = True
    ):
        assert type(key) == dict, "Expecting key to be of type dict"
        exp_attribute_values = key
        original_key_list = list(key.keys())
        # print(f"original_key_list: {original_key_list}")
        print(f"key_condition_exp: {key_condition_exp}")

        expression_names_mapping = {}
        for count, key_name in enumerate(original_key_list):
            expression_names_mapping[key_name] = f"#{key_name}"

        for key_name in original_key_list:
            mapped_field_name = expression_names_mapping[key_name]
            # print(f"mapped_field_name: {mapped_field_name}")
            expr_key_name = f":{key_name}"
            exp_attribute_values[expr_key_name] = key[key_name]
            exp_attribute_values.pop(key_name)
        print(f"exp_attribute_values: {exp_attribute_values}")

        if "between" in key_condition_exp:
            exp_attribute_values_db_format = {
                ":pk": {"S": exp_attribute_values[":pk"]},
                ":sk_val_1": {"S": str(exp_attribute_values[":sk"][0])},
                ":sk_val_2": {"S": str(exp_attribute_values[":sk"][1])},
            }
        else:
            exp_attribute_values_db_format = self.convert_to_dynamodb_format(
                exp_attribute_values
            )
        print(f"exp_attribute_values_db_format: {exp_attribute_values_db_format}")
        exp_attribute_names = {
            f"{expression_names_mapping[n]}": f"{n}" for n in expression_names_mapping
        }
        print(f"exp_attribute_names: {exp_attribute_names}")
        if index_name == "":
            query_response = self._db.query(
                TableName=self.table_name,
                KeyConditionExpression=key_condition_exp,
                ExpressionAttributeValues=exp_attribute_values_db_format,
                ExpressionAttributeNames=exp_attribute_names,
                Limit=self.limit,
                ScanIndexForward=scan_index_forward,
            )
        else:
            query_response = self._db.query(
                TableName=self.table_name,
                IndexName=index_name,
                KeyConditionExpression=key_condition_exp,
                ExpressionAttributeValues=exp_attribute_values_db_format,
                ExpressionAttributeNames=exp_attribute_names,
                Limit=self.limit,
                ScanIndexForward=scan_index_forward,
            )
        results = self.convert_list_from_dynamodb_format(query_response)
        return results
