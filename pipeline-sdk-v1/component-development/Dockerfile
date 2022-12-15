# The base container image
FROM python:3.7

# Any dependencies that need to be installed for your code to run.
RUN python3 -m pip install keras

# Files to copy into the container, such as the runnable code for this component.
COPY ./src /pipelines/component/src