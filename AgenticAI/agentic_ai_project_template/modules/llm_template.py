from openai import OpenAI

def generate_response(prompt):
    client = OpenAI(api_key="YOUR_API_KEY")
    response = client.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text

response = generate_response("Suggest steps for building an AI agent.")
print(response)