import pandas as pd
import streamlit as st
import os
from groq import Groq

# =============================
# Data Loading & Preprocessing
# =============================

def load_data():
    order_df = pd.read_csv("data/order.csv")
    outlet_df = pd.read_csv("data/outlet.csv")
    menu_df = pd.read_csv("data/menu.csv")
    outlet_menu_df = pd.read_csv("data/outlet_menu.csv")
    review_df = pd.read_csv("data/review.csv")
    return order_df, outlet_df, menu_df, outlet_menu_df, review_df


def clean_columns(df):
    df.columns = df.columns.str.lower().str.strip()
    return df


@st.cache_data
def build_master_dataframe():
    order_df, outlet_df, menu_df, outlet_menu_df, review_df = load_data()

    order_df = clean_columns(order_df)
    outlet_df = clean_columns(outlet_df)
    menu_df = clean_columns(menu_df)
    outlet_menu_df = clean_columns(outlet_menu_df)
    review_df = clean_columns(review_df)

    # Derived metric
    order_df["sales"] = order_df["quantity_"] * order_df["unitprice_"]

    df = pd.merge(
        order_df,
        outlet_menu_df,
        left_on="outlet_product_id_",
        right_on="id",
        how="left"
    )

    df = pd.merge(
        df,
        outlet_df,
        left_on="outletid",
        right_on="outlet_id",
        how="left"
    )

    df = pd.merge(
        df,
        menu_df,
        on="productid",
        how="left"
    )

    df = pd.merge(
        df,
        review_df[["outlet_product_id_", "sentiment"]],
        on="outlet_product_id_",
        how="left"
    )

    return df


# =============================
# Analytics Functions
# =============================

def get_best_outlets(df, top_n=5):
    return (
        df.groupby(["outlet", "city"])
        .agg(total_sales=("sales", "sum"))
        .sort_values("total_sales", ascending=False)
        .head(top_n)
        .reset_index()
    )


def get_best_products(df, top_n=5):
    return (
        df.groupby(["product", "category"])
        .agg(total_sales=("sales", "sum"))
        .sort_values("total_sales", ascending=False)
        .head(top_n)
        .reset_index()
    )


def compare_cities(df, cities):
    filtered = df[df["city"].isin(cities)]
    if filtered.empty:
        return pd.DataFrame()

    return (
        filtered.groupby("city")
        .agg(total_sales=("sales", "sum"))
        .reset_index()
    )


# =============================
# RAG Context Selection
# =============================

def retrieve_context(df, question):
    q = question.lower()

    # ---- Count questions are handled outside LLM ----
    if q.startswith("how many"):
        return "__COUNT__"

    # ---- City comparison ----
    if "compare" in q:
        cities = df["city"].dropna().unique().tolist()
        mentioned = [c for c in cities if c.lower() in q]
        if len(mentioned) >= 2:
            return compare_cities(df, mentioned)

    # ---- City filter ----
    for city in df["city"].dropna().unique():
        if city.lower() in q:
            df = df[df["city"].str.lower() == city.lower()]

    # ---- Best outlet ----
    if "outlet" in q:
        return get_best_outlets(df)

    # ---- Best product ----
    if "product" in q or "burger" in q:
        return get_best_products(df)

    return df.sample(10) if not df.empty else pd.DataFrame()


# =============================
# Dataset Summary (Adaptive)
# =============================

def dataset_summary(df):
    lines = [f"Total records: {len(df)}"]

    if "outlet" in df.columns:
        lines.append(f"Outlets: {df['outlet'].nunique()}")

    if "product" in df.columns:
        lines.append(f"Products: {df['product'].nunique()}")

    if "total_sales" in df.columns:
        lines.append(f"Total sales: {df['total_sales'].sum():.2f}")

    if "sales" in df.columns:
        lines.append(f"Total sales: {df['sales'].sum():.2f}")

    return "\n".join(lines)


# =============================
# Groq LLM
# =============================

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_groq(context_df, question):
    if context_df.empty:
        return "The requested information is not available in the dataset."

    summary = dataset_summary(context_df)
    context_text = summary + "\n\n" + context_df.to_string(index=False)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a data-grounded assistant. "
                "Answer the question directly in the first sentence. "
                "When identifying the best outlet or product, base the decision ONLY on total sales. "
                "Give numeric justification immediately. "
                "If information is missing, say it is not available in the dataset."
            )
        },
        {
            "role": "user",
            "content": f"DATA:\n{context_text}\n\nQUESTION:\n{question}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content



# Streamlit UI


st.title("AI-Powered Retail Analytics Chatbot")
st.caption("AJAYS FASTFOOD")

st.markdown("### Example Queries")
st.markdown("- Which outlet has the highest sales in Surat?")
st.markdown("- Which burger is the best?")
st.markdown("- Compare Surat and Navsari outlets")
st.markdown("- How many outlets are there in Navsari?")

question = st.text_input("Ask a question")

if question:
    master_df = build_master_dataframe()
    q = question.lower()

    #  Deterministic COUNT handling 
    if q.startswith("how many") and "outlet" in q or "store" in q:
        for city in master_df["city"].dropna().unique():
            if city.lower() in q:
                count = master_df[master_df["city"].str.lower() == city.lower()]["outlet"].nunique()
                st.write(f"There are {count} outlets in {city}.")
                st.stop()

        st.write(f"There are {master_df['outlet'].nunique()} outlets in total.")
        st.stop()

    # RAG flow
    context = retrieve_context(master_df, question)
    answer = ask_groq(context, question)
    st.write(answer)

