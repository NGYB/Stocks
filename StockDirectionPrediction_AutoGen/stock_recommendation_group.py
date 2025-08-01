import os
from dotenv import load_dotenv

from autogen import AssistantAgent, GroupChat, GroupChatManager
import pandas as pd

load_dotenv()

# Function to read CSV file and prepare data for aggregation
def read_csv_file():
    print("Reading CSV file...")
    # df = pd.read_csv("./data/Stocks-data - Alphabet.csv")
    # df = pd.read_csv("./data/Stocks-data - Intel.csv")
    df = pd.read_csv("./data/Stocks-data - AT&T.csv")
    return df.to_dict()

# Define LLM configuration
model = "gpt-4.1"
llm_config = {
    "model": model,
    "temperature": 0.9,
    "api_key": os.environ["OPENAI_API_KEY"],
}

# Define the data aggregation agent
data_aggregation_agent = AssistantAgent(
    name="Data_Aggregation_Agent",
    llm_config=llm_config,
    system_message="""
        You collect and aggregate financial data from the provided CSV file for the monthly financial report.
        Analyze key financial metrics such as revenue growth, profit margins, cash flow, debt levels, and other relevant indicators.
        When asked for data, read from the CSV file using the provided function.
    """,
)

# Define the report generation agent
report_generation_agent = AssistantAgent(
    name="Report_Generation_Agent",
    llm_config=llm_config,
    system_message=f"Generate a detailed financial report based on the following data: {read_csv_file()}",
)

# Define the stock analysis agent
stock_analysis_agent = AssistantAgent(
    name="Stock_Analysis_Agent",
    llm_config=llm_config,
    system_message="""
    You analyze financial data to assess the company's stock investment potential.
    Consider factors such as:
    - Revenue growth trends
    - Profitability and margins
    - Cash flow strength
    - Debt levels and financial stability
    - Market position and competitive advantages
    - Industry trends and outlook
    Provide a comprehensive analysis of whether the company is performing well financially.
    """,
)

# Define the stock recommendation agent
stock_recommendation_agent = AssistantAgent(
    name="Stock_Recommendation_Agent",
    llm_config=llm_config,
    system_message="""
    You provide clear stock investment recommendations based on financial analysis.
    Your recommendation should be either:
    - "BUY" - if the company shows strong financial performance, growth potential, and positive indicators
    - "HOLD" - if the company shows mixed or neutral financial indicators
    - "SELL" - if the company shows poor financial performance or concerning indicators
    If the company is doing well, recommend BUY. Otherwise, recommend HOLD or SELL as appropriate.
    Provide your recommendation with clear reasoning based on the financial analysis.
    Include confidence level and key factors that influenced your decision.
    """,
)

# Define the accuracy review agent
accuracy_review_agent = AssistantAgent(
    name="Accuracy_Review_Agent",
    llm_config=llm_config,
    system_message="""
    You check the financial report and stock recommendation for accuracy and consistency.
    Verify that the analysis is based on sound financial principles and the data provided.
    """,
)

# Define the summary generation agent
summary_generation_agent = AssistantAgent(
    name="Summary_Generation_Agent",
    llm_config=llm_config,
    system_message="""
    You summarize the financial report and stock recommendation for executive presentations.
    Only include 2 points: 1. stock recommendation (BUY, HOLD, SELL), and 2. Reason.
    """,
)

# Make the data reading function available to the agents (if needed, e.g. via tool registration)
# For now, agents will be instructed to ask for data and the user can provide it, or you can extend with tool use.

# Create the group chat with all agents
agents = [
    data_aggregation_agent,
    report_generation_agent,
    stock_analysis_agent,
    stock_recommendation_agent,
    accuracy_review_agent,
    summary_generation_agent,
]

groupchat = GroupChat(
    agents=agents,
    messages=[],
    max_round=10, # Max no. of agents that can speak in 1 turn (need to check)
    speaker_selection_method="auto",
    allow_repeat_speaker=True,
)

# Create the group chat manager
manager = GroupChatManager(
    groupchat=groupchat,
    name="GroupChat_Manager",
    llm_config=llm_config,
)

# Initial task to start the workflow
initial_task = (
    """Collect and aggregate financial data for the monthly financial report and stock analysis. "
    "Analyze the data to understand the company's financial performance and prepare for stock investment recommendation. "
    "Generate a detailed report, analyze stock, make a recommendation (BUY if company is doing well), review accuracy, and summarize for executives."""
)

# Start the group chat by sending the initial message to the manager
# The manager will orchestrate the conversation among the agents
data_aggregation_agent.initiate_chat(
    recipient=manager,
    message=initial_task,
    max_turns=2,   # limits the number of total messages exchanged in the chat from the initiating user’s perspective
    summary_method="last_msg",
)
