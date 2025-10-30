import os
from datetime import datetime
from src.variables import OUTPUTS_BASE_PATH, OUTPUTS_DATE_FORMAT

class OutputManager:
    """
    Gestiona la creación de carpetas y guardado de archivos de datos y gráficos.
    """
    def __init__(self):
        now = datetime.now().strftime(OUTPUTS_DATE_FORMAT)
        self.base_dir = os.path.join(OUTPUTS_BASE_PATH, now)
        os.makedirs(self.base_dir, exist_ok=True)

    def get_path(self, filename: str) -> str:
        return os.path.join(self.base_dir, filename)

    def save_dataframe(self, df, filename: str):
        path = self.get_path(filename)
        df.to_csv(path, index=False)
        return path

    def save_plot(self, plt, filename: str):
        path = self.get_path(filename)
        plt.savefig(path)
        return path
