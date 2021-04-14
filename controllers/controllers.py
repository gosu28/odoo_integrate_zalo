import logging
import json

import requests

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebhookController(http.Controller):

    @http.route('/get_info', type='json', auth='public')
    def get_follower_info(self, **kwargs):
        h = http.request.httprequest
        data = h.data
        encoding = 'utf-8'
        paypload = str(data, encoding)
        message = json.loads(paypload)
        if request.env['ir.config_parameter'].sudo().get_param('zalo_message.is_setting'):
            access_token = request.env['ir.config_parameter'].sudo().get_param('zalo_message.access_token')
        else:
            raise ValueError('You have not set up the access token')
        url = 'https://openapi.zalo.me/v2.0/oa/message?access_token=' + str(access_token)
        headers = {
            'Content-Type': 'application/json'
        }
        list_bot_question = []
        bot_question = request.env['zalo.bot.question'].sudo().search([], order='sequence asc')
        for bot in bot_question:
            list_bot_question.append(bot.name)
        if message['event_name'] == 'follow':
            data = {
                "recipient": {
                    "user_id": message['follower']['id']
                },
                "message": {
                    "text": list_bot_question[0]
                }
            }
            data_json = json.dumps(data, indent=4)
            data_json.replace(" ' ", ' " ')
            requests.post(url, data=data_json, headers=headers)
            follower = request.env['zalo.info.message'].sudo().search([('follower_id', '=', message['follower']['id'])])
            follower_id = message['follower']['id']
            if len(follower) == 0:
                request.env['zalo.info.message'].sudo().create({
                    'follower_id': follower_id,
                    'question': list_bot_question[0],
                })
        elif message['event_name'] == 'user_send_text':
            answer_related = request.env['zalo.info.message'].sudo().search([('follower_id', '=', message['sender']['id'])])
            list_answered = []
            next_question = ''
            if answer_related:
                for x in answer_related:
                    list_answered.append(x.question)
            if list_answered:
                for i in range(0, len(list_bot_question) - 1):
                    if list_answered[-1] == list_bot_question[i]:
                        next_question = list_bot_question[i + 1]

            current_question = request.env['zalo.info.message'].sudo().search([('follower_id', '=', message['sender']['id']), ('question', '=', list_answered[-1])])
            if current_question:
                current_question.sudo().write({
                    'answer': message['message']['text']
                })

            if next_question != '':
                user_id = message['sender']['id']
                data = {
                    "recipient": {
                        "user_id": user_id
                    },
                    "message": {
                        "text": next_question
                    }
                }
                data_json = json.dumps(data, indent=4)
                data_json.replace(" ' ", ' " ')
                requests.post(url, data=data_json, headers=headers)
                request.env['zalo.info.message'].sudo().create({
                    'follower_id': user_id,
                    'question': next_question,
                })
        elif message['event_name'] == 'unfollow':
            unfollower_id = message['follower']['id']
            unfollower = request.env['zalo.info.message'].sudo().search([('follower_id', '=', unfollower_id)])
            if unfollower:
                unfollower.active = False
        elif 'event_name' not in message:
            pass
