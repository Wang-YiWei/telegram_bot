import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

#from flaskext.mysql import MySQL

from fsm import TocMachine


API_TOKEN = '533331484:AAFw1ZEbqLea3icqEwc1AzKmOsnYcHgsbJk'
WEBHOOK_URL = 'https://b0b48360.ngrok.io/hook'

app = Flask(__name__)


bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        # 'blank',
        'user',
        'boring',
        # customer side
        'customer',
        'Taipei',
        'Taichung',
        'Tainan',
        # owner side
        'owner',
        'signup',
        'login',
        'verify',
        'next',
        'reset',
        'resetnum',
        # shops
        'subway',
        'donut',
        'tasty',
        'mcdonald',
        'doublecheese',
        'burgerking',
        'subwaycheck',
        'donutcheck',
        'tastycheck',
        'mcdonaldcheck',
        'doublecheesecheck',
        'burgerkingcheck'
    ],
    transitions=[
        # {
        #     'trigger': 'advance',
        #     'source': 'blank',
        #     'dest': 'user',
        #     'conditions': 'is_going_to_user'
        # },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'boring',
            'conditions': 'is_going_to_boring'
        },
        # customer side
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'customer',
            'conditions': 'is_going_to_customer'
        },
        {
            'trigger': 'advance',
            'source': 'customer',
            'dest': 'Taipei',
            'conditions': 'is_going_to_Taipei'
        },
        {
            'trigger': 'advance',
            'source': 'customer',
            'dest': 'Taichung',
            'conditions': 'is_going_to_Taichung'
        },
        {
            'trigger': 'advance',
            'source': 'customer',
            'dest': 'Tainan',
            'conditions': 'is_going_to_Tainan'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'subway',
            'conditions': 'is_going_to_subway'
        },
        {
            'trigger': 'advance',
            'source': 'Taipei',
            'dest': 'donut',
            'conditions': 'is_going_to_donut'
        },
        {
            'trigger': 'advance',
            'source': 'Taichung',
            'dest': 'tasty',
            'conditions': 'is_going_to_tasty'
        },
        {
            'trigger': 'advance',
            'source': 'Taichung',
            'dest': 'mcdonald',
            'conditions': 'is_going_to_mcdonald'
        },
        {
            'trigger': 'advance',
            'source': 'Tainan',
            'dest': 'doublecheese',
            'conditions': 'is_going_to_doublecheese'
        },
        {
            'trigger': 'advance',
            'source': 'Tainan',
            'dest': 'burgerking',
            'conditions': 'is_going_to_burgerking'
        },
        # check again
        {
            'trigger': 'advance',
            'source': 'subway',
            'dest': 'subwaycheck',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'advance',
            'source': 'donut',
            'dest': 'donutcheck',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'advance',
            'source': 'tasty',
            'dest': 'tastycheck',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'advance',
            'source': 'mcdonald',
            'dest': 'mcdonaldcheck',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'advance',
            'source': 'doublecheese',
            'dest': 'doublecheesecheck',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'advance',
            'source': 'burgerking',
            'dest': 'burgerkingcheck',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'go_back_to_subway',
            'source':'subwaycheck',
            'dest': 'subway'
        },
        {
            'trigger': 'go_back_to_donut',
            'source':'donutcheck',
            'dest': 'donut'
        },
        {
            'trigger': 'go_back_to_tasty',
            'source':'tastycheck',
            'dest': 'tasty'
        },
        {
            'trigger': 'go_back_to_mcdonald',
            'source':'mcdonaldcheck',
            'dest': 'mcdonald'
        },
        {
            'trigger': 'go_back_to_doublecheese',
            'source':'doublecheesecheck',
            'dest': 'doublecheese'
        },
        {
            'trigger': 'go_back_to_burgerking',
            'source':'burgerkingcheck',
            'dest': 'burgerking'
        },
        # owner side
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'owner',
            'conditions': 'is_going_to_owner'
        },
        {
            'trigger': 'advance',
            'source': 'owner',
            'dest': 'login',
            'conditions': 'is_going_to_login'
        },
        {
            'trigger': 'advance',
            'source': 'owner',
            'dest': 'signup',
            'conditions': 'is_going_to_signup'
        },
        {
            'trigger': 'advance',
            'source': 'login',
            'dest': 'verify',
            'conditions': 'is_going_to_verify'
        },
        {
            'trigger': 'advance',
            'source': 'verify',
            'dest': 'next',
            'conditions': 'is_going_to_next'
        },
        {
            'trigger': 'advance',
            'source': 'verify',
            'dest': 'reset',
            'conditions': 'is_going_to_reset'
        },
        {
            'trigger': 'advance',
            'source': 'reset',
            'dest': 'resetnum',
            'conditions': 'reset_done'
        },
        {
            'trigger': 'go_back',
            'source': 'next',
            'dest': 'verify'
        },
        {
            'trigger': 'go_back_from_reset',
            'source': 'resetnum',
            'dest': 'verify',
        },
        {
            'trigger': 'advance',
            'source': [
                'boring',
                 # customer side
                'customer',
                'Taipei',
                'Taichung',
                'Tainan',
                # owner side
                'owner',
                'signup',
                'login',
                'verify',
                'next',
                'reset',
                'resetnum',
                # shops
                'subway',
                'donut',
                'tasty',
                'mcdonald',
                'doublecheese',
                'burgerking'
            ],
            'dest': 'user',
            'conditions': 'go_back_to_user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))
        

@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id

    machine.advance(update,bot,chat_id)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()