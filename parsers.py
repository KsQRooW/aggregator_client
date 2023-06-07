import requests

from cache import Cache


markets_colors = {
    'wildberries': '#481173',
    'ozon': '#005bff',
    'aliexpress': '#dc3545'
}


def get_rating_color(rating: float) -> str:
    """Выбор цвета в зависимости от значения оценки карточки"""
    if rating > 90:
        return '#198754'
    elif rating > 50:
        return '#ffc107'
    return '#dc3545'


class Cards:
    # Имитация БД, храним последние 5 запросов чтобы не парсить заново
    cache = Cache(max_items=5)
    api_url = 'http://127.0.0.1:8888'

    def __init__(self, search_query: str, k_comments_num: int, k_avg_review: int, k_price: int, k_text_match: int):
        """Запрос карточек товаров по поисковой строке"""
        self.items: list[dict] = []
        self._max_reviews = 0
        self._max_comments = 0
        self._max_reverse_price = 0
        self._max_text_accuracy = 0
        self._k_comments_num = k_comments_num
        self._k_avg_review = k_avg_review
        self._k_price = k_price
        self._k_text_match = k_text_match

        if search_query:
            cached_cards = self.cache.get_item(search_query)
            if cached_cards:
                self.items = cached_cards
                return

            self._request_new_cards(search_query)

    def extend_cards_info(self):
        """Расширить карточки товаров необходимыми параметрами"""
        self._get_max_params()
        for card in self.items:
            card['market_color'] = markets_colors.get(card['market'], '#343a40')
            card['rating'] = self._calculate_rating(card)
            card['rating_color'] = get_rating_color(card['rating'])

    def sorted(self, sort_by: str):
        """Отсортировать карточки"""
        return sorted(self.items, key=lambda item: item[sort_by], reverse=True)

    def filter(self, markets: list):
        """Отфильтровать карточки по маркетплейсам"""
        self.items = list(filter(lambda card: card['market'] in markets, self.items))

    def _request_new_cards(self, search_query: str):
        """Сделать запрос в АПИ парсера товаров"""
        requests.get(self.api_url + '/search', params={'input_name': search_query})

        # # Имитируем реальный запрос
        # time.sleep(2)
        # with open('test_search_full.json', encoding='utf-8') as file:
        #     self.items.extend(json.load(file))

        self.cache.add_item(search_query, self.items)

    def _get_max_params(self):
        """Найти максимальные параметры из списка карточек"""
        for card in self.items:
            if (reviews := card.get('reviews', 0)) > self._max_reviews:
                self._max_reviews = reviews
            if (comments := card.get('comments', 0)) > self._max_comments:
                self._max_comments = comments
            if (reverse_price := card.get('reverse_price', 0)) > self._max_reverse_price:
                self._max_reverse_price = reverse_price
            if (text_accuracy := card.get('text_accuracy', 0)) > self._max_text_accuracy:
                self._max_text_accuracy = text_accuracy

    def _calculate_rating(self, card: dict) -> float:
        """Высчитать оценку карточки товара с учетом весовых коэффициентов"""
        return round(
            sum((
                card.get('reviews', 0) / self._max_reviews * self._k_avg_review,
                card.get('comments', 0) / self._max_comments * self._k_comments_num,
                card.get('reverse_price', 0) / self._max_reverse_price * self._k_price,
                card.get('text_accuracy', 0) / self._max_text_accuracy * self._k_text_match
            )),
            2
        )
