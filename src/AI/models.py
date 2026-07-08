from pydantic import BaseModel

class Message(BaseModel):
    role:       str
    content:    str
    thinking:   str | None = None

class Generation(BaseModel):
    model:  str
    done:   bool
    done_reason: str | None = None
    total_duration_ms: int | float
    load_duration_ms: int | float
    prompt_eval_tokens: int
    prompt_eval_duration: int | float
    eval_tokens: int
    eval_duration: int | float

class AIResponse(BaseModel):
    message: Message
    generation : Generation