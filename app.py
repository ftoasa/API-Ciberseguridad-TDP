from flask import Flask, request, jsonify
   import requests

   app = Flask(__name__)

   # Base de datos simulada de IPs en lista negra (para ejemplo)
   BLACKLIST = {
       "192.168.1.100": {"reason": "Malware distribution", "severity": "High"},
       "10.0.0.50": {"reason": "Brute force attacks", "severity": "Medium"},
       "172.16.254.1": {"reason": "Phishing", "severity": "Low"}
   }

   # Configuración de AbuseIPDB (reemplaza con tu clave API)
   ABUSEIPDB_API_KEY = "YOUR_ABUSEIPDB_API_KEY"  # Cambia por tu clave real
   ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

   def check_ip_blacklist(ip):
       """Verifica si una IP está en la lista negra simulada."""
       if ip in BLACKLIST:
           return {
               "status": "listed",
               "details": BLACKLIST[ip]
           }
       return {
           "status": "not_listed",
           "details": "La IP no está en la lista negra."
       }

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

   @app.route('/check-ip', methods=['GET'])
   def check_ip():
       ip = request.args.get('ip')
       if not ip:
           return jsonify({"error": "Proporciona una dirección IP"}), 400
       
       # Validación básica de formato de IP (simplificada)
       if not all(c.isdigit() or c == '.' or c == ':' for c in ip):  # Soporta IPv4 e IPv6
           return jsonify({"error": "Formato de IP inválido"}), 400
       
       result = check_ip_blacklist(ip)
       return jsonify(result)

   @app.route('/check-abuseipdb', methods=['GET'])
   def check_abuseipdb_endpoint():
       ip = request.args.get('ip')
       if not ip:
           return jsonify({"error": "Proporciona una dirección IP"}), 400
       
       # Validación básica de formato de IP (simplificada)
       if not all(c.isdigit() or c == '.' or c == ':' for c in ip):
           return jsonify({"error": "Formato de IP inválido"}), 400
       
       result = check_abuseipdb(ip)
       return jsonify(result)

   @app.route('/info', methods=['GET'])
   def info():
       return jsonify({
           'nombre': 'Checkear IP - Tratamiento de Datos Personales Paralelo A',
           'version': '1.0.0',
           'descripcion': 'API para verificar si una dirección IP está listada en bases de datos de listas negras (blacklists)',
           'autor': 'Fabricio Toasa, Maria Ordoñez, Anghelo Loayza',
       })

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)