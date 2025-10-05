import openai
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAPI_KEY"))


def extract_financial_data_helper(text):
    prompt = get_prompt_financial() + text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": prompt
             }
        ]
    )
    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })



def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "MicroStrategy",
        "Stock Symbol": "MSTR",
        "Revenue": "$125 millions",
        "Net Income": "$15 million",
        "EPS": "0.80 $"
    }
    News Article:
    ============

    '''

if __name__ == '__main__':
    text = '''
    In Q2 2025, MicroStrategy reported revenues of $125 million, up 12% year-over-year, with net income of $15 million and an EPS of $0.80. The company's strong performance was driven by increased demand for its business intelligence software and a 3% gain in its Bitcoin holdings. As of June 30, 2025, MicroStrategy held approximately 140,000 BTC, valued at $17.5 billion.
    '''
    df = extract_financial_data_helper(text)

    print(df.to_string())