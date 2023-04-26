#use an official python runtime
FROM python:3.8-slim-buster

#Set the working directory 
WORKDIR /app

#Copy the code base in the current directory to the container /app
COPY . /app

#Upgrade PIP
RUN pip install --upgrade pip

#Install any needed packages
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install pygal

#Set the default command to run when starting the container 
CMD ["python", "app.py"]