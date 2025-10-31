from dataclasses import dataclass, field
from typing import List
from .price_series import PriceSeries
import statistics
from src.simulation.montecarlo import MonteCarloSimulator
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

    def monte_carlo_simulation(self, n_simulations=1000, n_days=252, mu_sigma_dict=None):
        """
        Realiza una simulación de Monte Carlo de la cartera usando MonteCarloSimulator.
        Devuelve un array (n_simulations, n_days+1) con el valor total simulado de la cartera.
        """
       
        sim = MonteCarloSimulator(n_simulations=n_simulations, n_days=n_days)
        return sim.simulate_portfolio(self, mu_sigma_dict)

    def report(self, show=True):
        """
        Genera un reporte en formato markdown con análisis relevante de la cartera.
        Si show=True, imprime el reporte por pantalla.
        """
        lines = []
        lines.append(f"# Reporte de Cartera: {self.name}\n")
        lines.append(f"**Número de activos:** {len(self.assets)}\n")
        lines.append(f"**Media de precios:** {self.mean():.2f}")
        lines.append(f"**Volatilidad:** {self.volatility():.2f}")
        # Advertencias
        if len(self.assets) == 0:
            lines.append("**ADVERTENCIA:** La cartera no contiene activos.\n")
        for asset in self.assets:
            if len(asset.data) < 2:
                lines.append(f"**ADVERTENCIA:** El activo {asset.symbol} tiene pocos datos.\n")
        lines.append("\n## Activos\n")
        for asset in self.assets:
            lines.append(f"- **{asset.symbol}**: {len(asset.data)} puntos, media={asset.mean():.2f}, volatilidad={asset.stdev():.2f}")
        report = "\n".join(lines)
        if show:
            print(report)
        return report
