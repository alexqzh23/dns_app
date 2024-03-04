import socket

# Assuming you're using a simple in-memory dictionary for storing mappings
dns_records = {}

def handle_registration(data):
    lines = data.split('\n')
    record = {}
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:  # Ensure the line can be split into exactly 2 parts
            record[parts[0]] = parts[1]
    # Update the DNS records only if both NAME and VALUE are present
    if "NAME" in record and "VALUE" in record:
        dns_records[record['NAME']] = record['VALUE']
        return "Registration successful"
    else:
        return "Registration failed due to missing NAME or VALUE"

def handle_dns_query(data):
    lines = data.split('\n')
    query = {}
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:
            query[parts[0]] = parts[1]
    # Perform the DNS query only if NAME is present in the query
    if "NAME" in query:
        hostname = query['NAME']
        return dns_records.get(hostname, "Not found")
    else:
        return "Query failed due to missing NAME"

def start_udp_server(host='0.0.0.0', port=53533):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Authoritative Server listening on {host}:{port}")
        while True:
            data, addr = s.recvfrom(1024)
            data_decoded = data.decode()
            print(f"Received message from {addr}")

            # Determine if the message is for registration or DNS query
            if "VALUE" in data_decoded:
                response = handle_registration(data_decoded)
            else:
                response = handle_dns_query(data_decoded)
            
            # Send the response
            s.sendto(response.encode(), addr)
            print(f"Sent response to {addr}: {response}")

if __name__ == '__main__':
    start_udp_server()


