# AI-Powered Retail Analytics Chatbot

## Project Overview
This project implements an AI-powered chatbot that helps users analyze retail data to identify the **best outlet**, the **best product**, and answer **natural language questions** about sales performance.  
The chatbot follows a **data-grounded (RAG-style)** approach by combining structured dataset filtering with a **Groq LLaMA 3 large language model** to generate accurate, non-hallucinated responses.

---

## Dataset
**Source:**  
https://www.datayb.com/datasets/dataset-details/datayb_dataset_details_p333awduhf2dv5t/

The dataset is downloaded and stored locally in the `data/` directory.

### Dataset Contains
- Outlet details and locations
- Product and category information
- Order-level sales data
- Customer review sentiment (when available)

---

## Key Columns Used
- **Outlet-level:** `outlet`, `city`
- **Product-level:** `product`, `category`
- **Sales-related:** `quantity`, `unitprice`, `sales`
- **Derived metrics:** `total_sales`

---

## Definition of “Best”
- **Best Outlet:** Outlet with the **highest total sales** in the dataset
- **Best Product:** Product with the **highest total sales** in the dataset

> Sentiment data is used only as supporting context when available.

---

## Tech Stack
- Python
- Pandas
- Streamlit
- Groq API (llama-3.3-70b-versatile`)

---

## Setup Instructions

### 1. Clone the repository

git clone <your-repository-url>
cd ai-chatbot


### 2. Create and activate a virtual environment

# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Windows (CMD)
python -m venv .venv
.venv\Scripts\activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
   

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set the Groq API Key

# macOS/Linux
export GROQ_API_KEY="your_api_key_here"

# Windows (PowerShell)
setx GROQ_API_KEY "your_api_key_here"


### 5. Run the application

streamlit run app.py


## Example Queries

-Which outlet has the highest sales in Surat?
-Which burger is the best?
-Compare Navsari, Surat, and Vapi outlets.
-How many outlets are there in Navsari?

## Features

-Data preprocessing and aggregation
-Computation of best outlet and best product
-RAG-style context grounding using real dataset rows
-Deterministic handling of count-based questions
-Groq LLM integration with hallucination prevention
-Streamlit-based chat interface

## Project Structure
ai-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── order.csv
│   ├── outlet.csv
│   ├── menu.csv
│   ├── outlet_menu.csv
│   └── review.csv

## Notes

-The Groq API key is loaded from an environment variable and is not hardcoded.
-The chatbot answers strictly based on the dataset context and clearly states when information is not available.
-Make sure to use a currently supported Groq LLaMA 3 model to avoid decommissioned model errors.