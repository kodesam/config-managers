import streamlit as st
import random
import re
import time
import os
from openai import AzureOpenAI
from openai._exceptions import APIError, APIConnectionError, RateLimitError

# Configure sensitive patterns and replacements
SENSITIVE_PATTERNS = {
    r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b": 'IP_ADDRESS="XXX.XXX.XXX.XXX"',
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b": 'EMAIL="***@***.com"',
    r"\b(?:\d{4}-?){3}\d{4}\b": 'CREDIT_CARD="****-****-****-****"',
    r"\b\d{3}-\d{2}-\d{4}\b": 'SSN="***-**-****"',
}

SENSITIVE_KEYWORDS = ["token", "password", "secret", "api key", "credentials"]

def filter_sensitive_content(prompt):
    """Filter and mask sensitive information in the prompt"""
    masked_prompt = prompt
    for pattern, replacement in SENSITIVE_PATTERNS.items():
        masked_prompt = re.sub(pattern, replacement, masked_prompt, flags=re.IGNORECASE)
    
    if any(keyword in masked_prompt.lower() for keyword in SENSITIVE_KEYWORDS):
        return None
    
    return masked_prompt if masked_prompt != prompt else prompt

# Streamlit UI Configuration
st.set_page_config(page_title="Config-Manager AI", page_icon="🚀⚙️ ")
title_style = "color: #87CEEB; font-weight: bold;"
st.markdown(f"<h1 style='{title_style}'>⚙️ ⚙️  Config-Manager AI ⚙️ ⚙️ </h1>", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi I am Configma AI !! How can I assist you with script/Configuration generation today?"}]
if "current_config" not in st.session_state:
    st.session_state.current_config = None

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ AI Config Manager")
    
    openai_api_key = st.text_input("Azure OpenAI API Key", type="password")
    
    # Load Ansible modules from file with error handling
    try:
        with open("/home/ec2-user/config-managers-main/lib/Module/ansible_module.txt") as f:
            ansible_modules = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        st.error("⚠️ Module list not found at 'lib/Module/module.txt'")
        ansible_modules = ["file", "copy", "template"]  # Default fallback
    except Exception as e:
        st.error(f"Error loading modules: {str(e)}")
        ansible_modules = ["file", "copy", "template"]

    modules = {
        "Infrastructure": ["terraform", "cloudformation"],
        "Orchestration": ["ansible", "kubernetes", "openshift"],
        "Scripting": ["shell", "powerShell"],
        "Code generation": ["python", "python notebook"],
        "Container image": ["Docker file", "Podman file"],
        "Conversion": ["csv to json", "json to csv", "json to yaml", "yaml to json"],
        "Security": ["iam_policy", "security_group"],
        "Error Correction": ["validate_config"],
        "Advance Ansible Modules": ansible_modules  # New module list from file
    }
    
    selected_module = st.selectbox("Configuration Type", list(modules.keys()))
    sub_module = st.selectbox("Subtype", modules[selected_module])
    
    env_options = ["dev", "stage", "prod"]
    selected_env = st.selectbox("Environment", env_options)
    
    compliance_options = st.multiselect(
        "Compliance Standards",
        ["CIS AWS", "PCI-DSS", "HIPAA", "GDPR"]
    )
    
    with st.expander("Advanced Settings"):
        model_choice = st.selectbox(
            "AI Model",
            ["gpt-4o-mini"],
            index=0
        )
        max_tokens = st.slider("Max Tokens", 100, 2000, 500)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3)

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Modified documentation generation section
if st.session_state.current_config:
    if st.button("📄 Generate Documentation"):
        try:
            if not openai_api_key:
                st.error("🔑 Please enter your Azure OpenAI API key in the sidebar")
                st.stop()

            client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://codedocumentation.openai.azure.com/"),
                api_key=openai_api_key,
                api_version="2024-02-15-preview"
            )

            doc_prompt = f"""
            Generate comprehensive documentation in Markdown (.md) format for this {sub_module} configuration:
            ```{sub_module.split()[-1]}
            {st.session_state.current_config}
            ```
            
            **Required Sections:**
            1. `## Configuration Overview`
            2. `## Environment Details` (with **{selected_env}** environment specifics)
            3. `## Compliance Standards` (formatted as table)
            4. `## Security Best Practices`
            5. `## Deployment Workflow`
            6. `## Monitoring & Logging`
            7. `## Troubleshooting Guide`
            8. `## Version History`

            **Formatting Requirements:**
            - Use proper Markdown syntax
            - Configuration examples in code blocks with language specification
            - Tables for compliance standards and environment details
            - Bullet points for lists
            - Links to official documentation where applicable
            - Highlight important notes with `> **Note**` blocks
            """

            with st.spinner("Generating Markdown documentation..."):
                doc_response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": """You are a technical documentation specialist. 
                        Create professional Markdown documentation with proper formatting, tables, and code blocks.
                        Ensure compliance with technical writing standards and markdownlint rules."""},
                        {"role": "user", "content": doc_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000,
                    top_p=0.9
                )

            docs = doc_response.choices[0].message.content
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📄 **Configuration Documentation**\n\n{docs}"
            })
            st.session_state.current_config = None
            st.rerun()

        except Exception as e:
            error_msg = f"⚠️ Documentation generation failed: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

# ... (rest of the code remains the same until footer)

# Update footer version
st.sidebar.caption("v2.2.0 | Enterprise AI Config Manager")
# Chat input processing
if prompt := st.chat_input("Describe your configuration needs..."):
    # Validate API key
    if not openai_api_key:
        st.error("🔑 Please enter your Azure OpenAI API key in the sidebar")
        st.stop()
    
    # Input validation
    if len(prompt) > 1000:
        st.warning("Input exceeds maximum length of 1000 characters. Please shorten your message.")
        st.stop()
    
    # Content filtering
    filtered_prompt = filter_sensitive_content(prompt)
    if not filtered_prompt:
        st.warning("Input contains sensitive content. Please revise and try again.")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": filtered_prompt})
    st.chat_message("user").write(filtered_prompt)

    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://codedocumentation.openai.azure.com/"),
            api_key=openai_api_key,
            api_version="2024-02-15-preview"
        )

        # Create system message with context
        system_context = f"""
        Generate {selected_module} configuration for {sub_module} in {selected_env} environment.
        Compliance requirements: {', '.join(compliance_options) if compliance_options else 'None'}.
        Provide secure, production-ready configuration with detailed comments.
        """
        
        # Prepare messages for API
        context_messages = [
            {"role": "system", "content": system_context},
            *st.session_state.messages
        ]

        # API call with retry logic
        max_retries = 3
        response = None
        
        for attempt in range(max_retries):
            try:
                with st.spinner(f"Generating response (attempt {attempt+1}/{max_retries})..."):
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=context_messages,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    break
            except (APIConnectionError, RateLimitError) as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff

        # Validate response
        if not response or not response.choices:
            raise APIError("Received empty response from the API")
        
        msg = response.choices[0].message.content
        st.session_state.current_config = msg  # Store generated configuration
        
        if not msg.strip():
            raise ValueError("Empty response generated by the model")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()

    except (APIError, APIConnectionError, RateLimitError) as e:
        error_msg = f"⚠️ API Error: {str(e)}. Please try again later."
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.rerun()
        
    except Exception as e:
        error_msg = f"⚠️ Unexpected error: {str(e)}. Please contact support."
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.rerun()

# Add footer with additional information
st.sidebar.markdown("---")
st.sidebar.caption(f"Session ID: {random.randint(10000, 99999)}")
st.sidebar.caption("v2.1.0 | Enterprise AI Config Manager")
