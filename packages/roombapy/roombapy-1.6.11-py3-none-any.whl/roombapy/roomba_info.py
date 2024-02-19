from functools import cached_property
from typing import Dict, Optional

from pydantic import BaseModel, Field, computed_field, field_validator


class RoombaInfo(BaseModel):
    hostname: str
    firmware: str = Field(alias="sw")
    ip: str
    mac: str
    robot_name: str = Field(alias="robotname")
    sku: str
    capabilities: Dict[str, int] = Field(alias="cap")
    password: Optional[str] = None

    @field_validator("hostname")
    @classmethod
    def hostname_validator(cls, value: str) -> str:
        if "-" not in value:
            raise ValueError(f"hostname does not contain a dash: {value}")
        model_name, blid = value.split("-")
        if blid == "":
            raise ValueError(f"empty blid: {value}")
        if model_name.lower() not in {"roomba", "irobot"}:
            raise ValueError(f"unsupported model in hostname: {value}")
        return value

    @computed_field
    @cached_property
    def blid(self) -> str:
        return self.hostname.split("-")[1]

    def __hash__(self) -> int:
        return hash(self.mac)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, RoombaInfo) and self.mac == o.mac
