from flask import Flask, render_template, request
from github import Github
from openai import OpenAI
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["user_input"]
        instruction_1 = request.form["module_instruction"]
        instruction_2 = request.form["additional_instruction"]
        
        # Set OpenAI API key
        openai_api_key = "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"

        # Set GitHub credentials
        github_token = "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"
        repo_owner = "kodesam"
        repo_name = "collection-b-runbooks"
        folder_path = "linux"
        branch_name = "main"  # Set the desired branch name

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

    return render_template("index.html")

if __name__ == "__main__":
    app.run()