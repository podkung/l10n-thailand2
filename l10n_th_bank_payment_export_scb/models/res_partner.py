# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    scb_email_partner = fields.Char()
    scb_phone_partner = fields.Char()
    scb_sms_partner = fields.Char()
