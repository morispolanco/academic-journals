import streamlit as st
from docx import Document
import re

# Configuración inicial de la página
st.set_page_config(page_title="Manuscript Review Chatbot", page_icon="📚")

# Título y descripción
st.title("Manuscript Review Chatbot")
st.write("""
Welcome to the Manuscript Review Chatbot! Ask me anything about your manuscript or journal guidelines, and I'll guide you step by step.
""")

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Función para verificar formato básico
def check_format(text):
    word_count = len(re.findall(r'\w+', text))
    pages_estimate = word_count / 250  # Estimación: 250 palabras por página
    return {
        "word_count": word_count,
        "pages_estimate": pages_estimate
    }

# Simular una llamada a una API para obtener las directrices de la revista
def fetch_journal_guidelines(journal_name):
    # Endpoint ficticio para simular una API
    url = f"https://api.example.com/journal-guidelines/{journal_name.replace(' ', '-')}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Suponemos que la API devuelve un JSON
    except requests.exceptions.RequestException:
        return None

# Función para evaluar el manuscrito
def evaluate_manuscript(document, guidelines=None):
    # Extraer texto del manuscrito
    manuscript_text = "\n".join([para.text for para in document.paragraphs])
    
    # Verificar formato básico
    format_info = check_format(manuscript_text)
    
    # Evaluar estructura básica
    evaluation = []
    evaluation.append(f"- **Estimated Word Count**: {format_info['word_count']}")
    evaluation.append(f"- **Estimated Page Count**: {format_info['pages_estimate']:.1f} pages")
    
    # Verificar resumen
    abstract_match = re.search(r'abstract[\s\S]*?introduction', manuscript_text.lower())
    if abstract_match:
        abstract_text = abstract_match.group().strip()
        abstract_word_count = len(re.findall(r'\w+', abstract_text))
        evaluation.append(f"- **Abstract Length**: {abstract_word_count} words")
        if guidelines and 'abstract_length' in guidelines:
            if abstract_word_count > guidelines['abstract_length']:
                evaluation.append("- **Warning**: Abstract exceeds recommended length.")
    else:
        evaluation.append("- **Warning**: Abstract not found. Ensure it is clearly labeled.")

    # Verificar longitud total
    if guidelines and 'max_pages' in guidelines:
        if format_info['pages_estimate'] > guidelines['max_pages']:
            evaluation.append("- **Warning**: Manuscript exceeds recommended length.")

    # Verificar palabras clave
    keywords_match = re.search(r'keywords?:\s*([\w\s,]+)', manuscript_text.lower())
    if keywords_match:
        keywords = [kw.strip() for kw in keywords_match.group(1).split(",")]
        evaluation.append(f"- **Keywords Found**: {len(keywords)} ({', '.join(keywords)})")
        if len(keywords) < 3:
            evaluation.append("- **Suggestion**: Include at least 3–5 relevant keywords.")
    else:
        evaluation.append("- **Suggestion**: Add a keywords section to your manuscript.")

    # Feedback general
    evaluation.append("- **Formatting**: Use Times New Roman, size 12, double-spaced, 1-inch margins.")
    evaluation.append("- **References**: Follow APA (7th edition) style for citations and references.")

    return "\n".join(evaluation)

# Procesar la consulta del usuario
def process_query(user_input, manuscript_text=None, guidelines=None):
    if "manuscript" in user_input.lower():
        return "Please upload your manuscript file to proceed."
    
    if "journal" in user_input.lower():
        journal_name = user_input.split("journal")[-1].strip()
        guidelines = fetch_journal_guidelines(journal_name)
        if guidelines is None:
            return f"Sorry, I couldn't find specific guidelines for '{journal_name}'. Please double-check the journal name or consult its official website."
        else:
            return f"""
**Guidelines for {journal_name}:**
- Focus and Scope: {guidelines.get('focus', 'Not specified')}
- Abstract Length: ≤ {guidelines.get('abstract_length', 'Not specified')} words
- Maximum Length: {guidelines.get('max_pages', 'Not specified')} pages
- Formatting: {guidelines.get('formatting', 'Not specified')}
- References: Follow {guidelines.get('references', 'Not specified')} style
"""
    
    if manuscript_text:
        uploaded_file = st.session_state.get("uploaded_file")
        if uploaded_file:
            document = Document(uploaded_file)
            return evaluate_manuscript(document, guidelines)

    return "I'm here to help! Ask me about your manuscript or journal guidelines."

# Entrada del usuario
user_input = st.chat_input("Ask me something...")

# Procesar la entrada del usuario
if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Procesar la consulta
    response = process_query(user_input)

    # Agregar respuesta del chatbot al historial
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Permitir al usuario cargar un archivo
uploaded_file = st.file_uploader("Upload your manuscript (Word file)", type=["docx"])
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    st.success("File uploaded successfully!")
