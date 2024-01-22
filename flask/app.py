from flask import Flask, render_template, request
from github import Github, GithubException
from openai import ChatCompletion
import openai
import random
import re

app = Flask(__name__,template_folder='.')
openai_api_key = "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"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        repo_owner = request.form['repo_owner']
        repo_name = request.form['repo_name']
        folder_path = request.form['folder_path']
        branch_name = request.form['branch_name']
        
        # Filter sensitive content in the prompt
        filtered_prompt = filter_sensitive_content(prompt)
        
        if not filtered_prompt:
            return "Error: The prompt contains sensitive content. Please remove any sensitive information."
        
        # Get the response from OpenAI Chat API
        response = get_openai_response(filtered_prompt)
        msg = response.choices[0].message.content
        
        # Generate a random number
        random_number = random.randint(1, 1000)
        
        # Update the filename
        base_filename = "code"
        filename = f"{base_filename}_{random_number}.yaml"
        
        try:
            # Create a connection to the GitHub repository
            g = Github("YOUR_GITHUB_ACCESS_TOKEN")
            repo = g.get_repo(f"{repo_owner}/{repo_name}")

            # Check if the file already exists in the folder
            file_path = f"{folder_path}/{filename}"
            file_exists = True

            try:
                repo.get_contents(file_path, ref=branch_name)
            except GithubException as e:
                if e.status == 404:
                    file_exists = False
                else:
                    raise

            if not file_exists:
                # Create or update the file in the repository
                content = msg
                commit_message = f"Create {filtered_prompt}"
                repo.create_file(file_path, commit_message, content, branch=branch_name)
                return f"Success: File '{filename}' created successfully in the GitHub repository."
            else:
                return f"Error: File '{filename}' already exists in the GitHub repository. Skipping creation."
        except AssertionError as e:
            return "Error: An error occurred while creating the file. Please try again later."
        except GithubException as e:
            return "Error: File already exists in GitHub Repository folder."
        
    return render_template('index.html')

def filter_sensitive_content(prompt):
    # Perform the necessary filtering operations or checks here
    # You can use regex, NLP techniques, or other methods to identify and mask sensitive content
    
    # Example: Check if prompt contains IP address and mask it
    ip_address_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"  # Regex pattern for IP address
    masked_prompt = re.sub(ip_address_pattern, 'IP ADDRESS="XXX.XXX.XXX.XXX"', prompt)
    
    if masked_prompt != prompt:
        return masked_prompt  # Return the masked prompt if it contains sensitive content
    
    # Check if additional instruction contains any of the sensitive keywords
    sensitive_keywords = ["password", "secret", "token", "nokia"]
    additional_instruction_lower = prompt.lower()  # Convert additional instruction to lowercase
    
    for keyword in sensitive_keywords:
        keyword_lower = keyword.lower()  # Convert keyword to lowercase
        if keyword_lower in additional_instruction_lower:
            return None  # Return None if the additional instruction contains sensitive content
    
    return prompt  # Return the filtered prompt if it doesn't contain sensitive content

def get_openai_response(prompt):
    openai.api_key = openai_api_key
    messages = [
        {"role": "system", "content": "You are a chat-based assistant that helps generate code."},
        {"role": "user", "content": prompt},
    ]
    response = openai.Completion.create(
        engine="gpt-3.5-turbo", 
        messages=messages,
    )
    return response

if __name__ == '__main__':
    app.run()