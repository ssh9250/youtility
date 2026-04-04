from decimal import Decimal
from typing import Optional
import yfinance as yf

class StockService:
    """yfinance를 통한 현재가 조회."""

    @staticmethod
    def get_current_price(ticker: str) -> Optional[Decimal]:
        """
        단일 종목 현재가 반환.
        실패 시 None 반환 (호출부에서 처리).
        """
        try:
            # info = yf.Ticker(ticker).fast_info
            # return Decimal(str(info["last_price"]))
            pass
        except Exception:
            return None

    @staticmethod
    def get_bulk_prices(tickers: list[str]) -> dict[str, Optional[Decimal]]:
        """
        복수 종목 현재가 일괄 조회.
        반환: {"AAPL": Decimal("189.50"), "005930.KS": Decimal("72000"), ...}
        """
        result: dict[str, Optional[Decimal]] = {}
        for ticker in tickers:
            result[ticker] = StockService.get_current_price(ticker)
        return result