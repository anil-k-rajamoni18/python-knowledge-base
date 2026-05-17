# step 1 - Use an official Python runtime as a parent image
FROM python:3.11-slim

# step 2 - Set the working directory in the container
WORKDIR /app

# step 3 - Copy the requirements file into the container at /app
COPY requirements.txt /app/


# step 4 - Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# step 5 - Copy the current directory contents into the container at /app
COPY . /app/

# step 6 - Make port 8000 available to the world outside this container
EXPOSE 8000

# step 7 - Define environment variables
ENV PYTHONUNBUFFERED=1

# step 8 - Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]