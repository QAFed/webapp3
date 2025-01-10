#!/bin/bash

UNIQUE_ID="TST100"
SERVER_URL="http://192.168.55.105:5000/update"
IP_FILE="/tmp/current_ip.txt"
LISTEN_PORT=8888

get_current_ip() {
  hostname -I | awk '{print $1}'
}

send_ip_to_server() {
  local current_ip="$1"
  echo "Sending IP: $current_ip to server..."  # Логирование отправляемого IP
  response=$(curl -s -o /dev/null -w "%{http_code}" --location --request POST "$SERVER_URL" \
    --header "Content-Type: application/json" \
    --data "{\"ip\": \"$current_ip\",\"name\": \"$UNIQUE_ID\"}")
  echo "Response code: $response"  # Логирование кода ответа
  if [ "$response" -eq 200 ] || [ "$response" -eq 201 ]; then
    echo "Server accepted IP (response code: $response). Writing to file."
    echo "$current_ip" > "$IP_FILE"
  else
    echo "Server rejected IP. Response code: $response"
  fi
}

start_listener() {
  while true; do
    echo -e "{\"ip\": \"$(get_current_ip)\", \"name\": \"$UNIQUE_ID\"}" | nc -l -p $LISTEN_PORT -q 1
  done
}

# Запуск сервера для ответов на запросы
start_listener &

while true; do
  current_ip=$(get_current_ip)

  if [ ! -f "$IP_FILE" ] || [ "$(cat $IP_FILE)" != "$current_ip" ]; then
    send_ip_to_server "$current_ip"
  fi
  sleep 30
done