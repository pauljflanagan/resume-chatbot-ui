import os
import json
import requests
import asyncio
from websockets.server import serve
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Get configuration from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
PORT = int(os.getenv("PORT", 8765))

# Validate API key
if not API_KEY:
    print("ERROR: OPENROUTER_API_KEY environment variable is not set!")
    print("Please set your OpenRouter API key in the .env file")
    exit(1)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-Title": "Resume Chatbot"  # Optional: for analytics
}

def read_json_format(json_path):
    """Read the JSON format template"""
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: {json_path} not found, using empty template")
        return {}

# Load the resume data once when the server starts
try:
    resume_data = read_json_format("resume.json")
    print("Resume data loaded successfully")
except Exception as e:
    print(f"Error loading resume data: {e}")
    resume_data = {}

# Store conversation history for each client
client_conversations = {}

async def get_ai_response(user_message, conversation_history):
    """Get AI response from OpenRouter API"""
    try:
        # Build the messages array with system message and conversation history
        messages = [
            {
                "role": "system",
                "content": f"""You are Paul Flanagan, a fullstack software engineer whose professional experience and skills center around fullstack software development, cloud computing, and AI integration.

All professional information can be found here:
{json.dumps(resume_data, indent=2)}

Respond to all user questions using only the information provided in this JSON structure, analyzing the data and providing the best answer in a conversational format in full, complete sentences. 
Do not fabricate or assume any details beyond what is explicitly stated in the JSON. If you are asked any questions that are not related to software engineering, fullstack development, cloud computing, or AI integration, politely inform the user that you can only provide information related to your professional expertise as outlined in the JSON.

Responses should be concise, conversational, and professional. Although you have access to detailed information, avoid overwhelming the user with excessive detail unless specifically requested."""
            }
        ]
        
        # Add conversation history (limit to last 10 messages to manage token count)
        messages.extend(conversation_history[-10:])
        
        # Add the new user message
        messages.append({"role": "user", "content": user_message})
        
        data = {
            "model": "openai/gpt-4",
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        print(f"Sending request to OpenRouter with model: {data['model']}")
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            return ai_response
        else:
            error_detail = ""
            try:
                error_json = response.json()
                error_detail = error_json.get("error", {}).get("message", response.text)
            except:
                error_detail = response.text
            
            print(f"OpenRouter API error: {response.status_code}")
            print(f"Error details: {error_detail}")
            print(f"Headers sent: {headers}")
            print(f"API Key present: {'Yes' if API_KEY else 'No'}")
            print(f"API Key format: {API_KEY[:20]}..." if API_KEY and len(API_KEY) > 20 else f"API Key: {API_KEY}")
            
            return f"I'm sorry, I'm having trouble accessing my information right now. API Error: {response.status_code}. Please check the server logs."
            
    except requests.exceptions.Timeout:
        return "I'm sorry, my response is taking longer than expected. Please try asking again."
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return "I apologize, but I encountered an error while processing your request. Please try again."

async def handle_chat_message(websocket, message, client_id):
    """Handle incoming chat messages"""
    try:
        data = json.loads(message)
        user_message = data.get("message", "").strip()
        
        if not user_message:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Empty message received"
            }))
            return
        
        # Initialize conversation history for new clients
        if client_id not in client_conversations:
            client_conversations[client_id] = []
        
        # Add user message to conversation history
        client_conversations[client_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Get AI response
        ai_response = await get_ai_response(user_message, client_conversations[client_id])
        
        # Add AI response to conversation history
        client_conversations[client_id].append({
            "role": "assistant",
            "content": ai_response
        })
        
        # Send response back to client
        response_data = {
            "type": "chat_response",
            "message": ai_response,
            "role": "assistant"
        }
        
        await websocket.send(json.dumps(response_data))
        await websocket.send("[END]")
        
    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            "type": "error",
            "message": "Invalid JSON format"
        }))
    except Exception as e:
        print(f"Error handling chat message: {e}")
        await websocket.send(json.dumps({
            "type": "error",
            "message": "An error occurred while processing your message"
        }))

async def echo(websocket, path):
    """WebSocket connection handler"""
    client_id = id(websocket)
    print(f"Client {client_id} connected")
    
    try:
        # Send welcome message
        welcome_message = {
            "type": "chat_response",
            "message": "Hello! I'm Paul Flanagan, a full stack software engineer. Feel free to ask me about my experience, skills, or any projects I've worked on. How can I help you today?",
            "role": "assistant"
        }
        await websocket.send(json.dumps(welcome_message))
        await websocket.send("[END]")
        
        async for message in websocket:
            await handle_chat_message(websocket, message, client_id)
            
    except (ConnectionClosedError, ConnectionClosedOK):
        print(f"Client {client_id} disconnected normally")
    except Exception as e:
        print(f"Error with client {client_id}: {e}")
    finally:
        # Clean up conversation history
        if client_id in client_conversations:
            del client_conversations[client_id]
        print(f"Cleaned up client {client_id}")

async def main():
    """Start the WebSocket server"""
    print(f"Starting WebSocket server on port {PORT}...")
    print(f"Resume data loaded: {'Yes' if resume_data else 'No'}")
    
    async with serve(echo, "0.0.0.0", PORT):
        print(f"WebSocket server running on ws://0.0.0.0:{PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
