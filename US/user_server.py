from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    # Extract query parameters
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    
    # Directly use 'host.docker.internal' for Docker-to-host communication
    as_ip = "host.docker.internal"
    as_port = 53533  # Assuming the AS always listens on this port

    if not all([hostname, fs_port, number]):
        return jsonify({"error": "Missing parameters"}), 400

    # Query the AS for FS's IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message = f"TYPE=A\nNAME={hostname}"
        s.sendto(message.encode(), (as_ip, as_port))
        fs_ip, _ = s.recvfrom(1024)

    if fs_ip.decode() == "Not found":
        return jsonify({"error": "Fibonacci Server not found"}), 404

    # Request the Fibonacci number from FS
    response = requests.get(f"http://{fs_ip.decode()}:{fs_port}/fibonacci?number={number}")

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Error from Fibonacci Server"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Ensure the host is set to '0.0.0.0' to be reachable from outside the Docker container
