FROM python:3.11

ADD Pipfile .
ADD Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . .

CMD ["python", "-m", "src.main"]