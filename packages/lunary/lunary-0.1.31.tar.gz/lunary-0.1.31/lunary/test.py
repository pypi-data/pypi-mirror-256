import lunary
import os
from openai import OpenAI


client = OpenAI()

def my_llm_agent(input):
  res = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=input 
  )
  return res.choices[0].message.content

os.environ["LUNARY_APP_ID"] = "568c359b-af7f-4020-ad5a-ef50200a6893"
os.environ["LUNARY_API_URL"] = "http://127.0.0.1:3333"

dataset = lunary.get_dataset("test")


for item in dataset:
    result = my_llm_agent(item.input)
    print(result)

    passed, results = lunary.evaluate(
        checklist="pirate",
        input=item.input,
        output=result,
        ideal_output=item.ideal_output
    )

    print(passed, results)

    if not passed:
        print("Test failed!!!")
        print(results)
    else:
        print("Test passed!!!")

    