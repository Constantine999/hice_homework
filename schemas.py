from datetime import datetime

from pydantic import BaseModel, Field


class Info(BaseModel):
    name: str = Field(title="Имя отправителя")
    text: str = Field(title="Текст сообщения")


class ResponseInfo(BaseModel):
    name: str = Field(title="Имя отправителя")
    text: str = Field(title="Текст сообщения")
    created: datetime = Field(title="Дата отправки")
    sequence_number: int = Field(title="Порядковый номер сообщения")
    messages_count: int = Field(title="Количество сообщений от текущего пользователя")
