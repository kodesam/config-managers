import streamlit as st
from github import Github, GithubException
import openai
import random
import re
import json
from datetime import datetime
from transformers import pipeline

# Local AI example using Hugging Face
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')
print(generator("Generate config for:", max_length=100))

class ConfigManager:
    def __init__(self, api_key):
        self.ai_client = openai.ChatCompletion(api_key=api_key)
        self.github = None
        self.validation_rules = self.load_compliance_rules()
        
    def load_compliance_rules(self):
        return {
            'security': ['encryption', 'tls', 'access_control'],
            'cis_benchmarks': {
                'aws': ['CIS.1.1', 'CIS.1.2'],
                'azure': ['AZURE.1.1']
            }
        }
    
    def generate_config(self, prompt, context):
        enriched_prompt = self._enrich_prompt(prompt, context)
        response = self.ai_client.create(
            model=context['model'],
            messages=[{"role": "user", "content": enriched_prompt}],
            temperature=context.get('temperature', 0.5)
        )
        return response.choices[0].message.content
    
    def _enrich_prompt(self, prompt, context):
        base_prompt = f"Generate {context['module']} configuration with these requirements:\n{prompt}\n"
        if context.get('environment'):
            base_prompt += f"\nEnvironment: {context['environment']}\n"
        if context.get('compliance'):
            base_prompt += f"\nMust comply with: {', '.join(context['compliance'])}\n"
        return base_prompt
    
    def validate_config(self, config, standards):
        validation_prompt = f"Validate this configuration against {standards}:\n{config}\n\n"
        validation_prompt += "Identify:\n1. Security risks\n2. Compliance violations\n3. Best practice issues\n"
        validation_prompt += "Format response as JSON with keys: 'issues', 'severity', 'recommendations'"
        
        response = self.ai_client.create(
            model="gpt-4",
            messages=[{"role": "user", "content": validation_prompt}],
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    
    def generate_documentation(self, config):
        doc_prompt = f"Generate comprehensive documentation for this configuration:\n{config}\n\n"
        doc_prompt += "Include:\n1. Architecture diagram description\n2. Security considerations\n3. Deployment steps"
        return self.ai_client.create(
            model="gpt-4",
            messages=[{"role": "user", "content": doc_prompt}],
            temperature=0.3
        ).choices[0].message.content

class ConfigUI:
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "config_history" not in st.session_state:
            st.session_state.config_history = {}
        if "current_config" not in st.session_state:
            st.session_state.current_config = ""
            
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
    
    def render_chat_interface(self, manager):
        st.header("AI Configuration Generator")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.chat_input("Describe your configuration needs...")
        
        with col2:
            if st.button("Generate Documentation"):
                if st.session_state.current_config:
                    docs = manager.generate_documentation(st.session_state.current_config)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"📚 Documentation:\n{docs}"
                    })
        
        if user_input:
            self.process_user_input(user_input, manager)
            
        for msg in st.session_state.messages:
            self.display_message(msg)
    
    def process_user_input(self, user_input, manager):
        context = {
            "module": st.session_state.get("module", "terraform"),
            "environment": st.session_state.get("environment", "dev"),
            "compliance": st.session_state.get("compliance", []),
            "model": st.session_state.get("model", "gpt-4"),
            "temperature": st.session_state.get("temperature", 0.3)
        }
        
        try:
            config = manager.generate_config(user_input, context)
            validation = manager.validate_config(config, context['compliance'])
            
            st.session_state.current_config = config
            st.session_state.config_history[datetime.now().isoformat()] = {
                "config": config,
                "validation": validation
            }
            
            st.session_state.messages.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": f"Generated Config:\n```\n{config}\n```"},
                {"role": "assistant", "content": f"Validation Results:\n{self.format_validation(validation)}"}
            ])
            
        except openai.error.OpenAIError as e:
            st.error(f"AI Error: {str(e)}")
    
    def format_validation(self, results):
        return "\n".join([
            f"⚠️ {issue['severity'].upper()}: {issue['description']}\n🛠️ Fix: {issue['recommendation']}"
            for issue in results.get('issues', [])
        ])
    
    def display_message(self, msg):
        with st.chat_message(msg["role"]):
            content = msg["content"]
            if "```" in content:
                st.code(content.split("```")[1])
            else:
                st.markdown(content)

class GitHubIntegration:
    def __init__(self, token):
        self.client = Github(token)
        
    def save_to_repo(self, repo_info, config):
        try:
            repo = self.client.get_repo(f"{repo_info['owner']}/{repo_info['name']}")
            branch = repo_info.get('branch', 'main')
            path = f"{repo_info['path']}/{self.generate_filename(repo_info['type'])}"
            
            commit_msg = f"AI-generated {repo_info['type']} config for {repo_info['environment']}"
            repo.create_file(path, commit_msg, config, branch=branch)
            return True
        except GithubException as e:
            st.error(f"GitHub Error: {str(e)}")
            return False
    
    def generate_filename(self, config_type):
        types = {
            "terraform": "main.tf",
            "ansible": "playbook.yml",
            "kubernetes": "deployment.yaml"
        }
        return types.get(config_type, "configuration.txt")

def main():
    ui = ConfigUI()
    context = ui.render_sidebar()
    
    if not context['api_key']:
        st.info("🔑 Please enter your OpenAI API key to continue")
        return
    
    manager = ConfigManager(context['api_key'])
    ui.render_chat_interface(manager)
    
    st.sidebar.header("Version Control")
    gh_token = st.sidebar.text_input("GitHub Token", type="password")
    if gh_token and st.session_state.current_config:
        gh_info = {
            "owner": st.sidebar.text_input("Repo Owner"),
            "name": st.sidebar.text_input("Repo Name"),
            "path": st.sidebar.text_input("Folder Path", "configs"),
            "branch": st.sidebar.text_input("Branch", "main"),
            "type": context['module'].split(" ")[0],
            "environment": context['environment']
        }
        
        if st.sidebar.button("💾 Save to GitHub"):
            gh = GitHubIntegration(gh_token)
            if gh.save_to_repo(gh_info, st.session_state.current_config):
                st.success("✅ Configuration saved to GitHub!")

if __name__ == "__main__":
    main()
