from flask import Flask
from github_webhook import Webhook
import telepot
import utils

GITHUB_URL = "https://github.com/"
TOKEN = "484527904:AAHVkzp5hHuxWVfR0tYkIFPV-sgQkXQKqAQ"
# CHANNEL = "-1001084328317"
CHANNEL = "-398468065"
SECRET = "Singapore2017"
Bot = telepot.Bot(TOKEN)
message = "<a href='{pusher_url}'>{pusher}</a> pushed to <a href='{branch_url}'>{branch_name}</a>:\n"
commit_message = "{msg}<a href='{url}'>...</a>\n"

application = Flask(__name__)
webhook = Webhook(application, endpoint="/", secret=SECRET)


@application.route("/hello")
def hello():
    print(1)
    return "<h1>Hello There!</h1>"


@webhook.hook(event_type="ping")        # Defines a handler for the 'push' event
def on_ping(data):
    print("Got ping with: {0}".format(data))


@webhook.hook(event_type="push")        # Defines a handler for the 'push' event
def on_push(data):
    commits = data["commits"]
    pusher = data["pusher"]["name"]
    repo = data["repository"]
    branch = utils.parse_branch(data["ref"])
    answer = message.format(
        pusher=pusher,
        pusher_url=GITHUB_URL + pusher,
        branch_name=repo["name"] + "/" + branch,
        branch_url=repo["url"] + "/tree/" + branch
    )
    for commit in commits:
        answer += commit_message.format(
            msg=commit["message"],
            url=commit["url"],
        )

    Bot.sendMessage(CHANNEL, answer, parse_mode="HTML", disable_web_page_preview=True)
