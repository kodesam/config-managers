# Build the Docker image: Open a terminal in the directory where your Dockerfile and requirements.txt files are located. Run the following command to build the Docker image:

```docker build -t blue_runbook_ai:latest . ```

This command will build the Docker image and tag it with the name blue_runbook_ai and the latest tag.

Run the Docker container: Once the image is built, you can run a Docker container using the following command:

``` docker run -p 8501:8501 blue_runbook_ai:latest ```

This command maps port 8501 (used by Streamlit) from the container to port 8501 on the host machine.

Access the Streamlit app: Open a web browser and visit ```http://localhost:8501``` to access the Streamlit app running inside the Docker container.
