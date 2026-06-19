import base64
import io
from fastapi.testclient import TestClient
from dotenv import load_dotenv
load_dotenv("../.env")
from app.main import app

client = TestClient(app)

dummy_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")

try:
    response = client.post(
        "/api/v1/sculpture/analyze",
        files={"file": ("nataraja_sculpture.png", dummy_png, "image/png")}
    )
    print("Status code:", response.status_code)
    print("Response body:", response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
