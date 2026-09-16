from pathlib import Path
from langchain_core.tools import tool
from pydantic import BaseModel
from db import insert_details
from typing import Literal, NotRequired, TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import PromptTemplate

llm_qwen_low = ChatOllama(model = "qwen2.5:7b", temprature = 0)
llm_qwen_high = ChatOllama(model = "qwen2.5:7b", temprature = 1)

class output_format(BaseModel):
    ''' An analysis of user's given content what is the intent of content and on what basis
    intent is decide and does the user need to give reply  '''
    summary: str
    ''' this is summary of the body text ''' 
    purpose: str
    ''' What is the intent or purpose of the content '''
    reply: Literal["Yes", "No"]
    ''' Do user need to give reply  '''

class State(TypedDict):
    mail: dict
    summarize_node: output_format

def body_summarizer(state: State):
    """ it summarize the content of the body"""
    mail = state["mail"]
    content = mail["body_content"]
    Body_prompt = PromptTemplate.from_template(""" Follow the instruction
    
    Important:
    - First read whole the content 
    - make the summary of the content
    - Summarization must be easy to understand and It must contain only important text 
    - Identify why the mail is sent 
    - Specify purpose of mail to user in few line
    - Reply is needed or not answer this in YES Or NO only

    'content': {content} 
    """)  

    structured_llm = llm_qwen_low.with_structured_output(output_format)
    model = Body_prompt | structured_llm

    answer = model.invoke(content)

    # adding data to the database
    insert_details(mail, answer)
    
    return {'summarize_node': answer}

def reply_needed(content: str):
    ''' Not completed yet'''
    pass

def build_graph():
    # creating the Langgraph 
    builder = StateGraph(State)
    builder.add_node("Summary", body_summarizer) # here 'Summary' cause it will give us the summary of the mail's content
    builder.add_edge(START, "Summary")
    builder.add_edge("Summary", END)
    graph = builder.compile()

    return graph

def graph_call(data):
    graph = build_graph()
    answer = graph.invoke({'mail': data})
    return answer

