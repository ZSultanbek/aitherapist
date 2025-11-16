import hvac
import os

VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "root")  # Never hardcode in production!

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

def get_ai_therapist_secrets():
    secret = client.secrets.kv.v2.read_secret_version(path="ai-therapist")
    data = secret['data']['data']
    return data  # returns dict: {'gemini_api_key': '...', 'gemini_api_secret': '...'}
