FROM tiangolo/uwsgi-nginx-flask-docker:python3.7


# Create the workspace
WORKDIR /app
RUN mkdir /app/output
COPY . .


# Install the pip dependencies
RUN pip install -r /app/requiments.txt


# Train the model
COPY train.py /app/
RUN python3 train.py
COPY /app/output ./output


# Run the production in app
ENV ENVIROMENT PRODUCTION
COPY predict.py /app/
RUN python3 predict.py