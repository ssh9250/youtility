from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


# from .models import Holding, NewsItem
# from .serializers import (
#     HoldingSerializer, PortfolioSummarySerializer, NewsItemSerializer
# )
# from .services.stock_service import StockService
# from .services.news_service import NewsService


class HoldingViewSet(viewsets.ModelViewSet):
    """
    종목 CRUD + 포트폴리오 조회 + 뉴스 피드.

    GET    /api/stocks/holdings/              → 보유 목록
    POST   /api/stocks/holdings/              → 종목 추가
    GET    /api/stocks/holdings/{id}/         → 단일 조회
    PATCH  /api/stocks/holdings/{id}/         → 수정
    DELETE /api/stocks/holdings/{id}/         → 삭제
    GET    /api/stocks/holdings/portfolio/    → 포트폴리오 요약 (현재가 포함)
    GET    /api/stocks/holdings/news/         → 전체 뉴스 피드
    GET    /api/stocks/holdings/{id}/news/    → 종목별 뉴스
    """

    # queryset         = Holding.objects.all()
    # serializer_class = HoldingSerializer

    # ── CRUD는 ModelViewSet이 자동 제공 ──

    @action(detail=False, methods=["get"])
    def portfolio(self, request):
        """
        보유 종목 전체 + 현재가 + 손익 + 비중.
        StockService에서 현재가를 일괄 조회 후 각 holding에 annotate.
        """
        # holdings = self.get_queryset()
        # tickers  = list(holdings.values_list("ticker", flat=True))
        # prices   = StockService.get_bulk_prices(tickers)

        # enriched = []
        # total_cost = total_value = Decimal("0")
        # for h in holdings:
        #     cp  = prices.get(h.ticker) or h.avg_price   # fallback: 매수가
        #     cv  = h.quantity * cp
        #     pl  = cv - h.total_cost
        #     total_cost  += h.total_cost
        #     total_value += cv
        #     enriched.append((h, cp, cv, pl))

        # holdings_data = []
        # for h, cp, cv, pl in enriched:
        #     weight = float(cv / total_value * 100) if total_value else 0
        #     data   = PortfolioHoldingSerializer(h).data
        #     data.update({
        #         "current_price":   cp,
        #         "current_value":   cv,
        #         "profit_loss":     pl,
        #         "profit_loss_pct": float(pl / h.total_cost * 100) if h.total_cost else 0,
        #         "weight_pct":      weight,
        #     })
        #     holdings_data.append(data)

        # summary = {
        #     "total_cost":            total_cost,
        #     "total_current_value":   total_value,
        #     "total_profit_loss":     total_value - total_cost,
        #     "total_profit_loss_pct": float((total_value - total_cost) / total_cost * 100)
        #                              if total_cost else 0,
        #     "holdings": holdings_data,
        # }
        # return Response(PortfolioSummarySerializer(summary).data)
        return Response({})

    @action(detail=False, methods=["get"])
    def news(self, request):
        """전체 보유 종목 뉴스 피드 (최신순)."""
        # items = NewsItem.objects.select_related("holding").order_by("-published_at")[:50]
        # return Response(NewsItemSerializer(items, many=True).data)
        return Response([])

    @action(detail=True, methods=["get"])
    def news_by_holding(self, request, pk=None):
        """특정 종목의 뉴스 피드."""
        # holding = self.get_object()
        # items   = holding.news_items.order_by("-published_at")[:20]
        # return Response(NewsItemSerializer(items, many=True).data)
        return Response([])