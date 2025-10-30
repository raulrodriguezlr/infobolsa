import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia un DataFrame: elimina duplicados, rellena valores faltantes y ordena por fecha.
    """
    df = df.drop_duplicates()
    df = df.sort_values('date')
    # Rellenar valores faltantes con forward fill, luego backward fill si quedan (sin usar método deprecated)
    df = df.ffill().bfill()
    return df

def check_temporal_consistency(df: pd.DataFrame) -> bool:
    """
    Verifica que las fechas sean consistentes y no haya gaps grandes.
    """
    if 'date' not in df.columns:
        return False
    dates = pd.to_datetime(df['date'])
    diffs = dates.diff().dt.days.dropna()
    return diffs.max() <= 7  # Por ejemplo, no más de 7 días entre datos
