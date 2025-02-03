from dotenv import load_dotenv
from langchain.agents import AgentExecutor, AgentType, initialize_agent, tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import BaseTool, render_text_description
from langchain_openai import ChatOpenAI


from react_udemy.callbacks import AgentCallbackHandler


load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns the length of the text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("\n").strip('"')
    return len(text)


def main():
    llm = ChatOpenAI(name="gpt-4o-mini")
    agent_executor: AgentExecutor = initialize_agent(
            tools=[get_text_length],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            )
    agent_executor.invoke({
        "input": "What is the length of the text DOG?"})


if __name__ == "__main__":
    main()
