import os

import openai
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

llm_model = 'gpt-4-1106-preview'

def getTravelPlan(location: str):
  chat = ChatOpenAI(temperature=0.0, model=llm_model)

  template_string = """
    Give me 5 tourist activities to do in {location}? \
    Your response should follow a JSON format with the location and an array of activities(name, location, description, type). \
    If you don't know the type of activity, just put "other". \
    Stick strictly to this format even if multiple location are given, don't create a new JSON object. \
    Example: {{location: "Paris", activities: [{{name: string, location: string, description: string, type: string}}]}} \
    """

  prompt_template = ChatPromptTemplate.from_template(template_string)

  location_schema = ResponseSchema(name='location', description='Address of the activity')
  activity_schema = ResponseSchema(
    name="activities", 
    description="description to model with the example: [{name: string, location:string, description: string, type: string}]", 
    type="array(objects)")

  response_schemas = [activity_schema, location_schema]

  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
  format_instructions = output_parser.get_format_instructions()

  prompt_json = prompt_template.format_messages(location=location, format_instructions=format_instructions)

  model_resonse = chat(prompt_json)

  return output_parser.parse(model_resonse.content)