FROM ubuntu

# Install dependencies
RUN apt update && apt install -y python3 python3-pip 
RUN pip install flask requests gunicorn boto3

# Copy the application code into the container
COPY ./WeatherForecast-app /WeatherForecast-app

# Set the working directory and user
WORKDIR /WeatherForecast-app

# Start the Flask application with Gunicorn
CMD gunicorn --workers=1 --bind=0.0.0.0:8000 Weather_Forecast_Flask:app

