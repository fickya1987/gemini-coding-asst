import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
import streamlit as st


from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

#Get Available Models
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)

# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("Can you write a sample code in python \n"
#                                   "to find prime numbers between 2 integers?")
# print(response.text)

def complete_code(coding_lang, instruction):
    llm = genai.GenerativeModel('gemini-pro')

    template = '''
        ### System:
        You are an exceptionally intelligent programmer who
        consistently delivers accurate and reliable responses
        to user instructions.
        ### User:
        {} in {}")
        '''

    formatted_prompt = template.format(instruction, coding_lang)

    response = llm.generate_content(formatted_prompt)

    return response.text, coding_lang


# if __name__ == '__main__':
#     llm = genai.GenerativeModel('gemini-pro')
#     coding_lang = "python"
#     instruction = "Can you write a sample code in python to find prime numbers between 2 integers?"
#     template = '''
#     ### System:
#     You are an exceptionally intelligent programmer who
#     consistently delivers accurate and reliable responses
#     to user instructions.
#     ### User:
#     {} in {}")
#     '''
#
#     # prompt = PromptTemplate(input_variables=["coding_lang", "instruction"],
#     #                         template=template)
#
#     formatted_prompt = template.format(instruction, coding_lang)
#     #
#     # formatted_prompt = ("Can you write a sample code in python to \n"
#     #                     "find prime numbers between 2 integers?")
#     print(formatted_prompt)
#     response = llm.generate_content(formatted_prompt)
#
#     print(response.text)

def separate_code_and_text(input_text):
    # Find the position of the first and last "/"
    start_pos = input_text.find("```")
    end_pos = input_text.rfind("```")

    if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
        # Extract text before and after the code block
        text_before = input_text[:start_pos].strip()
        code_content = input_text[start_pos + 1:end_pos].strip()
        text_after = input_text[end_pos + 1:].strip()

        return text_before, code_content, text_after
    else:
        # If "/" is not found or in the incorrect order
        return None, None, None

st.set_page_config(
    page_title="CodeAssist",
    page_icon='</>',
    layout='centered',
    initial_sidebar_state='collapsed')

st.header('Coding Assistant')

coding_lang = st.selectbox('Choose the language',
                          ('Python', 'C++', 'Java', 'JavaScript'), index=0)

instruction = st.text_area("Your input here !")

submit = st.button("Generate")

if submit:
    output_text, coding_lang = complete_code(coding_lang, instruction)
    text_before, code_content, text_after = separate_code_and_text(output_text)

    if text_before:
        st.text(text_before)

        # Display code block if present
    if code_content:
        st.code(code_content, language=coding_lang)

        # Display text after the code block
    if text_after:
        st.text(text_after)