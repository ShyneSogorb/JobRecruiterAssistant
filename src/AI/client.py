import requests

from src.ai.exceptions import AIClientError
from src.ai.models import Message, Generation, AIResponse
from src.utils import time_conversion as tc

class AIClient:

    def __init__(self, model: str = "qwen3:14b", base_url: str = "http://localhost:11434") -> None:
        self.model = model
        self.base_url = base_url

    def ask(self, prompt: str) -> AIResponse:
        payload = self._build_payload(prompt)

        response = self._send_request(payload)

        return self._parse_response(response)

    @property
    def chat_url(self) -> str:
        return f"{self.base_url}/api/chat"

    def _build_payload(self, prompt: str) -> dict:
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    
    
    def _send_request(self, payload: dict) -> requests.Response:
        req = requests.post(
            self.chat_url, 
            json=payload,
            timeout=60
        )

        try:
            req.raise_for_status()
        except requests.RequestException as e:
            raise AIClientError(...) from e
        
        return req
    
    def _parse_response(self, response: requests.Response) -> AIResponse:
        data = response.json()
        msg = data["message"]
        message = Message(
            role=msg.get("role"), content=msg.get("content"), thinking=msg.get("thinking")
        )
        generation = Generation(
            model=data.get("model"),
            done=data.get("done"),
            done_reason=data.get("done_reason"),
            total_duration_ms=tc.time_conversion(data.get("total_duration"), tc.ETimeFormat.Nanosec, tc.ETimeFormat.Milisec),
            load_duration_ms=tc.time_conversion(data.get("load_duration"), tc.ETimeFormat.Nanosec, tc.ETimeFormat.Milisec),
            prompt_eval_tokens=data.get("prompt_eval_count"),
            prompt_eval_duration=tc.time_conversion(data.get("prompt_eval_duration"), tc.ETimeFormat.Nanosec, tc.ETimeFormat.Milisec),
            eval_tokens=data.get("eval_count"),
            eval_duration=tc.time_conversion(data.get("eval_duration"), tc.ETimeFormat.Nanosec, tc.ETimeFormat.Milisec),
        )
        res = AIResponse(message=message, generation=generation)
        return res
    

