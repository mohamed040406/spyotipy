from typing import Optional, Dict, Any


class Copyright:
    def __init__(self, data):
        self._update(data)

    def _update(self, data: Dict[str, Any]):
        self.text: Optional[str] = data.pop("text", None)
        self.type: Optional[str] = data.pop("type", None)
