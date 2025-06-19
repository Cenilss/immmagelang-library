import os
from dotenv import load_dotenv

load_dotenv()

def check_login(username, password):
    return (
        username == os.getenv("ADMIN_USER") and
        password == os.getenv("ADMIN_PASS")
    )