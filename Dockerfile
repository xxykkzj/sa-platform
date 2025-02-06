FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the Docker container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y

# Copy the Python requirements file into the container at /app
COPY ./requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install browsers for playwright
RUN playwright install --with-deps chromium

COPY . /app/

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
