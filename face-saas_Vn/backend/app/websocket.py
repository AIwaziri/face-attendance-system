from fastapi import APIRouter, WebSocket

router = APIRouter()

clients = []


@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for c in clients:
                await c.send_text(data)

    except:
        clients.remove(websocket)