FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /weather_analysis_system
WORKDIR /weather_analysis_system
COPY requirements.txt /weather_analysis_system/
RUN pip install -r requirements.txt
COPY . /weather_analysis_system/
EXPOSE 8000
CMD ["gunicorn", "weather_analysis_system.wsgi:application", "--bind", "0.0.0.0:8000"]