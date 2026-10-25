from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
import time
import hashlib
import json
from auctor.identity.key import Identity
import jcs

class MandateModel(BaseModel):
    type: str = "mandate"
    id: str = Field(default_factory=lambda: f"m_{uuid.uuid4().hex[:8]}")
    issuer: str
    subject: str
    capabilities: Dict[str, Any]
    parent_id: Optional[str] = None
    signature: Optional[Dict[str, str]] = None

class ReceiptModel(BaseModel):
    type: str = "receipt"
    mandate_id: str
    timestamp: int = Field(default_factory=lambda: int(time.time()))
    action: Dict[str, Any]
    outcome: Dict[str, Any]
    signature: Optional[Dict[str, str]] = None
