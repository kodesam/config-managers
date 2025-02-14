    def render_sidebar(self):
        with st.sidebar:
            st.title("⚙️ AI Config Manager")
            openai_api_key = st.text_input("OpenAI API Key", type="password")
            
            modules = {
                "Infrastructure": ["terraform", "cloudformation"],
                "Orchestration": ["ansible", "kubernetes"],
                "Security": ["iam_policy", "security_group"],
                "Error Correction": ["validate_config"]
            }
            
            selected_module = st.selectbox("Configuration Type", list(modules.keys()))
            sub_module = st.selectbox("Subtype", modules[selected_module])
            
            env_options = ["dev", "stage", "prod"]
            selected_env = st.selectbox("Environment", env_options)
            
            compliance_options = st.multiselect(
                "Compliance Standards",
                ["CIS AWS", "PCI-DSS", "HIPAA", "GDPR"]
            )
            
            # Corrected expander section
            with st.expander("Advanced Settings"):
                model_choice = st.selectbox(
                    "AI Model",
                    ["gpt-4", "gpt-3.5-turbo"],
                    index=0
                )
                temp = st.slider("Creativity", 0.0, 1.0, 0.3)
                
            return {
                "api_key": openai_api_key,
                "module": f"{selected_module} ({sub_module})",
                "environment": selected_env,
                "compliance": compliance_options,
                "model": model_choice,
                "temperature": temp
            }
