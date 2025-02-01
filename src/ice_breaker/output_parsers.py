from typing import Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


# class Summary(BaseModel):
#     summary: str = Field(description="summary")
#     facts: list[str] = Field(description="interesting factions about them")
#
#     def to_dict(self):
#         return {"summary": self.summary, "facts": self.facts}

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: list[str] = Field(description="interesting facts about them")

    def to_dict(self) -> dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
