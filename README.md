# marketplaces_front

Фронт для АПИ парсера маркетплейсов AliExpress, Ozon, Wildberries

## Установка

Клонировать репозиторий и перейти в папку с проектом
```shell
git clone https://github.com/nparamonov/marketplaces_front.git
cd marketplaces_front
```
Создать виртуальное окружение
```shell
python -m venv venv
```
Активировать виртуальное окружение
```shell
# Для Linux:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate
```
Установить зависимости используя файл `requirements.txt`
```shell
pip install -r requirements.txt
```
Запустить сервер `uvicorn`
```shell
python main.py
```
По умолчанию сервер будет доступен в localhost (http://127.0.0.1:8000)
