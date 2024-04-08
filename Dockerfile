
FROM python:3.12.1

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /referral_system

# Set the working directory to /music_service
WORKDIR /referral_system

# Copy the current directory contents into the container at /music_service
ADD . /referral_system/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

