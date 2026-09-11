def fetch_git_issues(language,issue_label,page=1):
    url=f'https://api.github.com/search/issues?q=is:issue label:"{issue_label}" language:{language} state:open&per_page=10&page={page}'
    headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        data=response.json()
        return data["items"]
    else:
        print("GITHUB THREW AN ERROR.")
        return[]

def review_git_fetch(deep_review_url):
    url=deep_review_url
    headers={"Authorization":f"Bearer {os.getenv('GITHUB_TOKEN')}"}
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        data=response.json()
        git_deep_result1=data["title"]
        git_deep_result2=data["body"] or ""
        git_deep_result2_summary=git_deep_result2[:25000]
        git_deep_result3=data["number"]
        git_deep_result4=data["html_url"]
        git_deep_result5=data["created_at"]
        git_deep_result6=data["updated_at"]
        git_deep_net=(f"""#{git_deep_result3}+TITLE IS--{git_deep_result1},
        CONTENT--{git_deep_result2_summary},
        HTML URL FOR THE ISSUE--{git_deep_result4},
        CREATED ON--{git_deep_result5},
        UPDATED ON--{git_deep_result6}""")
        return git_deep_net
    else:
        print("GITHUB THREW AN ERROR.")
        return""

def clean_results(items,issue_number):
    git_messages=[]
    for item in items:
        git_result1=item["title"]
        git_result2=item["url"]
        git_body=item.get("body") or ""
        git_summary=" ".join(git_body.split()[:300])
        git_results[issue_number]=(git_result1,git_summary,git_result2)

        issue_number+=1
    for key,issue_data in git_results.items():
        title=issue_data[0]
        summary=issue_data[1]
        Link=issue_data[2]
        git_combined_text= (f" #{key}::{title}+{summary}+{Link}")
        git_messages.append(("user", git_combined_text))
    return git_messages,issue_number

def call_llm(git_user_input,git_messages):
    git_llm=ChatOpenAI(
        model="nvidia/nemotron-3-super-120b-a12b",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")
    )
    response=git_llm.invoke([
        ("system","""Analyze the project issues the user wants to solve and his current coding level.
            Then filter out the projects most suitable for the user which match the user's current coding level.
            Give the user the summary of the issue and what all he needs to know for solving and contributing in fixing the respective error in a organised pattern.
            DO NOT GIVE THE OUTPUT IN A TABLE FORMAT.
            DO NOT ASK ANY QUESTIONS TO THE USER.
            DO NOT PRINT THE RESULTS OF THE ISSUE UNTIL EXPLICITLY ASKED BY THE USER. 

            At the very end of the response, and nothing after it,output every issue number you mentioned in the response, in this exact format:
                ISSUES_MENTIONED: 1,3,5
                
            RULES for that line:
            - Comma-separated numbers only — no spaces, no symbols, no words like "ISSUE" or "#" or any usage of "*".
            - Include every number you referenced anywhere in your response above.
            - If you mentioned none, write ISSUES_MENTIONED: (with nothing after the colon)."""),
                ("user",git_user_input)
            ]+git_messages)
    return response.content

def in_depth_llm(deep_issue_data):
    git_llm_depth=ChatOpenAI(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")
    )
    response=git_llm_depth.invoke([
        ("system","""Analyze the issue given. Provide a deep analysis on the issue from github."""),
        ("user",deep_issue_data)
    ])
    return response.content

LANGUAGES={
    "1":"python",
    "2":"javascript",
    "3":"java",
    "4":"assembly",
    "5":"html",
    "6":"sql",
    "7":"typescript",
    "8":"c",
    "9":"c++",
    "10":"c#", 
    }

ISSUES={
    "1":"bug",
    "2":"documentation",
    "3":"duplicate",
    "4":"enhancement",
    "5":"good first issue",
    "6":"help wanted",
    "7":"invalid",
    "8":"question",
    "9":"wontfix",
    }

