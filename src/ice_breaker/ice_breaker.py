from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from ice_breaker.third_party.linkedin import scrape_linkedin_profile

load_dotenv()

def main():

    print("Hello LangChain")

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0)

    chain = summary_prompt_template | llm
    information = scrape_linkedin_profile("mock", True)
    res = chain.invoke(input={"information": information})

    print(res.content)

if __name__ == "__main__":
    main()
