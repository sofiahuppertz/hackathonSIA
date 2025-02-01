from typing import Dict

from pydantic import BaseModel


class ClientRequest(BaseModel):
  region: str
    
  def to_json(self) -> Dict[str, str]:
        """
        Converts the UserInput instance into a JSON-compatible dictionary.
        """
        return {
            "region": self.region,
        }