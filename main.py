import openai
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import json
import os 
from fastapi.middleware.cors import CORSMiddleware
import requests
# Functions
from dotenv import load_dotenv

load_dotenv()
def get_response(prompt):
    '''
    Get the ChatGPT response for a given prompt using the provided API key.
    '''
    OPEN_API_KEY=os.getenv('OPEN_API_KEY')
    completion = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.2,
        api_key=OPEN_API_KEY
    )

    return completion['choices'][0]['message']['content']


# FastAPI Application

app = FastAPI()
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["GET", "OPTIONS", "POST", "PUT", "DELETE"],

    allow_headers=["*"],

)



class InputData(BaseModel):
    company_description: str
    differentiator: str
    case_study: str
    current_solution: str
    reason_for_reaching_out: str
    new_teaching: str
    cost_of_inaction: str
    industry_change: str
    linkedin_id:str
    sender_name:str

@app.post("/process_code/")
async def process_code(data: InputData):
    '''
    Process the provided code using ChatGPT.
    '''
    answers = [
        data.company_description,
        data.differentiator,
        data.case_study,
        data.current_solution,
        data.reason_for_reaching_out,
        data.new_teaching,
        data.cost_of_inaction,
        data.industry_change
    ]
    text = '''
Write a BASHO Style cold email with my various inputs. The inputs are {1} {2} {3} {4} {5}  {6} {7} {8}   If one of the inputs is empty, just ignore it. Don't start the email with anything like I hope this email finds you well or other useless pleasantries. Don't speak about what I do, only speak about how I solve their problem. Keep the email under 100 words.
Write the email in this format. Start with a casual reason I am reaching out to the prospect. For the second sentence, either ask a question that makes them think differently about the problem or explain how my product or service can help them. The third sentence should mention how others have already found success with our product or service. The final sentence is the call to action which you can add some slight self deprecating humor into. 
Study the prospect with the provided information and write a email to their understanding level similar to the examples given above.Mention the prospect's name in the mail.get the propect's name from their linkedin profile full name.AT the end of the mail append the best regards or any other wishes  in the end of the mail with name {sender_name}
Here is a couple of examples of an email that I like. The email content is unrelated but I like the tone and structure of the email. Here are some examples I want you to learn from. 
___

Hi Claire,

Came across some recent press coverage in Bustle featuring Aunt Flow on the list of 7 Gender- Neutral Period Products You Should Know About. Thought it would be valuable to connect with you. This one article is already garnering a ton of online engagement for your organization!
Based on this, I took the initiative to put together a media analysis showing everywhere that Aunt Flow has been mentioned in the past 90 days and highlighted which key messages and publications are generating the most web traffic, social engagement, and online conversions 
I've also compiled a list of influential journalists who are writing about you, your peers, and the industry as a whole for you to be able to include in your next campaign.
If we could help you connect with influential journalists, would that be useful to you?

Best,
Annie
___

Here is another email that I like. The content is unrelated but I like the formatting.

""

Gene, 
I recently read a Forbes article about Target's initiative in Perth Amboy, N.J. to replenish inventory faster while allowing stores to reduce the amount of space needed to store merchandise.  (Yes, I read supply chain news on Saturdays.)
Totally get why you folks are using flow centers, but noticed a few things in working with retailers like A and B that you could potentially be doing better to eliminate the stockpiling heaps of clothing, toiletries, books, towels, knick-knacks, and electronics without incurring capital expenses. 
I am, of course, looking for you to consider ACME but am happy to provide you with a few ideas of varying quality you might find interesting even if we never talk again.

Would this be interesting?

___

Here is another email that I like. 

___

Just watched an MCPS video where you stated that school safety was a top priority for the Montgomery School Board. In particular, I took note of your renewed focus around physical, social, and psychological well-being.
Just curious, of the thousands of chats and emails students send, how do you proactively monitor messages for signs of suicide and violent acts so you can prevent these tragedies from happening?  
The reason I ask is that Gaggle helps districts like A and B stop suicide and violent acts by proactively monitoring emails and alerting you if a student is struggling.
If this is of interest, would you be open to learning more? 

Josh
P.S. Here’s a case study from our work with Weld Country School District. 

___

Here is an example of another email that I like

___
Hey varsha – Scanned your profile - noticed the . We’re helping {SIMILAR COMPANY - example Fintech sales teams} pinpointing specific parts of Sequences that need adjusting - which drives reply rates ~18%. Per Gartner, it takes 7-13 touches to get an initial meeting. We have AI that determines the sentiment of responses (positive, negative, neutral) so that you can improve response rates. Is this worth exploring? Thanks, {Rep initials) 
___
Here is an example of another email that I like 
___

I'm familiar with Remerge through your success helping Funstage increase in-app sales by 4% while realizing a 264% return on ad spend.  Not too shabby. :)

I'm not sure if this a problem you have, given your success in the gaming space, but are your SDRs sending more and more cold emails but not booking enough meetings with mobile app developers that you want to get in front of?

We've got an unusual approach for B2B inside sales teams that can potentially help Remerge book 30% more meetings with gaming, retail, and food app developers in less than 45 days (but only if your ACV is greater than 11k).

If you don't book more meetings, you pay nothing.  

Would you be open to chatting sometime?  

Josh
___

Here is another example of an email that I like. 
___

Hey John,

What I used to hate about my job (cofounder and CEO at Rippling) is the admin work of running a business — stuff like paperwork, IT tasks, setting up new employees, payroll, creating an account in gmail, Salesforce, GitHub, AWS, our VPN, etc.  

Rippling makes it go away.

In Rippling, you click a button to hire (or promote or terminate) and you’re done: we generate agreements and paperwork for signing, collect their personal info, ship them a pre-configured computer, set up your accounts in all your different systems, set them up in payroll, etc.

Here are just a few reasons {company} should consider Rippling today:

Free payroll.  Yup, you heard that right.  Rippling is free for smaller/startup companies, including our full service payroll system.  It’s the only free payroll system out there. It’s our way of betting on startups that will some day become big clients.  

IT-dept-in-a-box and Laptop-as-a-service.  Rippling completely automates IT for companies that don’t have in-house IT.  

When you hire someone, we ship their computer automatically.  With all software pre-installed and security managed from day 1 (antivirus, passwords enforced, etc.).

Would love to connect you with someone on my team that can show you the product.  Does next week work for a quick chat?

Parker Conrad

CEO, Rippling

___

)

Here is the information about the prospect :


'''
    proxy_api_key=os.getenv("PROXYCURL_API_KEY")
    headers = {'Authorization': 'Bearer ' + proxy_api_key}
    print(proxy_api_key)
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    linkedin_profile_url = data.linkedin_id
    user_info_response = requests.get(api_endpoint,
                        params={'url': linkedin_profile_url},
                        headers=headers)
    user_info = user_info_response.json()

    if 'similarly_named_profiles' in user_info:
        del user_info['similarly_named_profiles']
    

    
    for i, answer in enumerate(answers, start=1):
        text = text.replace(f"{{{i}}}", answer)
    text = text.replace(f"{{sender_name}}",data.sender_name)

    # Append the code to the provided answers
    prompt = text+json.dumps(user_info)
    print(user_info)
    response_text = get_response(prompt)

    return response_text





if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
