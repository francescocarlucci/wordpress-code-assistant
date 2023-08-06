import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

st.set_page_config(
    page_title="WordPress Code Assistant | Learn LangChain",
    page_icon="🤓"
)

st.header('🤓 WordPress Code Assistant')

st.subheader('Learn LangChain | Demo Project #4')

st.write('''
This is a demo project related to the [Learn LangChain](https://learnlangchain.org/) mini-course.
...
''')

st.info("You need your own keys to run commercial LLM models.\
    The form will process your keys safely and never store them anywhere.", icon="🔒")

openai_key = st.text_input("OpenAI Api Key", help="You need an account on OpenAI to generate a key: https://openai.com/blog/openai-api")

model = st.selectbox(
	'Select a model',
	(
		'gpt-3.5-turbo',
		'gpt-4'
	),
	help="Make sure your account is enable for GPT4 before using it"
)

task = st.selectbox(
	'Select a sample WordPress task',
	(
		'Store Contact Form 7 submissions as WordPress custom post types',
		'Custom'
	)
)

with st.form("code_assistant"):

	custom_task = st.text_input("Write your custom task (available if Selected Task is Custom)", disabled=(task != "Custom"))

	execute = st.form_submit_button("🚀 Generate Code")

	if execute:

		llm = ChatOpenAI(openai_api_key=openai_key, temperature=0, model_name=model)

		prompt = ChatPromptTemplate.from_template('''
		You are a Senior WordPress developer. Your job is to help me writing the best code
		to achieve the following: {task}
		''')

		chain = LLMChain(llm=llm, prompt=prompt)

		if task == "Custom":
			task = custom_task

		response = chain.run(task)

		st.write(response)

		st.text("") # empty text helps with formatting

st.divider()

st.write('A project by [Francesco Carlucci](https://francescocarlucci.com) - \
Need AI training / consulting? [Get in touch](mailto:info@francescocarlucci.com)')