import socket
import json
from flask import jsonify
import requests
from pyexpat.errors import messages


class CheckVm:
    def __init__(self, data):
        self.port = 8888
        self.ip = data.get('ip')
        self.exp_name = data.get('name')
        self.response = None
        self.json_response = None

    def get_data(self):
        try:
            with socket.create_connection((self.ip, self.port), timeout=5) as sock:
                self.response = sock.recv(1024).decode('utf-8').strip()
        except Exception as e:
            return jsonify({"status": "error", "message": str(e), "ip": self.ip}), 500

    def get_ip_name(self):
        try:
            url = f"http://{self.ip}:{self.port}"
            self.response = requests.get(url, timeout=3)
            self.response.raise_for_status()
            self.json_response = self.response.json()
        except Exception as e:
            return jsonify({"status": "error", "message": str(e), "ip": self.ip}), 500


    def mod_response(self):
        if not self.response:
            return jsonify({"status": "error", "message": "No response from server", "ip": self.ip}), 500
        try:
            self.json_response = json.loads(self.response)
        except json.JSONDecodeError:
            return jsonify(
                {"status": "error", "message": "Invalid JSON format from server", "response": self.response,
                 "ip": self.ip}), 500

    def compare_name(self):
        if not self.json_response:
            return jsonify({"status": "error", "message": "No JSON response to compare", "ip": self.ip}), 500
        if self.json_response.get('name') == self.exp_name:
            return jsonify(
                {"status": "success", "message": "Name matches", "response": self.json_response, "ip": self.ip}), 200
        else:
            return jsonify(
                {"status": "failure", "message": "Name does not match", "response": self.json_response, "ip": self.ip}), 200

    def run(self):
        result = self.get_ip_name()
        if result:
            return result  # Прекращаем выполнение, если есть ошибка
        # result = self.mod_response()
        # if result:
        #     return result  # Прекращаем выполнение, если есть ошибка
        return self.compare_name()  # Возвращаем результат сравнения