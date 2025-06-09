from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
import time

Api_key = os.getenv("GEMINI_API_KEY")
Base_Url = os.getenv("GEMINI_BASE_URL")

client = OpenAI(
    api_key=Api_key,
    base_url=Base_Url
)

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.
you can talk in hindi hinglish and english

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query
4 every maths operation should be done as step solution and you can use solution step as many time as you can
5. when output comes dont provide in simple way add some text also like you are giving answer to person
6. in language user ask question just answer in same language and same tone but agar kuch bhi language nhi di gyi hai to default language English 


Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}
"""
Messages = [
            {"role": "system","content":system_prompt},
        ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

class InputRequest(BaseModel):
    input_str: str

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/chat")
def Cot_visualizer(req: InputRequest):

    Messages = [
            {"role": "system","content":system_prompt},
        ]
    
    query = req.input_str
    Messages.append({"role":"user","content":query})
    while True:
        result = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=Messages,
            response_format={"type":"json_object"},
            temperature=1.9
        )

        parsed_response = json.loads(result.choices[0].message.content)

        Messages.append({"role":"assistant","content":json.dumps(parsed_response)})
        if parsed_response.get("step") != "output":
            time.sleep(7)
            continue
        break
    return {"messages": Messages}