print("\nGITHUB ISSUE FINDER\n")
git_results={}
git_messages=[]
issue_number=1
page=1
import os
import requests 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import time
import re
load_dotenv()

while True:
    language_chosen=input("""WHAT CODING LANGUAGE DO YOU WORK ON?
        1. PYTHON
        2. JAVA SCRIPT
        3. JAVA
        4. ASSEMBLY
        5. HTML
        6. SQL
        7. TYPESCRIPT
        8. C
        9. C++
        10. C# 
        """).strip()

    if language_chosen in LANGUAGES:
        language_chosen=LANGUAGES[language_chosen]
        break
    elif language_chosen in LANGUAGES.values():
        language_chosen=language_chosen.lower()
        break
    else:
        print("Not a valid option,try again")

while True:
    user_issue=input("""\nWHAT ISSUE DO YOU WANT TO WORK ON?
        1. BUG
        2. DOCUMENTATION
        3. DUPLICATE
        4. ENHANCEMENT
        5. GOOD FIRST ISSUE
        6. HELP WANTED
        7. INVALID
        8. QUESTION
        9. WONTFIX
        """)

    if user_issue in ISSUES:
        user_issue=ISSUES[user_issue]
        break
    elif user_issue in ISSUES.values():
        user_issue=user_issue.lower()
        break
    else:
        print("Not a valid option,try again")

items=fetch_git_issues(language_chosen,user_issue,1)
git_messages,issue_number=clean_results(items,issue_number)

print("\nPLEASE PROVIDE OUR AI WITH THE ISSUES YOU WANT TO FIX AND YOUR CURRENT CODING LEVEL FOR OPTIMAL FUNCTIONING.\n")
git_user_input=input("You: ")

start_git_response=time.time()
git_ai_response=call_llm(git_user_input,git_messages)

print(git_ai_response)
end_git_response=time.time()
duration_git_response=end_git_response-start_git_response
print(f"Response took {duration_git_response:.2f} seconds")

while True:
    while True:
        more_projects=input("""\nDO YOU WANT TO LOOK FOR MORE ISSUES?
        TYPE YES IF YES
        TYPE NO IF YOU WANT TO DIVE DEEPER INTO THE ISSUES ALREADY SHOWN.
        """).strip().upper()

        if more_projects=="YES":
            page+=1
            items=fetch_git_issues(language_chosen,user_issue,page)
            git_messages,issue_number=clean_results(items,issue_number)

            git_user_input=input("You: ")
            start_git_response2=time.time()
            git_ai_response=call_llm(git_user_input,git_messages)
            print(git_ai_response)

            end_git_response2=time.time()
            duration_git_response2=end_git_response2-start_git_response2
            print(f"Response took {duration_git_response2:.2f} seconds.")

        elif more_projects=="NO":
            mentioned_numbers_int=[]
            mentioned_numbers=re.search(r"ISSUES_MENTIONED:(.*)",git_ai_response)
            if mentioned_numbers==None:
                print("NO ISSUES PRINTED")
            else:
                mentioned_numbers_int=[int(num) for num in re.findall(r"\d+",mentioned_numbers.group(1))]
            if len(mentioned_numbers_int)==0:
                print("NO DESIRABLE ISSUES WERE FOUND.")
                break
            else:
                while True:
                    try:
                        git_deep_review=int(input(f"WHICH PROJECT DO YOU WANT A DEEPER INSIGHT ON?--{mentioned_numbers_int}").strip())
                        if git_deep_review in mentioned_numbers_int:
                            deep_review_url=(git_results[git_deep_review][2])
                            deep_issue_data=review_git_fetch(deep_review_url)
                            git_llm_review=in_depth_llm(deep_issue_data)
                            print(git_llm_review)
                            break
                        else:
                            print("PUT THE EXACT NUMERICAL ISSUE NUMBER SHOWN IN THE LIST.")
                    except ValueError:
                        print("PLEASE ENTER A VALID NUMBER")
            break

        if more_projects=="NO":
            break
