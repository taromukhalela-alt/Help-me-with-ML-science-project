from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:  # Keep the application importable before optional installs.
    BaseModel = None
    Field = None
    class ValidationError(ValueError):
        """Compatibility error used when pydantic is not installed."""


if BaseModel:
    class DocumentCreate(BaseModel):
        title: str = Field(min_length=1, max_length=200)
        content: str = Field(min_length=1, max_length=200000)
        theme: str = "default"
        metadata: Dict[str, Any] = Field(default_factory=dict)

    class DocumentIR(BaseModel):
        title: str
        blocks: List[Dict[str, Any]]
        theme: str = "default"
        metadata: Dict[str, Any] = Field(default_factory=dict)

    class DocumentStatus(BaseModel):
        status: str
        error: Optional[str] = None
else:
    @dataclass
    class DocumentCreate:
        title: str
        content: str
        theme: str = "default"
        metadata: Dict[str, Any] = field(default_factory=dict)

        def __post_init__(self):
            if not self.title or len(self.title) > 200 or not self.content:
                raise ValueError("title and content are required")

    @dataclass
    class DocumentIR:
        title: str
        blocks: List[Dict[str, Any]]
        theme: str = "default"
        metadata: Dict[str, Any] = field(default_factory=dict)

    @dataclass
    class DocumentStatus:
        status: str
        error: Optional[str] = None
