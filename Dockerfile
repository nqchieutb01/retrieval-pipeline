# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

EXPOSE 8889

# RUN chmod +x standalone_embed.sh

# Run the application

# CMD ["python3", "test.py"]
CMD ["python3", "-m", "app.main"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8889"]

# Keep the container running
# ENTRYPOINT ["tail", "-f", "/dev/null"]

# uvicorn app.main:app --host 0.0.0.0 --port 8889

