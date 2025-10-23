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
        """
        Calcula la media de los precios de cierre de la serie.
        """
        closes = []
        for p in self.data:
            closes.append(p.close)
        if closes:
            return statistics.mean(closes)
        return float('nan')

    def stdev(self):
        """
        Calcula la desviación típica de los precios de cierre de la serie.
        """
        closes = []
        for p in self.data:
            closes.append(p.close)
        if len(closes) > 1:
            return statistics.stdev(closes)
        return float('nan')

    def clean(self):
        """
        Elimina puntos con valores no válidos y ordena la serie por fecha.
        """
        cleaned = []
        for p in self.data:
            if not math.isnan(p.close):
                cleaned.append(p)
        self.data = cleaned
        self.data.sort(key=lambda p: p.date)

    def total_return(self):
        """
        Calcula el rendimiento total de la serie (último cierre / primer cierre - 1).
        """
        if len(self.data) < 2:
            return float('nan')
        first = self.data[0].close
        last = self.data[-1].close
        return (last / first) - 1

    def annualized_return(self):
        """
        Calcula el rendimiento anualizado de la serie.
        """
        if len(self.data) < 2:
            return float('nan')
        days = (self.data[-1].date - self.data[0].date).days
        if days == 0:
            return float('nan')
        total_ret = self.total_return() + 1
        return total_ret ** (365 / days) - 1

    def volatility(self):
        """
        Calcula la volatilidad anualizada de la serie usando los rendimientos logarítmicos diarios.
        """
        if len(self.data) < 2:
            return float('nan')
        returns = []
        for i in range(1, len(self.data)):
            prev = self.data[i-1].close
            curr = self.data[i].close
            if prev > 0:
                log_ret = math.log(curr / prev)
                returns.append(log_ret)
        if len(returns) < 2:
            return float('nan')
        return statistics.stdev(returns) * math.sqrt(252)

    def max_drawdown(self):
        """
        Calcula el máximo drawdown (caída máxima desde un máximo anterior) de la serie.
        """
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
