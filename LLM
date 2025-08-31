import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import  save_tool,  AquilaTool
from flask import Flask,render_template,redirect,url_for,request,jsonify
import random
import string
from langchain.schema import HumanMessage, SystemMessage
chat_history={}
lo=[]
# Load from cache (no more download)
app=Flask(__name__,template_folder='Templates')
@app.route("/",methods=["POST","GET"])
def IsraelGPT():
 if request.method == "POST":
    # Handle JSON request from fetch API
    if request.is_json:
        data = request.get_json()
        user = data.get("user1")
    else:
        # Handle form submission
        user = request.form.get("user1")
        
    print(str(user))
    # if str(email) not in emails:
    #     j1.append(str(email))
    #     return redirect(url_for("code"))
    class ResearchResponse(BaseModel):
        topic: str
        summary: str
        output: str
        sources: list[str]
        tools_used: list[str]
    # openai.api_key=token
    llm= ChatOpenAI(model="gpt-4o-mini",
    api_key=os.getenv('ASP'),
    temperature=0.7
    )
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    # print(completion.choices[0].message)
    # messages=[
    #         SystemMessage(content="You are a helpful assistant."),
    #         HumanMessage(content=user)
    # ]
    
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research assistant that will help generate a research paper. bear in mind that the addmission's phone numbers are:
                 phone:+971 2 564 2229  whatsapp: +971 56 538 4416. if the user greets, make sure to greet them in your output.
                Answer according to Aspen Height school's official website based in Abu Dhabi ,instructions and gain extra info from one of the imports named {{sav}} . bear in mind that , 
                try to answer in 
                a convincing way. if there is no relevant
                data, just simply say 'sorry, no relevant data found'.
                Wrap the output in this format and provide no other text\n{format_instructions},
                """,
               
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    tools = [AquilaTool()]
    # Create a wrapper for the generator to make it compatible with LangChain
    
    # Create an instance of the wrapper
    

    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
    query = str(user) + f"only search Aspen Heights school's official website based in Abu Dhabi and achieve additional info from the mgh.html file"
    print(user)
    chat_history[query]=''
    lkp=[]
    for y,i in chat_history.items():
      lkp.append(str(y))
      lkp.append(str(i))
    raw_response = agent_executor.invoke({"query": query,'messages':lkp})
    try:
    
    # Add the new interaction to chat history
    # chat_history.append({"role": "user", "content": user})
    # chat_history.append({"role": "assistant", "content": raw_response["output"]})
    
    # # Save chat history after each interaction
    # save_chat_history(chat_history)
    
      
        output_json_string = raw_response["output"]
        # Step 2: Parse the JSON string to a Python dict
        # output_dict = json.loads(output_json_string)
        # Step 3: Now pass it to  the parser
        structured_response = parser.parse(output_json_string)
        j=str(structured_response).find("sources")
        k=str(structured_response).find("summary")
        v=str(structured_response).find("tools_used")
        b=structured_response
        # Return proper JSON response for AJAX requests
        chat_history[query]=structured_response.output
        if request.is_json:
            chat_history[query]= jsonify({
            
                "output": structured_response.output,
                
            })
            n=structured_response.output
            if 'no relevant data ' in str(n):
                return jsonify({"output": structured_response.output+"you can contact the admission's  team through their email : admissions@ahbs.ae or their:" \
                " phone:+971 2 564 2229  whatsapp: +971 56 538 4416"})
            return jsonify({
            
                "output": structured_response.output,
                
            })
        # else:
            # Return HTML for form submissions
            
        return f'{structured_response},{render_template("button.html", content=structured_response.output)}'
    except Exception as e:
        if request.is_json:
            return jsonify({"error": "Error parsing response", "details": str(e)}), 500
        else:
            return "Error parsing response", e, "Raw Response - ", raw_response
 return render_template("button.html")









# example: access emails from Admissions page

# @app.route("/l")
# def ch():
#     return render_template("email.html")
# lo=[]
# lp=[]
# # @app.route("/oi")
# # def oi():
# li=random.choices(string.digits, k=6)
# @app.route("/code",methods=["POST","GET"])
# def code():
#     # lp=[]
#     # max_retries = 5
#     # base_wait_time = 2 
#     # # if request.method == "POST":
#     # if request.method == "POST":
#     #             code = request.form.get("code")
#                 # email=request.form.get("email")
#      # if email not in signed_in_users:
#      #     return redirect(url_for("sign_in"))
#      # else:
#                 # language = request.form.get("language of response")
#                 # user = request.form.get("user")
#                 # email2=request.form.get("email1")
#                 # email1=input("")
#                 import smtplib
#                 from email.message import EmailMessage
#                 l=[]
#                 # Configure your Outlook email credentials
#                 OUTLOOK_EMAIL = 'arash.khajavi.ghk123@gmail.com'  # Replace with your Outlook email address
#                 OUTLOOK_PASSWORD = "zvju tgad kioo pspy"  # Replace with your password or App Password
#                 email = EmailMessage()
#                 email["from"] = "Mosh Khajavi"  # Replace with your name
#                 email["to"] = f"{j1[0]}"  # Replace with the recipient's email address
#                 # print(str(email2))
#                 email["subject"] = "scholarship and registration"
#                 # lu=random.randint(0,9)
#                 email.set_content(
#                     "".join(li)
#                 )
#                 p = []
#                 # p.append(li)
#                 # Send the email using Outlook's SMTP server
#                 # e=str(email2)
#                 # lp.append(e)
#                 # for e in str(email2):
#                 #     p.append(e)
#                 # pr = "".join(p)
#                 # lp.append(str(pr))
#                 # print(lp)
#                 # try:
#                 k=[]
#                 with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
#                         smtp.ehlo()  # Identify yourself to the server
#                         smtp.starttls()  # Secure the connection
#                         smtp.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)  # Log in to your Outlook account
#                         smtp.send_message(email)
#                         k.append(email)# Send the email

#                         # return str(email)
#         #                 print(str(email).split("1.0")[1].strip())
#         #                 if str(code) == str(str(email).split("1.0")[1].strip()):
#         # #             lk.append(j1[0])
#         # #             print(lk)
#         #
#         #
#         #
#         # #             #  re=request.form.get("choice1")
#         # #             #  if str(re) == "fast":
#         #                     j1.clear()
#         #                     return redirect(url_for("IsraelGPT"))
#                 if request.method == "POST":
#                  code = request.form.get("message")
#                  print(str(email).split("1.0")[1].strip())
#                  if str(code) == str(str(email).split("1.0")[1].strip()):
#                  #             lk.append(j1[0])
#                  #             print(lk)
#                  #             #  re=request.form.get("choice1")
#                  #             #  if str(re) == "fast":
#                  #                     k.append(j1[0])
#                  #                     j1.clear()
#                                      emails.append(j1[0])
#                                      return redirect(url_for("IsraelGPT"))
#                             #  elif str(re) == "slow":
#                             #   return redirect(url_for("chat"))
#                 # else:
#                 #             import time
#                 #             time.sleep(10)
#                             # li="".join(random.choices(str//
#                             # return redirect(url_for("oi"))
#                             # li=random.choices(string.digits,k=6)
#                             # return f"unsuccessful , {str(code)} , {str(li)}"
#                 # except:
#                 #     pass
if __name__ == '__main__':
    app.run(debug=True)
