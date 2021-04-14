# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ZaloBotQuestion(models.Model):
    _name = 'zalo.bot.question'
    _order = "sequence"

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name')
