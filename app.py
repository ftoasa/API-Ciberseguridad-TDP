from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos simulada de IPs en lista negra
BLACKLIST = {
    "192.168.1.100": {"reason": "Malware distribution", "severity": "High"},
    "10.0.0.50": {"reason": "Brute force attacks", "severity": "Medium"},
    "172.16.254.1": {"reason": "Phishing", "severity": "Low"}
}

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

@app.route('/check-ip', methods=['GET'])
def check_ip():
    ip = request.args.get('ip')
    if not ip:
        return jsonify({"error": "Proporciona una dirección IP"}), 400
    
    # Validación básica de formato de IP (simplificada)
    if not all(c.isdigit() or c == '.' for c in ip):
        return jsonify({"error": "Formato de IP inválido"}), 400
    
    result = check_ip_blacklist(ip)
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