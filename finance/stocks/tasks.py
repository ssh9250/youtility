from celery import shared_task
from .models import Holding, NewsItem
from .services.news_service import NewsService


# @shared_task
def refresh_news_for_all_holdings():
    """
    매일 정해진 시간에 전체 보유 종목 뉴스 갱신.
    celery beat 스케줄 예시 (settings.py):
        CELERY_BEAT_SCHEDULE = {
            "refresh-stock-news": {
                "task": "finance.stocks.tasks.refresh_news_for_all_holdings",
                "schedule": crontab(hour=8, minute=0),   # 매일 오전 8시
            }
        }
    """
    # svc      = NewsService()
    # holdings = Holding.objects.all()
    # created  = 0
    # for holding in holdings:
    #     articles = svc.fetch_for_ticker(holding.ticker)
    #     for a in articles:
    #         _, is_new = NewsItem.objects.get_or_create(
    #             holding=holding,
    #             url=a["url"],
    #             defaults={
    #                 "title":        a["title"],
    #                 "summary":      a["summary"],
    #                 "source":       a["source"],
    #                 "published_at": a["published_at"],
    #             },
    #         )
    #         if is_new:
    #             created += 1
    # return f"Created {created} new news items"
    pass