import httpx
import base64
import io

dummy_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")

try:
    response = httpx.post(
        "http://localhost:8000/api/v1/sculpture/analyze",
        files={"file": ("nataraja_sculpture.png", dummy_png, "image/png")}
    )
    print("Status:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
