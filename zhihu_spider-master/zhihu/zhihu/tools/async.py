# -*- coding=utf8 -*-
"""
    异步任务类
"""
import logging
import requests
from celery import Celery

from zhihu.settings import BROKER_URL

app = Celery('image_downloader', broker=BROKER_URL)
LOGGER = logging.getLogger(__name__)


@app.task
def download_pic(image_url, image_path):
    """异步下载图片

    Args:
        image_url (string): 图片链接
        image_path (string): 图片路径
    """
    if not (image_url and image_path):
        LOGGER.INFO('illegal parameter')

    try:
        image = requests.get(image_url, stream=True)
        with open(image_path, 'wb') as img:
            img.write(image.content)
    except Exception as exc:
        LOGGER.ERROR(exc)
