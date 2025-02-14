import streamlit as st
import random
import re
import time
import os
import yaml
import hashlib
from datetime import datetime
from openai import AzureOpenAI
from openai._exceptions import APIError, APIConnectionError, RateLimitError
#api_key="70683718b85747ea89724db4214873e7",
# Set page config FIRST - required by Streamlit
st.set_page_config(
    page_title="Config-Manager AI",
    page_icon="🚀⚙️ ",
    layout="wide"
)

# Security Configuration
CREDENTIALS_FILE = "/home/ec2-user/config-managers-main/pages/auth/credentials.yml"
SESSION_LOG_FILE = "/home/ec2-user/config-managers-main/pages/auth/session.log"
SESSION_TIMEOUT = 1800  # 30 minutes in seconds

# Configure sensitive patterns and replacements
SENSITIVE_PATTERNS = {
    r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b": 'IP_ADDRESS="XXX.XXX.XXX.XXX"',
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b": 'EMAIL="***@***.com"',
    r"\b(?:\d{4}-?){3}\d{4}\b": 'CREDIT_CARD="****-****-****-****"',
    r"\b\d{3}-\d{2}-\d{4}\b": 'SSN="***-**-****"',
}

SENSITIVE_KEYWORDS = ["token", "password", "secret", "api key", "credentials"]

def log_session(action, details=None):
    """Log user activities to session file"""
    try:
        with open(SESSION_LOG_FILE, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "timestamp": timestamp,
                "username": st.session_state.auth.get("username", "unknown"),
                "action": action,
                "details": details
            }
            log_file.write(f"{str(entry)}\n")
    except Exception as e:
        st.error(f"Failed to write session log: {str(e)}")

def filter_sensitive_content(prompt):
    """Filter and mask sensitive information in the prompt"""
    masked_prompt = prompt
    for pattern, replacement in SENSITIVE_PATTERNS.items():
        masked_prompt = re.sub(pattern, replacement, masked_prompt, flags=re.IGNORECASE)
    
    if any(keyword in masked_prompt.lower() for keyword in SENSITIVE_KEYWORDS):
        return None
    
    return masked_prompt if masked_prompt != prompt else prompt

def load_credentials():
    """Load and validate user credentials"""
    try:
        with open(CREDENTIALS_FILE) as file:
            credentials = yaml.safe_load(file)
            if not isinstance(credentials, dict):
                raise ValueError("Invalid credentials format")
            return credentials
    except Exception as e:
        log_session("auth_error", f"Credential load failed: {str(e)}")
        st.error(f"⚠️ Authentication system error: {str(e)}")
        st.stop()

def authenticate(username, password):
    """Authenticate user with hashed password"""
    credentials = load_credentials()
    if username in credentials:
        stored_hash = credentials[username]
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return input_hash == stored_hash
    return False

# Initialize session state
if "auth" not in st.session_state:
    st.session_state.auth = {
        "logged_in": False,
        "username": None,
        "login_time": None
    }

# Show login form if not authenticated
if not st.session_state.auth["logged_in"]:
    st.title("🔐 Config-Manager AI Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if authenticate(username, password):
                st.session_state.auth = {
                    "logged_in": True,
                    "username": username,
                    "login_time": time.time()
                }
                log_session("login_success")
                st.rerun()
            else:
                log_session("login_failed", f"username: {username}")
                st.error("❌ Invalid credentials")

    st.markdown("---")
    st.caption("Contact admin for access credentials")
    st.stop()
else:
    # Session Timeout Check
    if (time.time() - st.session_state.auth["login_time"]) > SESSION_TIMEOUT:
        log_session("session_timeout")
        st.session_state.auth = {"logged_in": False, "username": None}
        st.error("🕒 Session timed out. Please login again")
        st.rerun()

    # Main Application
    title_style = "color: #87CEEB; font-weight: bold;"
    st.markdown(f"<h1 style='{title_style}'> ⚙️ ⚙️  Config-Manager AI ⚙️ ⚙️  </h1>", unsafe_allow_html=True)

    # Logout Button
    with st.sidebar:
        if st.button("🚪 Logout"):
            log_session("logout")
            st.session_state.auth = {"logged_in": False, "username": None}
            st.rerun()
        st.markdown(f"**Logged in as:** {st.session_state.auth['username']}")
        st.markdown("---")


 # API Key Input (MISSING IN PREVIOUS CODE)
        #openai_api_key = st.text_input("Azure OpenAI API Key", type="password")
       

        # Load Ansible modules from file
        try:
            with open("/home/ec2-user/config-managers-main/lib/Module/ansible_module.txt") as f:
                ansible_modules = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            st.error("⚠️ Module list not found")
            ansible_modules = ["file", "copy", "template"]
            log_session("module_load_error", "File not found")
        except Exception as e:
            st.error(f"Error loading modules: {str(e)}")
            ansible_modules = ["file", "copy", "template"]
            log_session("module_load_error", str(e))

        modules = {
            "Infrastructure": ["terraform", "cloudformation"],
            "Orchestration": ["ansible", "kubernetes", "openshift"],
            "Scripting": ["shell", "powerShell","ansible jinja template"],
            "Code generation": ["python", "python notebook"],
            "Container image": ["Docker file", "Podman file"],
            "Conversion": ["csv to json", "json to csv", "json to yaml", "yaml to json"],
            "Security": ["iam_policy", "security_group"],
            "Error Correction": ["validate_config"],
            " Advance Ansible Modules": ansible_modules
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

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello I am Configma assistant, How can I assist you with script generation today?"}]
    if "current_config" not in st.session_state:
        st.session_state.current_config = None

    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Documentation generation button
    if st.session_state.current_config:
        if st.button("📄 Generate Documentation"):
            try:
                client = AzureOpenAI(
                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://codedocumentation.openai.azure.com/"),
                    api_key=openai_api_key,
                    api_version="2024-02-15-preview"
                )

                doc_prompt = f"""
                Generate comprehensive documentation for this {sub_module} configuration:
                {st.session_state.current_config}
                """
                
                with st.spinner("Generating documentation..."):
                    doc_response = client.chat.completions.create(
                        model=model_choice,
                        messages=[
                            {"role": "system", "content": "You are a senior DevOps engineer"},
                            {"role": "user", "content": doc_prompt}
                        ],
                        temperature=0.2,
                        max_tokens=1500
                    )

                docs = doc_response.choices[0].message.content
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"📚 Documentation:\n{docs}"
                })
                log_session("doc_generated", f"module: {sub_module}")
                st.session_state.current_config = None
                st.rerun()

            except Exception as e:
                error_msg = f"⚠️ Documentation generation failed: {str(e)}"
                log_session("doc_error", str(e))
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()

    # Chat input processing
    if prompt := st.chat_input("Describe your configuration needs..."):
        log_session("config_request", f"module: {sub_module}")
        
        if not openai_api_key:
            st.error("🔑 Please enter your Azure OpenAI API key in the sidebar")
            st.stop()
        
        if len(prompt) > 1000:
            st.warning("Input exceeds maximum length of 1000 characters")
            st.stop()
        
        filtered_prompt = filter_sensitive_content(prompt)
        if not filtered_prompt:
            st.warning("Input contains sensitive content")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": filtered_prompt})
        st.chat_message("user").write(filtered_prompt)

        try:
            client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://codedocumentation.openai.azure.com/"),
                api_key=openai_api_key,
                api_version="2024-02-15-preview"
            )

            system_context = f"""
            Generate {selected_module} configuration for {sub_module} in {selected_env} environment.
            Compliance requirements: {', '.join(compliance_options) if compliance_options else 'None'}.
            Provide secure, production-ready configuration with detailed comments.
            """
            
            context_messages = [
                {"role": "system", "content": system_context},
                *st.session_state.messages
            ]

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
                    time.sleep(2 ** attempt)

            if not response or not response.choices:
                raise APIError("Empty API response")
            
            msg = response.choices[0].message.content
            st.session_state.current_config = msg
            
            if not msg.strip():
                raise ValueError("Empty response")

            st.session_state.messages.append({"role": "assistant", "content": msg})
            log_session("config_generated", f"module: {sub_module}")
            st.rerun()

        except (APIError, APIConnectionError, RateLimitError) as e:
            error_msg = f"⚠️ API Error: {str(e)}"
            log_session("api_error", str(e))
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()
            
        except Exception as e:
            error_msg = f"⚠️ Unexpected error: {str(e)}"
            log_session("system_error", str(e))
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Session ID: {random.randint(10000, 99999)}")
    st.sidebar.caption("v2.5.0 | Enterprise AI Config Manager")
