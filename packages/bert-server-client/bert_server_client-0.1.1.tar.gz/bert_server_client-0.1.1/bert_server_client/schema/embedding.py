from typing import Union, List, Optional, Dict, Any
from dataclasses import dataclass, field
from uuid import UUID

from bert_server_client.schema.base import Base


@dataclass
class EmbeddingData:
    object: str
    index: int
    embedding: List[float]


@dataclass
class EmbeddingUsage:
    prompt_tokens: int
    total_tokens: int


@dataclass
class Embedding(Base):
    object: str
    data: List[EmbeddingData]
    model: Optional[str] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)


@dataclass
class EmbeddingRequest(Base):
    input: Union[str, List[str]]
    model: str
    encoding_format: Optional[str] = field(default="float")
    dimensions: Optional[int] = field(default=None)
    user: Optional[UUID] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }
