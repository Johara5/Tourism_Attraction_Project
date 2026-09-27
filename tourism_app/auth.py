"""User authentication and profile management."""
import hashlib
import json
import os

from config import USERS_FILE

# Demo account for quick access (password: admin123)
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin123"


def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _find_username_key(users: dict, username: str) -> str | None:
    """Find stored username key (case-insensitive, trimmed)."""
    cleaned = username.strip()
    if not cleaned:
        return None
    if cleaned in users:
        return cleaned
    lower = cleaned.lower()
    for key in users:
        if key.lower() == lower:
            return key
    return None


def ensure_demo_user() -> None:
    """Create demo admin account if missing."""
    users = load_users()
    if DEMO_USERNAME not in users:
        users[DEMO_USERNAME] = {
            "password": hash_password(DEMO_PASSWORD),
            "email": "demo@tourism.local",
            "full_name": "Demo User",
        }
        save_users(users)


def register_user(username: str, password: str, email: str = "", full_name: str = "") -> tuple[bool, str]:
    username = username.strip()
    if not username:
        return False, "Username cannot be empty."
    if _find_username_key(load_users(), username):
        return False, "Username already exists (try logging in instead)."
    users = load_users()
    users[username] = {
        "password": hash_password(password),
        "email": email.strip(),
        "full_name": full_name.strip(),
    }
    save_users(users)
    return True, f"Account created! Log in with username: **{username}**"


def verify_login(username: str, password: str) -> tuple[bool, str, str]:
    """
    Returns (success, canonical_username, error_message).
    """
    ensure_demo_user()
    users = load_users()
    key = _find_username_key(users, username)
    if key is None:
        names = ", ".join(f"`{u}`" for u in list(users.keys())[:5])
        hint = f" Registered usernames: {names}" if users else ""
        return False, "", f"Username not found.{hint}"
    if users[key]["password"] != hash_password(password):
        return False, "", "Incorrect password. Please try again."
    return True, key, ""


def update_user_profile(
    username: str,
    email: str | None = None,
    full_name: str | None = None,
    new_password: str | None = None,
) -> bool:
    users = load_users()
    key = _find_username_key(users, username)
    if key is None:
        return False
    if email is not None:
        users[key]["email"] = email
    if full_name is not None:
        users[key]["full_name"] = full_name
    if new_password is not None:
        users[key]["password"] = hash_password(new_password)
    save_users(users)
    return True
