import socket
import time
import random
import json

# 브로드캐스트 주소와 포트 설정
BROADCAST_IP = '255.255.255.255'
PORT = 5005

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("UDP Broadcast 서버 시작...")

while True:
    # x, y 값을 랜덤으로 생성
    x = random.randint(0, 19)
    y = random.randint(0, 19)

    # JSON 형식으로 데이터 구성
    data = json.dumps({'x': x, 'y': y})

    # 브로드캐스트 전송
    sock.sendto(data.encode('utf-8'), (BROADCAST_IP, PORT))
    print(f"전송됨: x={x}, y={y}")

    # 5초 대기
    time.sleep(5)