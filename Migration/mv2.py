import openai
import re

# Set up OpenAI API key
openai.api_key = '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'

def generate_ansible_script(source_instance, destination_instance):
    tasks = f"""
- name: Migrate VM from {source_instance} to {destination_instance}
  hosts: localhost
  gather_facts: no

  tasks:
    - name: Stop source VM
      shell: |
        # Commands to stop the source VM in {source_instance}
        echo "Stopping source VM in {source_instance}..."
      register: stop_result
      changed_when: false

    - name: Migrate VM
      shell: |
        # Commands to migrate the VM from {source_instance} to {destination_instance}
        echo "Migrating VM from {source_instance} to {destination_instance}..."
      register: migrate_result
      changed_when: false

    - name: Start destination VM
      shell: |
        # Commands to start the destination VM in {destination_instance}
        echo "Starting destination VM in {destination_instance}..."
      register: start_result
      changed_when: false

    - name: Verify migration
      shell: |
        # Commands to verify the migration
        echo "Verifying VM migration..."
      register: verify_result
      changed_when: false
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": tasks},
        ],
        max_tokens=1500,
        temperature=0.7,
        n=1,
        stop=None
    )

    ansible_script = response['choices'][0]['message']['content']
    ansible_script = re.sub(r"([^\n])\n([^-\s])", r"\1 \2", ansible_script)  # Fix indentation

    return ansible_script

source_instance = input("Enter the name of the source GitHub Codespaces instance: ")
destination_instance = input("Enter the name of the destination GitHub Codespaces instance: ")

ansible_script = generate_ansible_script(source_instance, destination_instance)

with open("migration_tasks.yml", "w") as file:
    file.write(ansible_script)

print("Ansible tasks for VM migration generated successfully.")