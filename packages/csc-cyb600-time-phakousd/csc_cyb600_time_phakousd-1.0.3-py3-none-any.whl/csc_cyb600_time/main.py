import datetime
from flask import Flask

# Here is a change
app = Flask(__name__)

time=str(datetime.datetime.now())
print(time)

@app.route('/')
def say_time_class():
    return time