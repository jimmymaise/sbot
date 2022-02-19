import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk import WebClient
from bot_handlers.pto_register import PTORegister
from handlers.database.google_sheet import GoogleSheetDB

if not os.getenv('ENV'):
    load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
bolt_app = App(token=os.environ.get("SLACK_BOT_TOKEN"),
               signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
               url_verification_enabled=True,
               request_verification_enabled=False,
               process_before_response=True
               )

google_sheet_db = GoogleSheetDB(
    service_account_file_content=os.getenv('GOOGLE_SERVICE_BASE64_FILE_CONTENT'), is_encode_base_64=True)
PTORegister(bolt_app, client, google_sheet_db,
            leave_register_sheet=os.getenv('LEAVE_REGISTER_SHEET'),
            approval_channel=os.getenv('MANAGER_LEAVE_APPROVAL_CHANNEL'))


def handler(event, context):
    slack_handler = SlackRequestHandler(app=bolt_app)
    return slack_handler.handle(event, context)
