from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Holding(models.Model):
    """보유 종목 한 줄 = 티커 + 수량 + 매수가."""

    ticker = models.CharField(max_length=10)  # "AAPL", "005930.KS"
    name = models.CharField(max_length=100)  # "Apple Inc."
    quantity = models.DecimalField(
        max_digits=12, decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )
    avg_price = models.DecimalField(max_digits=14, decimal_places=4)  # 평균 매수가
    currency = models.CharField(max_length=3, default="USD")  # "USD", "KRW"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ticker"]

    def __str__(self):
        return f"{self.ticker} × {self.quantity}"

    # --- 계산 프로퍼티 (실제 현재가는 service 레이어에서 주입) ---
    @property
    def total_cost(self) -> Decimal:
        """총 매수 금액."""
        return self.quantity * self.avg_price


class NewsItem(models.Model):
    """보유 종목 관련 뉴스 1건."""

    holding = models.ForeignKey(
        Holding, on_delete=models.CASCADE, related_name="news_items"
    )
    title = models.CharField(max_length=300)
    summary = models.TextField(blank=True)
    url = models.URLField()
    source = models.CharField(max_length=100, blank=True)
    published_at = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        unique_together = ["holding", "url"]  # 중복 방지

    def __str__(self):
        return f"[{self.holding.ticker}] {self.title[:60]}"