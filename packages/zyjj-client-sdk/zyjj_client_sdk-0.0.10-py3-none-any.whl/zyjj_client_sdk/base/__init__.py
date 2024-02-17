import json
import logging
import uuid


class Base:
    def __init__(self):
        data = json.loads(open("config.json", "r").read())
        logging.info(f"config info {data}")
        self.username = data["username"]
        self.password = data["password"]
        self.host = data["host"]
        self.__config = data
        self.tmp_dir = "/tmp"

    def generate_file(self, extend: str) -> str:
        return f"{self.tmp_dir}/{str(uuid.uuid4())}.{extend}"

    def generate_file_with_key(self, key: str) -> str:
        return self.generate_file(key.split(".")[-1])

    # 从参数中提取文件路径
    def get_path_from_params(self, data: dict) -> str:
        return json.loads(data['param_data'])['path']

    # 从参数中提取耗时信息
    def get_duration_from_params(self, data: dict) -> float:
        return json.loads(data['param_data'])['duration']

    # 从参数中获取大小信息
    def get_size_from_params(self, data: dict) -> int:
        return json.loads(data['param_data'])['size']

    # 获取配置文件
    def get_config_data(self, key: str):
        return self.__config[key]
