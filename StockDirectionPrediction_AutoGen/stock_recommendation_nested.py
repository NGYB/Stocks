import os
from dotenv import load_dotenv

from autogen import AssistantAgent, UserProxyAgent
import pandas as pd


load_dotenv()

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
    """,
)

# Define the report generation agent
report_generation_agent = AssistantAgent(
    name="Report_Generation_Agent",
    llm_config=llm_config,
    system_message="""
    You generate detailed financial reports based on the aggregated data.
    Include analysis of key financial ratios, trends, and performance indicators.
    """,
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

# Define the user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "my_code",
        "use_docker": False,
    },
)


# Function to read CSV file and prepare data for aggregation
def read_csv_file():
    print("Reading CSV file...")
    df = pd.read_csv("./data/Stocks-data - AT&T.csv")
    return df.to_dict()


# Register nested chats with the user proxy agent
user_proxy.register_nested_chats(
    [
        {
            "recipient": report_generation_agent,
            "message": lambda recipient, messages, sender, config: f"Generate a detailed financial report based on the following data: {read_csv_file()}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": stock_analysis_agent,
            "message": lambda recipient, messages, sender, config: f"Analyze the financial data for stock investment potential: {read_csv_file()}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": stock_recommendation_agent,
            "message": lambda recipient, messages, sender, config: f"Based on the financial analysis, provide a stock investment recommendation (BUY/HOLD/SELL) with reasoning: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": accuracy_review_agent,
            "message": lambda recipient, messages, sender, config: f"Check this report and stock recommendation for accuracy and consistency: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": summary_generation_agent,
            "message": lambda recipient, messages, sender, config: f"Summarize the financial report and stock recommendation for an executive presentation: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
    ],
    trigger=data_aggregation_agent,
)

# Define the initial data aggregation task
initial_task = (
    """Collect and aggregate financial data for the monthly financial report and stock analysis.
    Analyze the data to understand the company's financial performance and prepare for stock investment recommendation."""
)

# Start the nested chat
user_proxy.initiate_chat(
    recipient=data_aggregation_agent,
    message=initial_task,
    max_turns=2,
    summary_method="last_msg",
)
