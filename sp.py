import openai

openai.api_key = 

response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="capital of india",
        max_tokens=250,
        temperature=0
    )
print(response)