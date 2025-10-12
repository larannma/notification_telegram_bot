FROM python:3.12

WORKDIR /app

# Copy and install libraries
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run init.py and main.py files
CMD ["sh", "-c", "python ./main.py"]

