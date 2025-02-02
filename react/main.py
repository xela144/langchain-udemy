from dotenv import load_dotenv
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import tool
from langchain_core.tools import render_text_description

load_dotenv()


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
Thought:
"""

tools = [get_text_length]
prompt = PromptTemplate.from_template(template=template).partial(
    tools=render_text_description(tools), tool_names=", ".join([t.name for t in tools])
)

llm = ChatOpenAI(temperature=0, name="gpt-4o-mini", stop=["\nObservation"])

agent = {"input": lambda x: x["input"]} | prompt | llm | ReActSingleInputOutputParser()

res = agent.invoke({"input": "What is the length of 'DOG' in characters?"})
breakpoint()
print(res)
