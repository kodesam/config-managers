import streamlit as st
from github import Github, GithubException
from openai import AzureOpenAI
import random
import re
import json
import hashlib
from datetime import datetime

class ConfigManager:
    def __init__(self, api_key):
        self.ai_client = AzureOpenAI(
            azure_endpoint="https://codedocumentation.openai.azure.com/",
            api_key=api_key,
            api_version="2024-02-15-preview"
        )
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
        response = self.ai_client.chat.completions.create(
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
        
        response = self.ai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": validation_prompt}],
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    
    def generate_documentation(self, config):
        doc_prompt = f"Generate comprehensive documentation for this configuration:\n{config}\n\n"
        doc_prompt += "Include:\n1. Architecture diagram description\n2. Security considerations\n3. Deployment steps"
        return self.ai_client.chat.completions.create(
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
            openai_api_key = st.text_input("Azure OpenAI API Key", type="password")
            
            modules = {
                "Infrastructure": ["terraform", "cloudformation"],
                "Orchestration": ["ansible", "kubernetes", "openshift"],
                "Scripting": ["shell", "powerShell"],
                "Code generation": ["python", "python notebook"],
                "container image": ["Docker file", "Podman file"],
                "Convertion": ["csv - json", "json - csv", "json - yaml", "yaml - json"],
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

    # Remaining ConfigUI methods unchanged...

class GitHubIntegration:
    def __init__(self, token):
        self.client = Github(token)
        
    def generate_hash(self, content):
        return hashlib.sha256(content.encode()).hexdigest()
        
    def save_to_repo(self, repo_info, config):
        try:
            repo = self.client.get_repo(f"{repo_info['owner']}/{repo_info['name']}")
            branch = repo_info.get('branch', 'main')
            path = f"{repo_info['path']}/{self.generate_filename(repo_info['type'])}"
            
            # Generate content hash
            config_hash = self.generate_hash(config)
            commit_msg = f"AI-generated {repo_info['type']} config for {repo_info['environment']}\nHash: {config_hash}"
            
            # Save both config and hash file
            repo.create_file(path, commit_msg, config, branch=branch)
            repo.create_file(f"{path}.sha256", commit_msg, config_hash, branch=branch)
            
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

# Main function remains unchanged...
