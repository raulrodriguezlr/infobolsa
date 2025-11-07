
def fetch_sec_filings(ticker, form_type):
    # form_type: '10-K' or '10-Q'
    # Buscar CIK del ticker
    cik_url = "https://www.sec.gov/files/company_tickers_exchange.json"
    try:
        cik_resp = requests.get(cik_url)
        cik_data = cik_resp.json()
        cik = CIK
        for entry in cik_data.values():
            if entry.get('ticker', '').upper() == ticker.upper():
                cik = entry.get('cik_str')
                break
        if not cik:
            print(f"[INFO] No se encontró CIK para {ticker} en SEC.")
            return
    except Exception as e:
        print(f"[ERROR] Descarga CIK para {ticker}: {e}")
        return
    # Buscar los últimos filings del tipo solicitado
    search_url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"
    try:
        filings_resp = requests.get(search_url, headers={"User-Agent": "infobolsa/1.0"})
        filings_data = filings_resp.json()
        filings = filings_data.get('filings', {}).get('recent', {})
        forms = filings.get('form', [])
        accession_numbers = filings.get('accessionNumber', [])
        report_links = []
        for i, form in enumerate(forms):
            if form == form_type:
                acc_num = accession_numbers[i].replace('-', '')
                link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_num}/{accession_numbers[i]}.txt"
                report_links.append(link)
        if report_links:
            print(f"[INFO] Últimos {form_type} para {ticker}:")
            for l in report_links[:2]:
                print(f"- {l}")
        else:
            print(f"[INFO] No se encontró {form_type} reciente para {ticker} en SEC.")
    except Exception as e:
        print(f"[ERROR] Descarga filings SEC para {ticker}: {e}")