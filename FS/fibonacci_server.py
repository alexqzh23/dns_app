from flask import Flask, request, jsonify
import socket
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    if not data or 'ip' not in data:
        return jsonify({"error": "Invalid data format"}), 400

    fs_ip = data['ip']
    
    # Statically set AS details for Docker-to-host communication
    as_ip = "host.docker.internal"
    as_port = 53533

    # Prepare the registration message
    message = f"TYPE=A\nNAME=fibonacci.com\nVALUE={fs_ip}\nTTL=10"

    # Send registration information to the AS using UDP and wait for acknowledgment
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode(), (as_ip, as_port))
        s.settimeout(5)  # Set a timeout for waiting for a response

        try:
            ack, _ = s.recvfrom(1024)  # Receive acknowledgment from AS
            ack_message = ack.decode()
            if ack_message == "Registration successful":
                logger.info("Registration acknowledged by AS")
                return jsonify({"message": "Registration acknowledged by AS"}), 201
            else:
                logger.error("Registration not acknowledged by AS")
                return jsonify({"error": "Registration not acknowledged by AS"}), 500
        except socket.timeout:
            logger.error("AS response timed out")
            return jsonify({"error": "AS response timed out"}), 500

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        number = int(request.args.get('number'))
        fib_number = fibonacci(number)
        return jsonify({"fibonacci": fib_number}), 200
    except (ValueError, TypeError):
        logger.error("Invalid number provided")
        return jsonify({"error": "Invalid number"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)  # Ensure the host is set to '0.0.0.0' to be reachable from outside the Docker container
