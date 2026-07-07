import json
from typing import Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketException
from fastapi import status as http_status
from loguru import logger

from agentchat.services.autobuild.manager import AutoBuildManager
from agentchat.api.services.user import UserPayload
from agentchat.utils.JWT import decode_token

router = APIRouter()


@router.websocket('/build/auto')
async def chat(websocket: WebSocket,
               chat_id: Optional[str] = None):
    try:
        await websocket.accept()

        auth_token = None
        query_params = websocket.query_params
        if 'token' in query_params:
            auth_token = query_params['token']
        else:
            headers = websocket.headers
            auth_header = headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                auth_token = auth_header[7:]

        if not auth_token:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token")

        payload = decode_token(auth_token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

        payload_data = json.loads(payload["sub"])
        login_user = UserPayload(**payload_data)

        chat_manager = AutoBuildManager()
        await chat_manager.control_auto_client(login_user=login_user, websocket=websocket, chat_id=chat_id or "")

    except WebSocketException as exc:
        logger.exception(f'Websocket exception: {str(exc)}')
        await websocket.close(code=http_status.WS_1011_INTERNAL_ERROR, reason=str(exc))
    except HTTPException as exc:
        logger.exception(f'Authentication error: {str(exc)}')
        await websocket.close(code=http_status.WS_1008_POLICY_VIOLATION, reason=exc.detail)
    except Exception as exc:
        logger.exception(f'Error in chat websocket: {str(exc)}')
        message = exc.detail if isinstance(exc, HTTPException) else str(exc)
        await websocket.close(code=http_status.WS_1011_INTERNAL_ERROR, reason=message)
