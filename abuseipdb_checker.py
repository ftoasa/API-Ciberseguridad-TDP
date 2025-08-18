import requests

# Configuración de AbuseIPDB (reemplaza con tu clave API)
ABUSEIPDB_API_KEY = "YOUR_ABUSEIPDB_API_KEY"  # Cambia por tu clave real
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

def check_abuseipdb(ip):
    """Consulta la API de AbuseIPDB para verificar una IP."""
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    try:
        response = requests.get(ABUSEIPDB_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})
        return {
            "status": "listed" if data.get("abuseConfidenceScore", 0) > 0 else "not_listed",
            "details": {
                "abuseConfidenceScore": data.get("abuseConfidenceScore", 0),
                "countryCode": data.get("countryCode", "Unknown"),
                "totalReports": data.get("totalReports", 0),
                "lastReportedAt": data.get("lastReportedAt", None)
            }
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "details": f"Error al consultar AbuseIPDB: {str(e)}"
        }