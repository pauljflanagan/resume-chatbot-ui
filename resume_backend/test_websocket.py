#!/usr/bin/env python3

import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8090"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Send a test message
            test_message = {"message": "What are your technical skills?"}
            await websocket.send(json.dumps(test_message))
            print(f"Sent: {test_message}")
            
            # Listen for responses
            async for message in websocket:
                print(f"Received: {message}")
                if "[END]" in message:
                    print("End of response received")
                    break
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_client())
