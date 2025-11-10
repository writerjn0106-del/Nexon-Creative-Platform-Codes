import socket
import time
import random
import json
import threading

# 브로드캐스트 주소와 포트 설정
BROADCAST_IP = '255.255.255.255'
PORT = 5005

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("UDP Broadcast 서버 시작...")

black_stone_game1 = [(4, 4),(2, 6),(6, 2),(5, 5),(3, 3),(7, 4),(2, 2),(4, 6),(5, 3),(3, 5)]
white_stone_game1 = [(6, 6),(3, 6),(5, 2),(4, 5),(6, 4),(2, 4),(7, 3),(5, 6), (4, 3),(6, 5)]
black_stone_game2 = [(4,4), (5,3), (3,5), (6,4), (4,6), (2,5), (5,5), (3,4), (6,5), (4,2)]
white_stone_game2 = [(5,4), (4,5), (3,6), (6,3), (2,4), (5,6), (3,3), (6,6), (2,6), (5,2)]


def run_game(room_id, black_stones, white_stones):
    while True:
        x_wait = random.randint(5, 15)

        for (b_x, b_y), (w_x, w_y) in zip(black_stones, white_stones):
            # 흑돌 전송
            data_black = json.dumps({'room': room_id, 'b_x': b_x, 'b_y': b_y})
            sock.sendto(data_black.encode('utf-8'), (BROADCAST_IP, PORT))
            print(f"[{room_id}] ⚫ 전송됨: ({b_x}, {b_y})")
            time.sleep(x_wait)

            # 백돌 전송
            data_white = json.dumps({'room': room_id, 'w_x': w_x, 'w_y': w_y})
            sock.sendto(data_white.encode('utf-8'), (BROADCAST_IP, PORT))
            print(f"[{room_id}] ⚪ 전송됨: ({w_x}, {w_y})")
            time.sleep(x_wait)

        # 초기화
        reset_data = json.dumps({'room': room_id, 'reset': True})
        sock.sendto(reset_data.encode('utf-8'), (BROADCAST_IP, PORT))
        print(f"[{room_id}] 🔄 초기화 신호 전송됨")
        time.sleep(3)

thread1 = threading.Thread(target=run_game, args=('game1', black_stone_game1, white_stone_game1))
thread2 = threading.Thread(target=run_game, args=('game2', black_stone_game2, white_stone_game2))

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()

# 메인 스레드는 계속 실행
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n서버 종료")
