import asyncio
import websockets
import socket
import json  # ========== json import 주석 해제 ==========

UDP_PORT = 5005
WS_PORT = 6789

# UDP 소켓 설정
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('', UDP_PORT))
udp_sock.setblocking(False)

# ========== room별로 클라이언트 관리 ==========
rooms = {
    "game1": set(),
    "game2": set()
}


# ========== room별 관리 끝 ==========

async def udp_listener():
    while True:
        try:
            data, _ = udp_sock.recvfrom(1024)
            message = data.decode('utf-8')

            # ========== JSON 파싱해서 room 확인 ==========
            try:
                udp_data = json.loads(message)
                room = udp_data.get("room", "game1")  # 기본값 game1

                # 해당 room의 클라이언트들에게만 전송
                if room in rooms:
                    for ws in rooms[room]:
                        await ws.send(message)
                    print(f"[{room}] 메시지 전송: {len(rooms[room])}명")
            except json.JSONDecodeError:
                # JSON이 아닌 경우 모든 클라이언트에게 전송 (하위 호환)
                for room_clients in rooms.values():
                    for ws in room_clients:
                        await ws.send(message)
            # ========== room별 전송 끝 ==========

        except BlockingIOError:
            await asyncio.sleep(0.1)


async def ws_handler(websocket, path):
    # ========== 클라이언트가 처음 연결되면 room 정보 받음 ==========
    try:
        init_message = await websocket.recv()
        init_data = json.loads(init_message)
        room = init_data.get("room", "game1")

        # 해당 room에 클라이언트 추가
        if room not in rooms:
            rooms[room] = set()
        rooms[room].add(websocket)

        print(f"클라이언트 입장 [{room}]: 총 {len(rooms[room])}명")

        try:
            async for _ in websocket:
                pass  # 클라이언트 메시지는 무시
        finally:
            rooms[room].remove(websocket)
            print(f"클라이언트 퇴장 [{room}]: 총 {len(rooms[room])}명")
    except Exception as e:
        print(f"에러: {e}")
    # ========== room 처리 끝 ==========


async def main():
    ws_server = websockets.serve(ws_handler, "0.0.0.0", WS_PORT)
    await asyncio.gather(ws_server, udp_listener())


print("WebSocket 중계 서버 시작...")
asyncio.run(main())
