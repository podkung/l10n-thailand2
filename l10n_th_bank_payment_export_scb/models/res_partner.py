# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    scb_beneficiary_noti = fields.Selection(
        selection=[
            ("N", "N - None"),
            ("F", "F - Fax"),
            ("S", "S - SMS"),
            ("E", "E - Email"),
        ],
        default="N",
        string="Beneficiary Notification",
    )
    scb_email_partner = fields.Char(string="Default Email")
    scb_phone_partner = fields.Char(string="Default Fax")
    scb_sms_partner = fields.Char(string="Default SMS")
    scb_beneficiary_charge = fields.Boolean(string="Beneficiary Charge")
