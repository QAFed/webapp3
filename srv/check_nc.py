import socket
import json
from flask import jsonify

class CheckVm:
    def __init__(self, data):
        self.port = 8888
        self.ip = data.get('ip')
        self.exp_name = data.get('exp_name')
        self.response = None
        self.json_response = None

    def get_data(self):
        try:
            with socket.create_connection((self.ip, self.port), timeout=5) as sock:
                self.response = sock.recv(1024).decode('utf-8').strip()
        except Exception as e:
            return jsonify({"status": "error", "message": str(e), "ip": self.ip}), 500

    def mod_response(self):
        try:
            self.json_response = json.loads(self.response)
        except json.JSONDecodeError:
            return jsonify(
                {"status": "error", "message": "Invalid JSON format from server", "response": self.response,
                 "ip": self.ip}), 500


    def compare_name(self):
        if self.json_response.get('name') == self.exp_name:
            return jsonify(
                {"status": "success", "message": "Name matches", "response": self.json_response, "ip": self.ip}), 200
        else:
            return jsonify(
                {"status": "failure","message": "Name does not match", "response": self.json_response, "ip": self.ip}), 200


    def run(self):
        self.get_data()
        self.mod_response()
        self.compare_name()