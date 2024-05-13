FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install daphne

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8002 available to the world outside this container
EXPOSE 8002

# Command to run Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8002", "backend.asgi:application"]
