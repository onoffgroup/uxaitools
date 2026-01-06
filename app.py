import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="GetUXCertified AI Tools", page_icon="🎓")

# Sidebar for Context
with st.sidebar:
    st.header("About")
    st.write("This tool generates standard UX documents for students.")
    st.warning("⚠️ Do not enter real names or phone numbers (PII).")

# API Setup (Securely pulls from Streamlit Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
except:
    st.error("API Key not found. Please check your secrets settings.")
    st.stop()

# Main Interface
st.title("UX Research Assistant 🤖")

tool_type = st.selectbox("What do you want to generate?", 
    [
        "Screener Survey", 
        "Informed Consent Form", 
        "Usability Test Script", 
        "User Persona Draft"
    ]
)

project_details = st.text_area("Describe your project (e.g., 'A mobile wallet app for elderly users in Manila')", height=150)

if st.button("Generate Draft"):
    if not project_details:
        st.error("Please describe your project first.")
    else:
        # The System Prompt acts as the guardrail
        system_instruction = f"""
        You are an expert Senior UX Researcher and instructor at GetUXCertified.
        Your goal is to write a professional {tool_type}.
        
        Rules:
        1. Use clear, professional language.
        2. Include placeholders like [Date] or [Participant Name] where needed.
        3. If writing a Screener, ensure questions are behavioral and not leading.
        4. If writing a Consent Form, ensure it mentions data privacy.
        
        Context: {project_details}
        """
        
        with st.spinner("Drafting your document..."):
            try:
                response = model.generate_content(system_instruction)
                st.markdown("### Your Draft")
                st.markdown(response.text)
                st.success("Don't forget to review this before using it!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")