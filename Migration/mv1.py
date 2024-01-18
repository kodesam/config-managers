import openai
import re

# Set up OpenAI API key
openai.api_key = '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'

def generate_ansible_script():
    tasks = """
- name: Migrate VM from AWS to Azure
  hosts: localhost
  gather_facts: no

  tasks:
    - name: Fetch AWS Instance details
      ec2_instance_info:
        filters:
          "tag:Name": "YOUR_AWS_INSTANCE_NAME"
          "instance-state-name": "running"
      register: aws_instance

    - name: Generate Azure VM configuration using AWS instance details
      azure_rm_virtualmachine:
        resource_group: YOUR_AZURE_RESOURCE_GROUP_NAME
        name: YOUR_AZURE_VM_NAME
        ...
        # Add your Azure VM configuration details here
        ...

    - name: Start Azure VM
      azure_rm_virtualmachine:
        resource_group: YOUR_AZURE_RESOURCE_GROUP_NAME
        name: YOUR_AZURE_VM_NAME
        state: started

    - name: Stop AWS EC2 Instance
      ec2:
        instance_ids: "{{ aws_instance.instances[0].id }}"
        state: stopped
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

ansible_script = generate_ansible_script()

with open("migration_tasks.yml", "w") as file:
    file.write(ansible_script)

print("Ansible tasks for VM migration generated successfully.")