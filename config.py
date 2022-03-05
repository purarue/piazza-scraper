import os

class Config:
    username = os.environ["PIAZZA_USERNAME"]
    password = os.environ["PIAZZA_PASSWORD"]
    courseid = os.environ['COURSEID']
