import streamlit as st
from docx import Document
import requests
import os

# Configuración inicial de la página
st.set_page_config(page_title="AMJ Manuscript Optimizer", page_icon="📚")

# Título y descripción
st.title("AMJ Manuscript Optimizer")
st.write("""
Welcome to the AMJ Manuscript Optimizer! This tool is designed to help you prepare and optimize your academic manuscript for submission to the **Academy of Management Journal (AMJ)**. 
Follow the steps below to get started.
""")

# Cargar archivo Word
uploaded_file = st.file_uploader("Upload your manuscript (Word file)", type=["docx"])
if uploaded_file:
    st.success("File uploaded successfully!")
    document = Document(uploaded_file)
    
    # Mostrar contenido del archivo Word
    st.subheader("Manuscript Preview")
    manuscript_text = "\n".join([para.text for para in document.paragraphs])
    st.text_area("Manuscript Content", manuscript_text, height=300)

# Input para consulta del usuario
user_query = st.text_input("Ask a question about your manuscript or AMJ guidelines:")

# Botón para enviar consulta
if st.button("Submit Query"):
    if not user_query:
        st.warning("Please enter a query.")
    elif not uploaded_file:
        st.warning("Please upload your manuscript first.")
    else:
        # Obtener API key desde secrets
        api_key = st.secrets["DASHSCOPE_API_KEY"]
        
        # Preparar datos para la solicitud a la API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": """
You are an expert assistant specialized in preparing and optimizing academic manuscripts for submission to the Academy of Management Journal (AMJ). 
Your tasks include:
1. Providing guidance on the scope and focus of AMJ.
2. Advising on manuscript structure and formatting.
3. Ensuring compliance with AMJ's technical requirements.
"""
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        }
        
        # Realizar solicitud a la API
        try:
            response = requests.post(
                "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            # Mostrar respuesta al usuario
            assistant_response = result["choices"][0]["message"]["content"]
            st.subheader("Assistant's Response")
            st.write(assistant_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Información adicional
st.sidebar.header("About AMJ")
st.sidebar.write("""
The **Academy of Management Journal (AMJ)** is a leading journal in the field of management research. It focuses on publishing high-quality, impactful research that advances theory and practice in areas such as organizational behavior, leadership, strategy, human resources, innovation, and entrepreneurship.
""")
st.sidebar.write("For more details, visit the [official AMJ website](https://journals.aom.org/amj).")

# Guardar API key en secrets
st.sidebar.header("API Key Setup")
st.sidebar.write("To use this app, save your DashScope API key in the Streamlit secrets file (`secrets.toml`) under the key `DASHSCOPE_API_KEY`.")
