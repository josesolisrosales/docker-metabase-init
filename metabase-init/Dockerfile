FROM python:3.9

ADD python/setup.py .

RUN pip install requests argparse

CMD ["python", "./setup.py" , "--help"]