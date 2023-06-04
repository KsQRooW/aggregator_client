from fastapi import APIRouter, Request, responses, Query
from fastapi.templating import Jinja2Templates
from parsers import Cards

pages_router = APIRouter(
    prefix='',
    tags=['pages']
)

templates = Jinja2Templates(directory="templates")


@pages_router.get('/')
def get_index_page(request: Request,
                   search_query: str = '',
                   k_comments_num: int = 25,
                   k_avg_review: int = 10,
                   k_price: int = 50,
                   k_text_match: int = 15,
                   sort_by: str = 'rating',
                   f_market: list[str] | None = Query(default=None)):
    """ Главная страница """

    if f_market is None:
        f_market = ['wildberries', 'ozon', 'aliexpress']

    if sum((k_comments_num, k_avg_review, k_price, k_text_match)) != 100:
        return responses.JSONResponse(
            {'status': 'error', 'msg': 'Сумма весовых коэффициентов должна быть равна 100'},
            400
        )

    cards = Cards(search_query, k_comments_num, k_avg_review, k_price, k_text_match)
    cards.extend_cards_info()
    cards.filter(markets=f_market)

    context = {
        'request': request,
        'search_query': search_query,
        'cards': cards.sorted(sort_by),
        'k_comments_num': k_comments_num,
        'k_avg_review': k_avg_review,
        'k_price': k_price,
        'k_text_match': k_text_match,
        'sort_by': sort_by,
        'f_market': f_market
    }

    return templates.TemplateResponse("index.html", context)
