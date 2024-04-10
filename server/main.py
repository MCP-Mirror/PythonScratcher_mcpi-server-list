import struct
import random
from flask import Flask, request, jsonify, render_template
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'), 418

@app.route('/ping', methods=['GET'])
def ping_server():
    server_address = request.args.get('server_address')
    if not server_address:
        return jsonify({"error": "Server address is required."}), 400

    if ":" in server_address:
        target_server = (server_address.split(":")[0], int(server_address.split(":")[1]))
    else:
        target_server = (server_address, 19132)

    magic_crap = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx'
    ping_packet = b'\x02' + struct.pack(">q", random.randint(5, 20)) + magic_crap

    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.settimeout(10)  # Set timeout to 5 seconds
    try:
        udp_socket.sendto(ping_packet, target_server)
        data = udp_socket.recvfrom(2048)[0]
        len_val = ord(data[34:34 + 1])
        server_name = data[35:35 + len_val].decode('utf-8').split(';')[2]
        return jsonify({"server_name": server_name}), 200
    except socket.timeout:

