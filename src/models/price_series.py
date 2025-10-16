from dataclasses import dataclass, field
from datetime import date
from typing import List
import statistics
import math

@dataclass
class PricePoint:
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class PriceSeries:
    symbol: str
    currency: str
    data: List[PricePoint] = field(default_factory=list)

    def mean(self):
        closes = [p.close for p in self.data]
        return statistics.mean(closes) if closes else float('nan')

    def stdev(self):
        closes = [p.close for p in self.data]
        return statistics.stdev(closes) if len(closes) > 1 else float('nan')

    def clean(self):
        """Elimina puntos con valores no válidos y ordena por fecha."""
        self.data = [p for p in self.data if not math.isnan(p.close)]
        self.data.sort(key=lambda p: p.date)

    def total_return(self):
        """Rendimiento total de la serie."""
        if len(self.data) < 2:
            return float('nan')
        return (self.data[-1].close / self.data[0].close) - 1

    def annualized_return(self):
        """Rendimiento anualizado."""
        if len(self.data) < 2:
            return float('nan')
        days = (self.data[-1].date - self.data[0].date).days
        if days == 0:
            return float('nan')
        total_ret = self.total_return() + 1
        return total_ret ** (365 / days) - 1

    def volatility(self):
        """Volatilidad anualizada (desviación típica de los rendimientos diarios)."""
        if len(self.data) < 2:
            return float('nan')
        returns = [math.log(self.data[i].close / self.data[i-1].close) for i in range(1, len(self.data)) if self.data[i-1].close > 0]
        if len(returns) < 2:
            return float('nan')
        return statistics.stdev(returns) * math.sqrt(252)

    def max_drawdown(self):
        """Máximo drawdown de la serie."""
        if not self.data:
            return float('nan')
        max_close = -float('inf')
        max_dd = 0.0
        for p in self.data:
            if p.close > max_close:
                max_close = p.close
            dd = (p.close - max_close) / max_close
            if dd < max_dd:
                max_dd = dd
        return abs(max_dd)
