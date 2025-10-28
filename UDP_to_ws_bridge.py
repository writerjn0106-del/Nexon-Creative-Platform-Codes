import asyncio
import websockets
import socket
#import json

UDP_PORT = 5005
WS_PORT = 6789

# UDP 소켓 설정
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('', UDP_PORT))
udp_sock.setblocking(False)

connected_clients = set()

async def udp_listener():
    while True:
        try:
            data, _ = udp_sock.recvfrom(1024)
            message = data.decode('utf-8')
            # 연결된 모든 WebSocket 클라이언트에게 전송
            for ws in connected_clients:
                await ws.send(message)
        except BlockingIOError:
            await asyncio.sleep(0.1)

async def ws_handler(websocket,path):
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            pass  # 클라이언트 메시지는 무시
    finally:
        connected_clients.remove(websocket)

async def main():
    ws_server = websockets.serve(ws_handler, "0.0.0.0", WS_PORT)
    await asyncio.gather(ws_server, udp_listener())

print("WebSocket 중계 서버 시작...")
asyncio.run(main())