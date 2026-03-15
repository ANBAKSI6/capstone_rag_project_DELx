import streamlit as st
import requests

st.title("Dell Laptop Assistant")

query = st.text_input("Ask your question")

if st.button("Submit"):

    response = requests.post(
        "http://127.0.0.1:8000/answer",
        json={"query": query}
    )

    if response.status_code == 200:

        result = response.json()

        st.write("### Answer")

        if "answer" in result:
            st.write(result["answer"])
        else:
            st.write("Unexpected response:", result)

    else:
        print(response.status_code)
        st.write("API Error:", response.text)