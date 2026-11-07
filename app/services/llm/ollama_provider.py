import httpx

from app.core.config import settings
from app.services.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.model = model or settings.ollama_model

    def generate_remediation(self, context: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": context, "stream": False},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload.get("response", "")
        if not text:
            raise RuntimeError("Ollama returned empty output")
        return text.strip()
