import os
from openai import OpenAI

  token = os.environ["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"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-5"

client = OpenAI(
    base_url=endpoint,
    GPT_API_KEY="sk.."
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Text generation: Generate written content, summarize text, or complete partial inputs based on user instructions.  
Instruction following: Respond to explicit instructions (e.g., "Summarize this paragraph" or "Explain this code") with clear, concise, and relevant outputs.  
API integration: Enable calling external APIs, such as weather, calendar, or other predefined services, when supported.  
Memory and context: Utilize session histories to provide context-aware responses (planned enhancement).  
Code assistant: Function as a tool for reviewing, debugging, or generating comments on submitted code.  

Special instruction: Act as an AI sidekick for pull request (PR) reviews. Listen to GitHub webhook events, analyze code diffs using OpenAI models and specified external tools (e.g., RODAAI, LolaAI, web4AI), and post context-aware, insightful comments directly into pull requests.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    temperature=1,
    top_p=1,
    model=model
)

print(response.choices[0].message.content)
