from dotenv import load_dotenv
from langchain.agents import tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import BaseTool, render_text_description
from langchain_openai import ChatOpenAI



load_dotenv()


def dir_helper(obj):
    return [x for x in dir(obj) if not x.startswith("__")]


def find_tool_by_name(tools: list[BaseTool], tool_name: str):
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool name {tool_name} not found")


# The following becomes a Tool that the LLM can decide to use. It
# decides by inspecting the docstring. Note: After using the @tool
# decorator we cannot invoke the function directly; instead we
# use the .invoke() method. Apparently, the .func() method is used
# internally by the framework.
@tool
def get_text_length(text: str) -> int:
    """Returns the length of the text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("\n").strip('"')
    return len(text)


template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""


def main():
    tools: list[BaseTool] = [get_text_length]
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), tool_names=", ".join([t.name for t in tools])
    )

    llm = ChatOpenAI(temperature=0, name="gpt-4o-mini", stop=["\nObservation"])

    intermediate_steps = []

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step: AgentAction | AgentFinish = agent.invoke(
        {
            "input": "What is the length in characters of the following word: DOG",
            "agent_scratchpad": intermediate_steps,
        }
    )
    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        print(observation)
        intermediate_steps.append((agent_step, str(observation)))


    agent_step: AgentAction | AgentFinish = agent.invoke(
        {
            "input": "What is the length in characters of the following word: DOG",
            "agent_scratchpad": intermediate_steps,
        }
    )

    if isinstance(agent_step, AgentFinish):
        print(f"{agent_step.return_values=}")

if __name__ == '__main__':
    main()
