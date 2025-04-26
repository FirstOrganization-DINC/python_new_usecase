# 1. Use an official lightweight Python image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy your project files into the container
COPY . /app

# 4. Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# 5. Expose the port Flask will run on
EXPOSE 5000

# 6. Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
