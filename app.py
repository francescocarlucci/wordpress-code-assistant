import re
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
In this project we will use some core LangChain components (Chains, PromptTemplates, OutputParsers),
to achieve a powerful outcome: a WordPress code assistant capable to handle real development tasks.
It's inspired by an AI-assisted code technique I use in my own development projects.
''')

st.write('''
The whole approach is based on the Divide and Conquer algorithm: solve a problem by dividing it
into smaller sub-problems, solving the sub-problems and combining the solutions to succesfully
complete the initial task. Let's see an example related to WordPress:
''')

st.success("Using this technique, you can use AI to handle most of the tasks frequently \
	found on freelancing sites like Fiverr, Upwork, Freelancer, etc...", icon="🤑")


st.info("You need your own keys to run commercial LLM models.\
    The form will process your keys safely and never store them anywhere.", icon="🔒")

openai_key = st.text_input("OpenAI Api Key", help="You need an account on OpenAI to generate a key: https://openai.com/blog/openai-api")

model = st.selectbox(
	'Select a model',
	(
		'gpt-3.5-turbo',
		'gpt-4'
	),
	help="Make sure your account is elegible for GPT4 before using it"
)

task = st.selectbox(
	'Select a sample WordPress task',
	(
		'Store Contact Form 7 submissions as WordPress custom post types',
		'Write a function that prints out the WP version',
		'Custom'
	)
)

with st.form("code_assistant"):

	custom_task = st.text_input("Write your custom task (available if Selected Task is Custom)", disabled=(task != "Custom"))

	thinking = st.checkbox('Display the full thinking process')

	cross_check = st.checkbox('Execute an additional Chain to cross-check the code provided')

	execute = st.form_submit_button("🚀 Generate Code")

	if execute:

		with st.spinner('Generating code for you...'):

			llm = ChatOpenAI(openai_api_key=openai_key, temperature=0, model_name=model)

			code_prompt = ChatPromptTemplate.from_template('''
			You are a Senior WordPress developer. Your job is to help me writing the best code
			to achieve the following: {task}
			Please make sure to enclose the PHP code in <?php ... ?> and describe your thinking
			proccess in detail.
			''')

			code_chain = LLMChain(llm=llm, prompt=code_prompt)

			if task == "Custom":
				task = custom_task

			code_response = code_chain.run(task)

			# NOTE possible improvement usgin langchain.output_parsers.regex.RegexParser
			#code_matches = re.findall(r'<\?php.*?\?>', code_response, re.DOTALL)
			code_matches = re.findall(r'```php(.*?)```', code_response, re.DOTALL)

			full_code = []
			
			for code in code_matches:

				if len(code) > 20:

					st.code(code, language="php")

					full_code.append(code)

			if thinking:

				st.subheader('Thinking process:')

				st.write(code_response)


			if cross_check and full_code:

				check_prompt = ChatPromptTemplate.from_template('''
				You are a Senior QA Tester. Your job is to make sure that the collowing code:
				{code} is suitable to achieve the following task: {task}
				If the code is good and suitable, just answer "SUCCESS, the code is good for this task".
				If the code is not good for any reason, answer "ERROR" and explain why in detail.
				''')

				check_chain = LLMChain(llm=llm, prompt=check_prompt)

				check_response = check_chain.run({"code":' '.join(full_code), "task":task})

				st.subheader('QA on provided code')

				st.write(check_response)
		
st.divider()

st.write('A project by [Francesco Carlucci](https://francescocarlucci.com) - \
Need AI training / consulting? [Get in touch](mailto:info@francescocarlucci.com)')