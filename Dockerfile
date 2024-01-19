# Use an official Ubuntu runtime as a parent image with Python 3
FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y python3-pip python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . /app

# Install any dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the training script to train the model and save artifacts
RUN python3 src/pipelines/training_pipeline.py

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]
