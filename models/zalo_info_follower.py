# -*- coding: utf-8 -*-

from odoo import models, fields


class ZaloInfoFollower(models.Model):
    _name = 'zalo.info.follower'

    follower_id = fields.Char('Zalo ID')
    follower_info = fields.Text("Information")


class ZaloInfoMessage(models.Model):
    _name = 'zalo.info.message'

    follower_id = fields.Char('Zalo ID')
    question = fields.Char('Bot Question')
    answer = fields.Char('Follower Answer')


