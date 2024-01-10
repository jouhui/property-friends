FROM python:3.11

ADD Pipfile .
ADD Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.main"]