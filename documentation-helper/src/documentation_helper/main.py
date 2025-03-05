from documentation_helper.backend.core import run_llm
import streamlit as st


def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


def main():
    st.header("Documentation helper bot for Langchain Udemy course")

    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []

    if "chat_answers_history" not in st.session_state:
        st.session_state["chat_answers_history"] = []

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    prompt = st.text_input("Prompt", placeholder="enter a prompt")
    if prompt:
        with st.spinner("Generating response..."):
            generated_response = run_llm(prompt, chat_history=st.session_state["chat_history"])
            sources = set(
                [doc.metadata["source"] for doc in generated_response["source_documents"]]
            )
            formatted_response = (
                f"{generated_response['result']}\n\n {create_sources_string(sources)}"
            )

        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", formatted_response))

    if st.session_state["chat_answers_history"]:
        history = st.session_state["user_prompt_history"]
        responses = st.session_state["chat_answers_history"]
        for generated_response, user_query in zip(responses, history):
            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(generated_response)


if __name__ == "__main__":
    main()
