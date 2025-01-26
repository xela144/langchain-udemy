from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from ice_breaker.third_party.linkedin import scrape_linkedin_profile
from ice_breaker.agents.linkedin_lookup_agent import lookup

load_dotenv()


def ice_break_with(name: str) -> str:
    linkedin_url = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(profile_url=linkedin_url, mock=True)

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
    information = scrape_linkedin_profile("__", True)
    res = chain.invoke(input={"information": information})

    print(res.content)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query", metavar="Linkedin search query", nargs="+", help="The search string for the URL"
    )
    args = parser.parse_args()
    query = " ".join(args.query)
    print(f"Search string: {query}")
    linkedin_url = ice_break_with(name=query)
    print(linkedin_url)


if __name__ == "__main__":
    main()
