import matplotlib.pyplot as plt
from src.utils.output_manager import OutputManager

output_manager = OutputManager()

def plot_price_series(price_series, show=True):
    dates = price_series.data['date'] if hasattr(price_series, 'data') else [p.date for p in price_series.data]
    closes = price_series.data['close'] if hasattr(price_series, 'data') else [p.close for p in price_series.data]
    plt.figure(figsize=(10, 4))
    plt.plot(dates, closes, label=price_series.ticker if hasattr(price_series, 'ticker') else price_series.symbol)
    plt.title(f"Precio histórico: {getattr(price_series, 'ticker', getattr(price_series, 'symbol', ''))}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.legend()
    plt.tight_layout()
    filename = f"{getattr(price_series, 'ticker', getattr(price_series, 'symbol', ''))}_historical_plot.png"
    output_manager.save_plot(plt, filename)
    if show:
        plt.show()
    plt.close()

def plot_portfolio_simulation(simulation_result, n_simulations=100, title="Simulación Monte Carlo de Cartera", show=True):
    plt.figure(figsize=(10, 4))
    for i in range(min(n_simulations, simulation_result.shape[0])):
        plt.plot(simulation_result[i], color="blue", alpha=0.1)
    plt.title(title)
    plt.xlabel("Días")
    plt.ylabel("Valor simulado")
    plt.tight_layout()
    filename = f"portfolio_montecarlo_plot.png"
    output_manager.save_plot(plt, filename)
    if show:
        plt.show()
    plt.close()
