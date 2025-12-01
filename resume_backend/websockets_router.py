#!/usr/bin/env python

import asyncio
import websockets
import os
import json
import requests
from pypdf import PdfReader

# OpenRouter API configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def read_json_format(json_path):
    """Read the JSON format template"""
    with open(json_path, "r") as file:
        return json.load(file)


# Load the resume data once when the server starts
try:
    json_format = read_json_format("resume.json")
    SYSTEM_MESSAGE = f"""You are Paul Flanagan, a fullstack software engineer, whose professional experience and skills center around fullstack software development, cloud computing, and AI integration.
            
All professional information can be found here:
{json_format}

Respond to all user questions using only the information provided in this JSON structure. Do not fabricate or assume any details beyond what is explicitly stated in the JSON. If you are asked any questions
that are not related to software engineering, fullstack development, cloud computing, or AI integration, politely inform the user that you can only provide information related to your professional expertise as outlined in the JSON. The
only exception is if the question that the user asks queries specific information that is found within the professional information JSON.

Responses should be concise, conversational, and professional. Although you have access to detailed information, avoid overwhelming the user with excessive detail unless specifically requested.
"""
except Exception as e:
    print(f"Error loading resume data: {e}")
    SYSTEM_MESSAGE = "I'm Paul Flanagan, a fullstack software engineer. I'm currently unavailable due to a configuration issue."

# Store conversation history for each client
client_conversations = {}


async def get_ai_response(user_message, conversation_history):
    """Get response from OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Build the messages array with system message and conversation history
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    data = {"model": "openai/gpt-4", "messages": messages, "max_tokens": 1500}

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            error_msg = f"API Error {response.status_code}: {response.text}"
            print(error_msg)
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. ({response.status_code})"
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."


async def handle_chat_message(websocket, message, client_id):
    """Handle incoming chat messages"""
    try:
        # Parse the message (assuming JSON format)
        try:
            message_data = json.loads(message)
            user_message = message_data.get("message", message)
        except json.JSONDecodeError:
            # If not JSON, treat as plain text
            user_message = message

        # Initialize conversation history for new clients
        if client_id not in client_conversations:
            client_conversations[client_id] = []

        # Get AI response
        ai_response = await get_ai_response(
            user_message, client_conversations[client_id]
        )

        # Update conversation history (keep last 10 exchanges to manage token limits)
        client_conversations[client_id].append(
            {"role": "user", "content": user_message}
        )
        client_conversations[client_id].append(
            {"role": "assistant", "content": ai_response}
        )

        # Keep only the last 10 messages to prevent token overflow
        if len(client_conversations[client_id]) > 20:
            client_conversations[client_id] = client_conversations[client_id][-20:]

        # Send response back to client
        response_data = {
            "type": "chat_response",
            "message": ai_response,
            "timestamp": asyncio.get_event_loop().time(),
        }

        await websocket.send(json.dumps(response_data))
        await websocket.send("[END]")

    except Exception as e:
        error_msg = f"Error processing message: {e}"
        print(error_msg)
        await websocket.send(
            json.dumps(
                {
                    "type": "error",
                    "message": "Sorry, I encountered an error processing your message.",
                }
            )
        )
        await websocket.send("[END]")


async def echo(
    websocket,
):  # Removed 'path' parameter as it's no longer needed in newer websockets versions
    client_id = id(websocket)  # Use websocket object ID as client identifier
    print(f"Client {client_id} connected", flush=True)

    try:
        async for message in websocket:
            print(f"Received message from client {client_id}: {message}", flush=True)

            # Handle the chat message using OpenRouter
            await handle_chat_message(websocket, message, client_id)

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} disconnected", flush=True)
        # Clean up conversation history for disconnected client
        if client_id in client_conversations:
            del client_conversations[client_id]
    except Exception as e:
        print(f"Error with client {client_id}: {e}", flush=True)


async def main():
    print("WebSocket server starting", flush=True)
    print(f"System message loaded: {len(SYSTEM_MESSAGE)} characters", flush=True)

    # Create the server with CORS headers
    async with websockets.serve(
        echo, "0.0.0.0", int(os.environ.get("PORT", 8090))
    ) as server:
        print("WebSocket server running on port 8090", flush=True)
        print("Resume chatbot is ready to receive connections", flush=True)
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
