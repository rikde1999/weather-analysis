FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /weather_analysis_system
WORKDIR /weather_analysis_system
COPY requirements.txt /weather_analysis_system/
RUN pip install -r requirements.txt
COPY . /weather_analysis_system/
EXPOSE 8000
ENTRYPOINT ["gunicorn", 'weather_analysis_system.wsgi']