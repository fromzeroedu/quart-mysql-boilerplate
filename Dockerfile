FROM python:3.7.3-slim

# Install pipenv
RUN pip install pipenv

# Make a local directory
RUN mkdir /counter_app

# Set "counter_app" as the working directory from which CMD, RUN, ADD references
WORKDIR /counter_app

# Now copy all the files in this directory to /counter_app
ADD . .

# Install pipenv
RUN pipenv install

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD pipenv run quart run --host 0.0.0.0
