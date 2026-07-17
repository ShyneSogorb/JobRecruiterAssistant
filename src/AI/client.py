import json
import textwrap
from typing import Any

import requests

from src.ai.exceptions import AIClientError
from src.ai.models import Message, Generation, AIResponse
from src.utils import time_conversion as tc
from src.utils.logger import Logger

class AIClient:

    def __init__(self, logger: Logger, model: str = "qwen3:30b", base_url: str = "http://localhost:11434") -> None:
        self.model = model
        self.base_url = base_url
        self.logger = logger

    def _log_separator(self, nrows:int = 1, nslashes:int = 40):
        slashes = "-".join("-" for i in range(nslashes))
        for i in range(nrows):
            self.logger.save(slashes)

    def _log_section(self, section:str, content: Any, nrows = 1):
        self._log_separator()
        self.logger.save(section)
        self._log_separator()
        self.logger.save(content)
        self._log_separator()

        

    def ask(self, prompt: str, think: bool = True, format: Any = None) -> AIResponse:

        self._log_separator(3)
        self.logger.log("NEW QUESTION")
        self._log_separator(3)

        payload = self._build_payload(prompt, think, format)
        self._log_section("Payload", payload)

        response = self._send_request(payload)

        result = self._parse_response(response)
        self._log_section("AI Response", result)

        return result

    @property
    def chat_url(self) -> str:
        return f"{self.base_url}/api/chat"

    def _build_payload(self, prompt: str, thinking: bool, format: dict[str, Any] | None) -> dict:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": thinking,
        }
        if not type(format) == None:
            payload["format"]= format

        return payload
    
    
    def _send_request(self, payload: dict) -> requests.Response:
        req = requests.post(
            self.chat_url, 
            json=payload,
            timeout=300
        )

        try:
            req.raise_for_status()
        except requests.RequestException as e:
            self.logger.log(f"Error ocurred, see more at {self.logger.root}")
            self.logger.save("Error: " + str(e))
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
    

