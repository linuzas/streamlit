import json
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime
import re
import streamlit as st
# Load environment variables


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

### -------------------------------------------
### ✅ USER FUNCTIONS
### -------------------------------------------

def get_user(username: str):
    """
    Retrieve a user record from Supabase by username.
    Args:
        username (str): The username to look up.
    Returns:
        dict: User record or None if not found.
    """
    response = supabase.table("users").select("*").eq("username", username).execute()
    if response.data:
        return response.data[0]
    return None


def save_user(username: str, password: str):
    """
    Insert a new user into the 'users' table.
    Args:
        username (str): The user's username.
        password (str): The user's hashed password.
    """
    data = {
        "username": username,
        "password": password,
        "created_at": "now()"
    }
    response = supabase.table("users").insert(data).execute()
    return response


def get_user_id(username: str):
    """
    Get the user ID based on the username.
    Args:
        username (str): The username to look up.
    Returns:
        UUID: User ID or None if not found.
    """
    response = supabase.table("users").select("id").eq("username", username).execute()
    if response.data:
        return response.data[0]["id"]
    return None


def delete_user(username: str):
    """
    Delete a user from the 'users' table.
    Args:
        username (str): The username to delete.
    """
    response = supabase.table("users").delete().eq("username", username).execute()
    return response


### -------------------------------------------
### ✅ CHAT FUNCTIONS
### -------------------------------------------

def save_chat(user_id: str, expert_type: str, messages, description: str):
    """
    Save a new chat into the 'chats' table.
    Args:
        user_id (str): The ID of the user.
        expert_type (str): Type of expert.
        messages (list): List of messages (user + assistant).
        description (str): Short description of the chat.
    Returns:
        dict: The saved chat record.
    """
    data = {
        "user_id": user_id,
        "expert_type": expert_type,
        "messages": json.dumps(messages),
        "description": description,
        "timestamp": "now()"  # Save current timestamp
    }
    response = supabase.table("chats").insert(data).execute()
    return response


def get_user_chats(user_id: str):
    """
    Retrieve all chats for a specific user.
    Args:
        user_id (str): The ID of the user.
    Returns:
        list: List of chat records.
    """
    response = supabase.table("chats").select("*").eq("user_id", user_id).order("timestamp", desc=True).execute()
    return response.data


def update_chat(chat_id: int, updates: dict):
    """
    Update an existing chat in the 'chats' table.
    Args:
        chat_id (int): The ID of the chat to update.
        updates (dict): The fields to update.
    """
    response = supabase.table("chats").update(updates).eq("id", chat_id).execute()
    return response


def delete_chat(chat_id: int):
    """
    Delete a chat by ID.
    Args:
        chat_id (int): The ID of the chat to delete.
    """
    response = supabase.table("chats").delete().eq("id", chat_id).execute()
    return response


### -------------------------------------------
### ✅ API USAGE FUNCTIONS (Optional)
### -------------------------------------------

def increment_api_calls(user_id: str, max_calls=10):
    """
    Increment API call count for the user.
    Resets count if it's a new day.
    Args:
        user_id (str): The ID of the user.
        max_calls (int): Max allowed calls per day.
    Returns:
        bool: True if call is allowed, False if limit exceeded.
    """
    today = datetime.utcnow().date()

    # Get current call count and last call date from Supabase
    user = supabase.table("users").select("call_count", "last_call_date").eq("id", user_id).execute()
    if user.data:
        current_count = user.data[0].get("call_count", 0)
        last_call_date = user.data[0].get("last_call_date")

        # Reset call count if it's a new day
        if last_call_date != str(today):
            current_count = 0

        # Check if the limit is reached
        if current_count >= max_calls:
            return False

        # Increment the call count and update last_call_date
        new_count = current_count + 1
        supabase.table("users").update({
            "call_count": new_count,
            "last_call_date": today.isoformat()
        }).eq("id", user_id).execute()

        return True

    return False

def validate_password(password: str) -> bool:
    """
    Validate password:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character (@, #, $, %, &, *, !, etc.)
    """
    if len(password) < 8:
        return False
    
    if not re.search(r'[A-Z]', password):  # At least one uppercase letter
        return False
    
    if not re.search(r'[a-z]', password):  # At least one lowercase letter
        return False
    
    if not re.search(r'[0-9]', password):  # At least one number
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # At least one special character
        return False
    
    return True
