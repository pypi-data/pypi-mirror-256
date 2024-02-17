from typing import TypedDict

class ScenarioCreateParams(TypedDict):
  description: str
  name: str
  priority: int
  
class ScenarioDestroyParams(TypedDict):
  force: bool