from fastapi import APIRouter

api_router = APIRouter(
    prefix='/api',
    tags=['api']
)


@api_router.get('/more_info')
def get_more_info(url: str = ''):
    """ Получить расширенную информацию по товару """

    # Имитируем реальный запрос
    import time
    time.sleep(2)

    import json
    with open('test_more_info.json', encoding='utf-8') as file:
        res = json.load(file)

    return res
