from urllib.parse import urlparse

from fastapi import APIRouter
import requests


api_router = APIRouter(
    prefix='/api',
    tags=['api']
)


@api_router.get('/more_info')
def get_more_info(url: str = ''):
    """ Получить расширенную информацию по товару """
    domain = urlparse(url).netloc
    if "wildberries" in domain:
        path = "wildberries"
    elif "ozon" in domain:
        path = "ozon"
    else:
        path = "aliexpress"
    res = requests.get(f"http://127.0.0.1:8888/extended/{path}", params={"url": url}).json()

    # Имитируем реальный запрос
    # import time
    # time.sleep(2)

    # import json
    # with open('test_more_info.json', encoding='utf-8') as file:
    #     res = json.load(file)

    return res
