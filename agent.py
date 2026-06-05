from groq import Groq
from config import GROQ_API_KEY
from tools import list_files, read_file, copy_folder, read_pdf, send_email
import json


client = Groq(
    api_key=GROQ_API_KEY
)


TOOLS = """
You are an AI Agent.

You can use tools.

You must respond ONLY in JSON format.

Available tools:


1. list_files

input:
{
"path":"string"
}


2. read_file

input:
{
"path":"string"
}


3. copy_folder

input:
{
"source":"string",
"destination":"string"
}


4. read_pdf

input:
{
"path":"string"
}


5. send_email

input:
{
"email":"string",
"subject":"string",
"body":"string"
}


IMPORTANT RULES:

Before using any tool:

1. Check if all required inputs exist.

2. If any required input is missing:
DO NOT call the tool.

Return:

{
"tool":"none",
"answer":"ask user for missing information"
}


Example:


User:
send email to abc@gmail.com


Response:

{
"tool":"none",
"answer":"Please provide subject and email body."
}



If all information exists:

Return:

{
"tool":"send_email",
"input":{
"email":"abc@gmail.com",
"subject":"hello",
"body":"message"
}
}



Do not explain.
Return only JSON.
"""


def ask_llm(user_query):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role":"system",
                "content":TOOLS
            },

            {
                "role":"user",
                "content":user_query
            }

        ]
    )

    return response.choices[0].message.content.strip()



def generate_final_answer(prompt):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role":"system",
                "content":
                """
                You are a helpful assistant.
                Answer user using the tool result.
                """
            },

            {
                "role":"user",
                "content":prompt
            }

        ]
    )


    return response.choices[0].message.content.strip()



def validate_email(email):

    import re

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern,email)



def execute_tool(llm_output):

    try:

        data = json.loads(llm_output)


    except Exception:

        return {
            "status":"error",
            "message":"Invalid JSON"
        }


    tool = data.get("tool")

    inputs = data.get("input",{})


    # no tool required
    if tool == "none":

        return data.get(
            "answer",
            "Need more information"
        )


    try:


        if tool == "send_email":


            email = inputs.get("email")
            subject = inputs.get("subject")
            body = inputs.get("body")


            # validation

            if not email:
                return "Please provide email address."


            if not validate_email(email):

                return "Invalid email format."


            if not subject:

                return "Please provide email subject."


            if not body:

                return "Please provide email body."



            return send_email(
                email,
                subject,
                body
            )



        elif tool == "read_file":

            return read_file(
                inputs["path"]
            )



        elif tool == "list_files":

            return list_files(
                inputs["path"]
            )



        elif tool == "copy_folder":

            return copy_folder(
                inputs["source"],
                inputs["destination"]
            )



        elif tool == "read_pdf":

            return read_pdf(
                inputs["path"]
            )


        return "Unknown tool"



    except Exception as e:


        return {
            "status":"tool_error",
            "message":str(e)
        }




def run_agent(user_query):


    print("\nUSER:")
    print(user_query)


    llm_output = ask_llm(user_query)


    print("\nLLM:")
    print(llm_output)



    result = execute_tool(llm_output)


    print("\nRESULT:")
    print(result)



    final_prompt = f"""

User:
{user_query}


Agent Result:

{result}


Reply naturally.

"""


    return generate_final_answer(
        final_prompt
    )