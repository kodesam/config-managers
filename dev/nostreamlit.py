from github import Github
from openai import OpenAI
import random

# Get available models
available_models = ['gpt-3.5-turbo-16k-0613','gpt-3.5-turbo-16k-1106','gpt-3.5-turbo', 'gpt-3.5', 'gpt-3.0']

# Set OpenAI API key
openai_api_key = "<YOUR_OPENAI_API_KEY>"

# Set GitHub credentials
github_token = "<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>"
repo_owner = "<GITHUB_REPO_OWNER>"
repo_name = "<GITHUB_REPO_NAME>"
folder_path = "<FOLDER_PATH>"
branch_name = "main"  # Set the desired branch name

# Set the prompt
prompt = "User input goes here"

# Set the instruction
instruction_1 = "Selected module instruction"

# Set the additional instruction
instruction_2 = "Additional instructions go here"

# Connect to OpenAI
client = OpenAI(api_key=openai_api_key)

# Create a conversation with assistant messages
messages = [
    {"role": "system", "content": "You are a user"},
    {"role": "user", "content": prompt},
    {"role": "assistant", "content": instruction_1},
    {"role": "assistant", "content": instruction_2}
]

# Include the instruction in the API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Extract the assistant's response
msg = response.choices[0].message.content

# Generate a random number
random_number = random.randint(1, 1000)

# Update the filename
base_filename = "code"
filename = f"{base_filename}_{random_number}.yaml"

# Create a connection to the GitHub repository
g = Github(github_token)
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# Check if the file already exists in the folder
file_path = f"{repo_owner}/{repo_name}/{folder_path}/{filename}"
file_exists = True

try:
    repo.get_contents(file_path, ref=branch_name)
except Exception as e:
    if e.status == 404:
        file_exists = False
    else:
        raise

if not file_exists:
    # Create or update the file in the repository
    content = msg
    commit_message = f"Create {prompt}"
    repo.create_file(file_path, commit_message, content, branch=branch_name)
    print(f"File '{filename}' created successfully in the GitHub repository.")
else:
    print(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")
