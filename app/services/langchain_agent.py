from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun

llm = ChatOpenAI(temperature=0, model="gpt-4")

search = DuckDuckGoSearchRun()
tools = [
    Tool(name="Search", func=search.run, description="Search the web for up-to-date information"),
]

agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

def run_agent(prompt: str):
    return agent.run(prompt)
