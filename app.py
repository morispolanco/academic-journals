import streamlit as st
from docx import Document
import re

# Configuración inicial de la página
st.set_page_config(page_title="Manuscript Review Assistant", page_icon="📚")

# Título y descripción
st.title("Manuscript Review Assistant")
st.write("""
Welcome to the Manuscript Review Assistant! This tool helps authors determine if their manuscript meets the guidelines of top management journals. 
Upload your manuscript, select the target journal, and receive personalized feedback.
""")

# Menú en la barra lateral para seleccionar la revista
st.sidebar.header("Select a Journal")
journal = st.sidebar.selectbox(
    "Choose the journal you are targeting:",
    [
        "Academy of Management Journal (AMJ)",
        "Administrative Science Quarterly (ASQ)",
        "Strategic Management Journal (SMJ)",
        "Journal of Management (JOM)",
        "Organization Science"
    ]
)

# Cargar archivo Word
uploaded_file = st.file_uploader("Upload your manuscript (Word file)", type=["docx"])
if uploaded_file:
    st.success("File uploaded successfully!")
    document = Document(uploaded_file)
    
    # Extraer texto del manuscrito
    manuscript_text = "\n".join([para.text for para in document.paragraphs])
    st.subheader("Manuscript Preview")
    st.text_area("Manuscript Content", manuscript_text, height=300)

    # Verificar formato básico
    def check_format(text):
        word_count = len(re.findall(r'\w+', text))
        pages_estimate = word_count / 250  # Estimación: 250 palabras por página
        return {
            "word_count": word_count,
            "pages_estimate": pages_estimate
        }

    format_info = check_format(manuscript_text)

    # Feedback general
    st.subheader("General Feedback")
    st.write(f"- Estimated word count: **{format_info['word_count']}**")
    st.write(f"- Estimated page count: **{format_info['pages_estimate']:.1f} pages**")

    # Evaluar según la revista seleccionada
    if st.button("Evaluate Manuscript"):
        st.subheader(f"Evaluation for {journal}")
        if journal == "Academy of Management Journal (AMJ)":
            st.write("""
- **Focus and Scope**: Your manuscript should address topics like organizational behavior, leadership, strategy, HR, innovation, or entrepreneurship.
- **Abstract**: Should be ≤ 150 words. Check if your abstract is concise and highlights the research problem, methods, findings, and contributions.
- **Length**: Maximum 40 pages. Your manuscript is estimated to be **{format_info['pages_estimate']:.1f} pages**.
            """.format(format_info=format_info))
            if format_info['pages_estimate'] > 40:
                st.warning("Your manuscript exceeds the recommended length. Consider reducing content.")

        elif journal == "Administrative Science Quarterly (ASQ)":
            st.write("""
- **Focus and Scope**: Your manuscript should offer interdisciplinary insights into organizational behavior, institutional dynamics, or organizational theory.
- **Abstract**: Should be ≤ 150 words. Ensure it captures attention and explains the relevance of your research.
- **Length**: Maximum 40 pages. Your manuscript is estimated to be **{format_info['pages_estimate']:.1f} pages**.
            """.format(format_info=format_info))
            if format_info['pages_estimate'] > 40:
                st.warning("Your manuscript exceeds the recommended length. Consider revising.")

        elif journal == "Strategic Management Journal (SMJ)":
            st.write("""
- **Focus and Scope**: Your manuscript should advance knowledge in business strategy, competitive advantage, or strategic management.
- **Abstract**: Should be ≤ 200 words. Ensure it defines the research problem and its importance.
- **Length**: Maximum 40 pages. Your manuscript is estimated to be **{format_info['pages_estimate']:.1f} pages**.
            """.format(format_info=format_info))
            if format_info['pages_estimate'] > 40:
                st.warning("Your manuscript exceeds the recommended length. Consider condensing content.")

        elif journal == "Journal of Management (JOM)":
            st.write("""
- **Focus and Scope**: Your manuscript should address topics like organizational behavior, leadership, HR, or entrepreneurship.
- **Abstract**: Should be ≤ 200 words. Ensure it clearly states the research problem and its significance.
- **Length**: Maximum 40 pages. Your manuscript is estimated to be **{format_info['pages_estimate']:.1f} pages**.
            """.format(format_info=format_info))
            if format_info['pages_estimate'] > 40:
                st.warning("Your manuscript exceeds the recommended length. Consider editing for brevity.")

        elif journal == "Organization Science":
            st.write("""
- **Focus and Scope**: Your manuscript should contribute to interdisciplinary research on organizational science, including design, culture, innovation, or group dynamics.
- **Abstract**: Should be ≤ 200 words. Ensure it defines the research problem and its importance.
- **Length**: Maximum 40 pages. Your manuscript is estimated to be **{format_info['pages_estimate']:.1f} pages**.
            """.format(format_info=format_info))
            if format_info['pages_estimate'] > 40:
                st.warning("Your manuscript exceeds the recommended length. Consider revising.")

        # Feedback adicional
        st.subheader("Additional Suggestions")
        st.write("""
- **Abstract**: Ensure it is clear, concise, and highlights the key contributions of your research.
- **Keywords**: Include 3–5 relevant keywords that reflect the core themes of your manuscript.
- **Formatting**: Use Times New Roman, size 12, double-spaced, with 1-inch margins.
- **References**: Follow APA (7th edition) style for citations and references.
        """)

# Recursos adicionales
st.sidebar.header("Additional Resources")
st.sidebar.write("""
For more details, visit the official websites of the respective journals:
- [AMJ](https://journals.aom.org/amj)
- [ASQ](https://journals.sagepub.com/home/asq)
- [SMJ](https://onlinelibrary.wiley.com/journal/10970266)
- [JOM](https://journals.sagepub.com/home/jom)
- [Organization Science](https://pubsonline.informs.org/journal/orgsci)
""")
