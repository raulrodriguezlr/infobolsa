# Configuración de secretos y API keys

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (puedes copiar de `.env.example`):

```
ALPHA_VANTAGE_API_KEY=tu_api_key_aqui
FINNHUB_API_KEY=tu_api_key_aqui
YAHOO_API_KEY=tu_api_key_aqui
OUTPUTS_BASE_PATH=outputs
```

- Consigue tus claves en las webs oficiales de cada API.
- No subas nunca tu `.env` real a GitHub.
- El código cargará automáticamente las claves desde `.env` usando `python-dotenv`.
