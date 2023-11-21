import openai

openai.api_key = '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'

response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="capital of india",
        max_tokens=250,
        temperature=0
    )
print(response)