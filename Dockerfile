# Use an official Python runtime environment
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dataset and script files directly into the container directory
COPY All_Diets.csv /app/All_Diets.csv
COPY data_analysis.py /app/data_analysis.py

# Pre-install the required data analysis frameworks
RUN pip install --no-cache-dir pandas matplotlib seaborn

# Command to automatically execute the script when the container boots up
CMD ["python", "data_analysis.py"]
