import os
import hashlib
import hmac
from flask import Flask, request

from google_reminder_api_wrapper import ReminderApi

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SLACK_OAUTH_ACCESS_TOKEN = os.environ['SLACK_OAUTH_ACCESS_TOKEN']
datetime_index = 16

app = Flask(__name__)


def verify(request):
    try:
        slack_secret = bytes(SLACK_SIGNING_SECRET, 'utf-8')
        timestamp = request.headers['X-Slack-Request-Timestamp']
        request_data = request.get_data().decode('utf-8')
        base_string = f"v0:{timestamp}:{request_data}".encode('utf-8')

        my_signature = 'v0=' + \
            hmac.new(slack_secret, base_string, hashlib.sha256).hexdigest()

        result = hmac.compare_digest(
            my_signature, request.headers['X-Slack-Signature'])
    except:
        return False

    return result


def set_reminder(text: str, dt: str):
    try:
        api = ReminderApi()
        new_reminder = api.create(text, dt)
    except:
        return False
    return True


def define_request_texts(text):
    title = text[:-datetime_index-1]
    dt = text[-datetime_index:]
    return title, dt


@app.route('/goremind', methods=['POST'])
def main():
    if verify(request):
        title, dt = define_request_texts(request.form['text'])
        if set_reminder(title, dt):
            return "done"
        else:
            return ('Google reminder query was not allowed', 405)

    else:
        return ('Request failed verification.', 401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '8080'))
