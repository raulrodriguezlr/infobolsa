from dataclasses import dataclass, field
from typing import List
from .price_series import PriceSeries
import statistics

@dataclass
class Portfolio:
    name: str
    assets: List[PriceSeries] = field(default_factory=list)

    def clean(self):
        for asset in self.assets:
            asset.clean()

    def total_value_by_date(self):
        """Devuelve un diccionario fecha: valor total de la cartera en esa fecha (suma de cierres)."""
        date_values = {}
        for asset in self.assets:
            for p in asset.data:
                if p.date not in date_values:
                    date_values[p.date] = 0.0
                date_values[p.date] += p.close
        return dict(sorted(date_values.items()))

    def mean(self):
        """Media de los valores de cierre de todos los activos."""
        closes = []
        for asset in self.assets:
            closes += [p.close for p in asset.data]
        return statistics.mean(closes) if closes else float('nan')

    def volatility(self):
        """Volatilidad agregada de la cartera (simple, no ponderada)."""
        closes = []
        for asset in self.assets:
            closes += [p.close for p in asset.data]
        if len(closes) < 2:
            return float('nan')
        return statistics.stdev(closes)
