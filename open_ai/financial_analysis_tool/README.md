````markdown
# Modern Fintech Analysis GenAI Tool

A Streamlit web app that extracts key financial data from news articles using OpenAI's GPT models.

---

![App Sample]([images/screenshot.png])

---

## Features
- Extracts **Company Name, Stock Symbol, Revenue, Net Income, and EPS** from financial news text.
- Displays extracted data in an interactive table.
- Clean, modern UI with colored headers and styled buttons.

---

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-folder>
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key in a `.env` file:

```env
OPENAPI_KEY=your_openai_api_key
```

---

## Usage

1. Run the Streamlit app:

```bash
streamlit run main.py
```

2. Paste a financial news article in the left panel.

3. Click **Get Analysis** to extract financial data.

4. View the results in the right panel.

---

## Example

Input:

> "In Q2 2025, MicroStrategy reported revenues of $125 million, net income of $15 million, and EPS of $0.80."

Output:

| Measure      | Value         |
| ------------ | ------------- |
| Company Name | MicroStrategy |
| Stock Symbol | MSTR          |
| Revenue      | $125 million  |
| Net Income   | $15 million   |
| EPS          | 0.80 $        |

---

## Dependencies

* Python 3.8+
* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [OpenAI](https://pypi.org/project/openai/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

