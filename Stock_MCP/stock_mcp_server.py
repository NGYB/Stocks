import os
import pandas as pd
import yfinance as yf

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("stock_mcp")

DATA_DIR = "data"

@mcp.tool()
def get_price(stock_code: str) -> float:
    """
    Get stock data from Yahoo Finance.

    Args:
        stock_code (str): The stock code to fetch data for.

    Returns:
        float: The current stock price.
    """

    stk = yf.Ticker(stock_code)

    try:
        stk_price = stk.info['currentPrice']
    except:
        try:
            stk_price = stk.info['previousClose']
        except:
            print("Error!!!!!! Unable to get stk_price.")

    return stk_price

@mcp.tool()
def get_analyst_price_target(stock_code: str) -> float:
    """
    Get analyst price targets from Yahoo Finance.

    Args:
        stock_code (str): The stock code to fetch data for.

    Returns:
        float: The mean analyst price target.
    """
    stk = yf.Ticker(stock_code)

    try:
        price_target = stk.analyst_price_targets['mean']
    except:
        print("Error!!!!!! Unable to get analyst price targets.")

    return price_target

@mcp.resource("data://folders")
def get_available_folders() -> str:
    """
    List all available stock folders in the data directory.
    
    This resource provides a simple list of all available stock folders.
    """
    folders = []
    
    # Get all topic directories
    if os.path.exists(DATA_DIR):
        for topic_dir in os.listdir(DATA_DIR):
            topic_path = os.path.join(DATA_DIR, topic_dir)
            if os.path.isdir(topic_path):
                financials_file = os.path.join(topic_path, "financials.csv")
                if os.path.exists(financials_file):
                    folders.append(topic_dir)
    
    # Create a simple markdown list
    content = "# Available Stocks\n\n"
    if folders:
        for folder in folders:
            content += f"- {folder}\n"
        content += f"\nFor example, use @{folder} to access financial data about this particular stock.\n"
    else:
        content += "No topics found.\n"
    
    return content

@mcp.resource("data://{stock}")
def get_stock_data(stock: str) -> str:
    """
    Get detailed information about the stock.
    
    Args:
        topic: The stock to retrieve financial info for
    """
    stock_dir = stock.upper().replace(" ", "_")
    stock_file = os.path.join(DATA_DIR, stock_dir, "financials.csv")
    
    if not os.path.exists(stock_file):
        return f"# No financial data found for stock: {stock}\n\n"
    
    try:
        # Read the CSV file (handles commas in numbers)
        df = pd.read_csv(stock_file, thousands=",")

        # Convert to markdown
        markdown_table = df.to_markdown(index=False)
        
        return markdown_table
    except Exception as e:
        return f"# Error reading stock data for {stock}\n\nThe financials.csv file is corrupted."

@mcp.prompt()
def generate_stock_analysis_prompt(stock: str) -> str:
    """
    Generate a prompt for Claude to find and discuss stock analysis.
    """
    prompt = f"""You are a financial analyst specializing in stock market investments.
        Your task is to research and analyze the stock '{stock}' for potential investment in 2025. 

        Follow these instructions:
        1. First, retrieve the financial data for the stock '{stock}' using the provided resource 'data://{stock}'.

        2. Retrieve the current stock price using the tool 'get_price' with the stock code '{stock}', 
        as well as the analyst price target using the tool 'get_analyst_price_target'.

        3. Next, fetch https://www.google.com/search?q={stock}+stock+analysis+2025+buy+reasons, 
        do a summary including the data retrieved from the resources and tools, 

        4. Organize your findings in a clear, structured format with headings and bullet points for easy readability.

        5. At the end of your response, provide a BUY, SELL, or HOLD recommendation for the stock based on your analysis.

        6. Write the overall summary and your BUY, SELL or HOLD recommendation to a file '{stock}.txt'

    Remember to output a BUY, SELL, or HOLD recommendation for the stock at the end of your analysis! 
    """

    return prompt

if __name__ == "__main__":
    mcp.run(transport='stdio')
