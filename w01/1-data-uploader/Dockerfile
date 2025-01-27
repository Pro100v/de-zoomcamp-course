FROM python:3.12.8 


# Update package list and install wget
RUN apt update && \
    apt-get install --no-install-recommends -y \
        wget && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/log/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set the working directory
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
# Copy project into workdir
COPY . .
COPY ingest_data.py ingest_data.py 

# Set the entrypoint
ENTRYPOINT [ "python", "ingest_data.py" ]