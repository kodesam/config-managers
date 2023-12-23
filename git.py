from github import Github

# GitHub personal access tokens for both repositories
source_token = "I"
target_token = ""

# Names of the source and target repositories
source_owner = "kodesam"
source_repo_name = "collection-b-runbooks"
target_owner = "kodesam"
target_repo_name = "codespace-pipeline"

# Path and filename of the file to be copied
file_path = "ansible/kubectl get nodes.yaml"
new_file_path = "kubectl get nodes.yaml"

# Execute button
execute = st.sidebar.button("Execute")

if execute:
try:
    # Create instances of the source and target repositories
    source_repo = Github(source_token).get_repo(f"{source_owner}/{source_repo_name}")
    target_repo = Github(target_token).get_repo(f"{target_owner}/{target_repo_name}")

    # Get the content of the file in the source repository
    file_content = source_repo.get_contents(file_path).content

    # Create the file in the target repository
    target_repo.create_file(new_file_path, "Copying file", file_content, branch="main")

    print(f"File '{file_path}' copied to '{new_file_path}' in the target repository successfully.")

except Exception as e:
    print(f"An error occurred while copying the file: {str(e)}")