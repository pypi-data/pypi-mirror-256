import json
import logging
import time
import uuid
from threading import Thread

from zyjj_client_sdk.api import Api, TaskStatus
from zyjj_client_sdk.base import Base
from zyjj_client_sdk.storage import Storage
from zyjj_client_sdk.entity import EntityHelper, EntityAudio, EntitySubtitles
from zyjj_client_sdk.ffmpeg_sdk import FFMpegService
from zyjj_client_sdk.client import MqttServer, MqttEventType
from typing import Callable
from tencentcloud.common import credential


# 给回调函数使用的api
class HandleApi:
    def __init__(
            self,
            _base: Base,
            _api: Api,
            uid: str,
            task_id: str,
            _input: dict,
            mqtt: MqttServer,
            global_data: dict
    ):
        self.__base = _base
        self.__api = _api
        self.__ffmpeg = FFMpegService()
        self.__storage = Storage(_base, _api)
        self.__entity = EntityHelper(_base)
        self.__mqtt = mqtt
        self.__global_data = global_data

        self.__uid = uid
        self.__task_id = task_id
        self.__input = _input
        self.__output = {}
        self.__output_str = ''

    def update_progress(self, progress: float):
        self.__mqtt.send_task_event(self.__uid, self.__task_id, MqttEventType.Progress, progress)

    # 下载文件并返回耗时信息
    def download_duration(self, key: str) -> (str, float):
        audio_path = self.__storage.download_file(self.__input[key])
        return audio_path, self.__ffmpeg.get_duration(audio_path) * 1000

    # 直接提取云端文件的url
    def get_tencent_url_from_param_key(self, key: str) -> str:
        key = self.__base.get_path_from_params(self.__input[key])
        return self.__storage.tencent_get_file_url(key)

    # 获取文件的耗时信息(单位s)
    def get_file_duration_by_key(self, key: str) -> float:
        return self.__base.get_duration_from_params(self.__input[key])

    # 直接cos key中提取url
    def get_tencent_url_from_key(self, key: str):
        return self.__storage.tencent_get_file_url(key)

    # 获取用户积分
    def get_point(self) -> int:
        return self.__api.get_user_point(self.__uid)

    # 检查用户积分
    def check_point(self, point: int):
        if self.__api.get_user_point(self.__uid) < point:
            raise Exception("积分不足请充值")

    # 扣除用户积分
    def use_point(self, name: str, cost: float, desc=''):
        if not self.__api.use_user_point(self.__uid, name, cost, desc):
            raise Exception("积分不足请充值")

    # 更新任务花费
    def update_cost(self, name: str, cost: float, desc='') -> bool:
        return self.__api.task_update_task_cost(self.__uid, self.__task_id, name, cost, desc)

    # 上传字幕文件
    def upload_subtitle(self, key: str, subtitles: EntitySubtitles):
        subtitle_file = self.__entity.generate_subtitle_file(subtitles)
        self.__output[key] = self.__storage.upload_file(subtitle_file.file_path, self.__uid, 1)

    # 获取二进制的url链接
    def get_bytes_url(self, extend: str, data: bytes) -> str:
        key = f"tmp/{uuid.uuid4()}.{extend}"
        # 上传二进制
        self.__storage.tencent_upload_bytes(key, data)
        # 获取url
        return self.__storage.tencent_get_file_url(key)

    # 获取任务的原始输入
    def get_task_input(self) -> dict:
        return self.__input

    # 获取任务的输出
    def get_output(self) -> str:
        return json.dumps(self.__output)

    # mqtt发送成功信息
    def success(self, data: dict):
        self.__mqtt.send_task_event(self.__uid, self.__task_id, MqttEventType.Success, data)

    # 获取腾讯的认证信息
    def get_tencent_credential(self) -> credential.Credential:
        token = self.__api.could_get_tencent_token()
        return credential.Credential(token["TmpSecretId"], token["TmpSecretKey"])

    # 获取配置文件
    def get_config_data(self, key: str) -> dict:
        return self.__base.get_config_data(key)

    #  获取全局数据
    def get_global_data(self, key: str):
        return self.__global_data[key]


class SdkService:
    def __init__(self):
        self.__base = Base()
        self.__api = Api(self.__base)
        self.__handle = {}
        self.__mqtt = MqttServer(self.__api)
        self.__global_data = {}

    # 添加处理器
    def add_handle(self, task_type: int, handle: Callable[[HandleApi], None]):
        self.__handle[task_type] = handle

    # 添加全局变量
    def add_global(self, key: str, value: any):
        self.__global_data[key] = value

    # 启动服务
    def start(self):
        # 后台启动mqtt
        self.__mqtt.start_backend()

    # 停止服务
    def stop(self):
        self.__mqtt.close()

    # 开始处理任务
    def execute_task(self):
        # pull task
        task_info = self.__api.task_pull_task()
        if task_info is None:
            logging.info("[task] task not found")
            return
        logging.info(f'[task] pull task is {task_info}')
        # get task info
        uid = task_info['uid']
        task_type = task_info['task_type']
        task_input = task_info['input']
        task_id = task_info['id']
        # 寻找处理器
        if task_type in self.__handle:
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Start, "")
            try:
                handle_api = HandleApi(
                    self.__base,
                    self.__api,
                    uid,
                    task_id,
                    json.loads(task_input),
                    self.__mqtt,
                    self.__global_data
                )
                self.__handle[task_type](handle_api)
                self.__api.task_update_task(task_id, status=TaskStatus.Success, output=handle_api.get_output())
                self.__mqtt.send_task_event(uid, task_id, MqttEventType.Success, None)
            except Exception as e:
                self.__api.task_update_task(task_id, status=TaskStatus.Fail, extra=str(e))
                self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, str(e))
        else:
            err_info = f"task type {task_type} not found"
            logging.error(err_info)
            self.__api.task_update_task(task_id, status=TaskStatus.Fail, extra=err_info)
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, err_info)

    def _handle_task(self, uid: str, data: dict):
        task_type = data['task_type']
        task_id = data['task_id']
        task_data = data['data']
        try:
            if data['task_type'] in self.__handle:
                handle_api = HandleApi(
                    self.__base,
                    self.__api,
                    uid,
                    task_id,
                    task_data,
                    self.__mqtt,
                    self.__global_data
                )
                self.__handle[task_type](handle_api)
            else:
                logging.error(f"[sdk] task type {task_type} not found")
                self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, f"task type {task_type} not found")
        except Exception as e:
            logging.error(f"[sdk] task type {task_type} error {e}")
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, str(e))

    def __handle_task(self, topic: str, data: dict):
        uid = topic.split('/')[-1]
        logging.info(f"[sdk] get task from {uid}, data {data}")
        # 后台启动一个线程运行
        Thread(target=self._handle_task, args=(uid, data)).start()

    # 启动mqtt监听
    def start_mqtt(self):
        self.__mqtt.add_subscribe("task/+", self.__handle_task)
        self.__mqtt.start()
