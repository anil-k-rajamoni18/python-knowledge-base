from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="Explain Python Data types like you would to a 5 year old."
)

print("Explanation:\n", response.output_text)