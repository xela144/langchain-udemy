from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from ice_breaker.third_party.linkedin import scrape_linkedin_profile
from ice_breaker.agents.linkedin_lookup_agent import lookup
from ice_breaker.output_parsers import Summary, summary_parser

load_dotenv()


def ice_break_with(name: str) -> tuple[Summary, str]:
    linkedin_url = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(profile_url=linkedin_url, mock=True)

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them

    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(temperature=0, name='gpt-4o-mini')

    chain = summary_prompt_template | llm | summary_parser

    summary: Summary = chain.invoke(input={"information": linkedin_data})

    return summary, linkedin_data.get("profile_pic_url", "")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query", metavar="Linkedin search query", nargs="+", help="The search string for the URL"
    )
    args = parser.parse_args()
    query = " ".join(args.query)
    print(f"Search string: {query}")
    summary = ice_break_with(name=query)
    print(summary)


if __name__ == "__main__":
    main()
