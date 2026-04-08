from rest_framework import serializers
from .models import Holding, NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # NewsItem
        fields = ["id", "title", "summary", "url", "source", "published_at"]


class HoldingSerializer(serializers.ModelSerializer):
    """기본 CRUD용."""

    class Meta:
        model = Holding
        fields = [
            "id", "ticker", "name",
            "quantity", "avg_price", "currency",
            "total_cost",
            "created_at", "updated_at",
        ]
        read_only_fields = ["total_cost", "created_at", "updated_at"]


class PortfolioHoldingSerializer(HoldingSerializer):
    """포트폴리오 조회 시 현재가·손익 포함 확장 버전."""

    current_price = serializers.DecimalField(
        max_digits=14, decimal_places=4, read_only=True
    )
    current_value = serializers.DecimalField(
        max_digits=16, decimal_places=4, read_only=True
    )
    profit_loss = serializers.DecimalField(
        max_digits=16, decimal_places=4, read_only=True
    )
    profit_loss_pct = serializers.FloatField(read_only=True)
    weight_pct = serializers.FloatField(read_only=True)  # 포트폴리오 비중

    class Meta(HoldingSerializer.Meta):
        fields = HoldingSerializer.Meta.fields + [
            "current_price", "current_value",
            "profit_loss", "profit_loss_pct", "weight_pct",
        ]


class PortfolioSummarySerializer(serializers.Serializer):
    """포트폴리오 전체 요약."""

    total_cost = serializers.DecimalField(max_digits=18, decimal_places=4)
    total_current_value = serializers.DecimalField(max_digits=18, decimal_places=4)
    total_profit_loss = serializers.DecimalField(max_digits=18, decimal_places=4)
    total_profit_loss_pct = serializers.FloatField()
    holdings = PortfolioHoldingSerializer(many=True)