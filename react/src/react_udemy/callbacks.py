from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from typing import Any, Optional
from uuid import UUID


class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: dict[str, Any], prompts: list[str], *, run_id: UUID, parent_run_id: Optional[UUID] = None, tags: Optional[list[str]] = None, metadata: Optional[dict[str, Any]] = None, **kwargs: Any) -> Any:

        print(f"****Prompt to LLM was:***\n{prompts[0]}")
        print("**********")

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print(f"****LLM response:***\n{response.generations[0][0].text}")
        print("**********")
