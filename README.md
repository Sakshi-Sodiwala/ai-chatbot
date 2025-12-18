AI-Powered Retail Analytics Chatbot

Project Overview
This project implements an AI-powered chatbot that helps users analyze retail data to identify the best outlet, the best product, and answer natural language questions about sales performance.

The chatbot follows a data-grounded (RAG-style) approach by combining structured dataset filtering with the Groq LLaMA 3.1 large language model to generate accurate, non-hallucinated responses.


Dataset
Source:
https://www.datayb.com/datasets/dataset-details/datayb_dataset_details_p333awduhf2dv5t/

The dataset is downloaded and stored locally in the data/ directory.

Dataset Includes
- Outlet details and locations
- Product and category information
- Order-level sales data
- Customer review sentiment (when available)


Key Columns Used
Outlet-level: outlet, city
Product-level: product, category
Sales-related: quantity, unitprice
Derived metrics: total_sales


Definition of “Best”
Best Outlet: Outlet with the highest total sales
Best Product: Product with the highest total sales

Sentiment and review data are used only as supporting context when available.


Tech Stack
- Python
- Pandas
- Streamlit
- Groq API (LLaMA 3.3 – 70B)


Setup Instructions

1. Clone the repository
git clone https://github.com/Sakshi-Sodiwala/ai-chatbot.git
cd ai-chatbot

2. Create and activate a virtual environment

Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Set the Groq API Key

Windows (PowerShell):
setx GROQ_API_KEY "your_api_key_here"

macOS / Linux:
export GROQ_API_KEY="your_api_key_here"

5. Run the application
streamlit run app.py


Example Queries
- Which outlet has the highest sales in Surat?
- Which burger is the best?
- Compare Navsari, Surat, and Vapi outlets.
- How many outlets are there in Navsari?


Features
- Dataset loading and preprocessing
- Computation of best outlet and best product
- City and outlet comparison based on sales
- RAG-style context grounding using real dataset rows
- Deterministic handling of count-based questions
- Groq LLM integration with hallucination prevention
- Streamlit-based chat interface


Project Structure
ai-chatbot/
app.py
requirements.txt
README.md
data/
order.csv
outlet.csv
menu.csv
outlet_menu.csv
review.csv
screenshots/
ui.png
best_outlet.png
best_product.png


Notes
The Groq API key is loaded from an environment variable and is not hardcoded.
The chatbot answers strictly based on dataset context and clearly states when information is not available.