# Copyright 2021 Ecosoft Co.,Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    cosmetic_vat = fields.Integer(
        string="Vat%",
        help="For VAT vendor and company No-VAT, show the cosmetic_vat",
    )
    company_novat = fields.Boolean(
        related="company_id.novat",
    )
    set_cosmetic_vat = fields.Boolean(
        string="Set Cosmetic VAT",
        help="Set to use Vat% to include VAT into price unit, "
        "and calculate cosmatic tax amount",
    )
    cosmetic_untaxed = fields.Monetary(
        string="(Untaxed)",
        store=True,
        readonly=False,
        compute="_compute_cosmetic_footer",
    )
    cosmetic_tax = fields.Monetary(
        string="(Tax)",
        store=True,
        readonly=False,
        compute="_compute_cosmetic_footer",
    )

    @api.depends("set_cosmetic_vat")
    def _compute_cosmetic_footer(self):
        for rec in self:
            untaxed = 0
            for line in rec.order_line:
                untaxed += line.cosmetic_price_subtotal or line.price_subtotal
            total = sum(rec.order_line.mapped("price_subtotal"))
            rec.cosmetic_tax = total - untaxed
            rec.cosmetic_untaxed = untaxed

    @api.onchange("partner_id")
    def _onchange_cosmetic_vat(self):
        if not self.partner_id.novat and self.env.company.novat:
            self.cosmetic_vat = self.env.company.account_purchase_tax_id.amount
        else:
            self.cosmetic_vat = False

    def apply_cosmetic_vat(self):
        self.mapped("order_line").apply_cosmetic_vat()
        self.write({"set_cosmetic_vat": True})

    def remove_cosmetic_vat(self):
        self.mapped("order_line").remove_cosmetic_vat()
        self.write({"set_cosmetic_vat": False})


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    cosmetic_vat = fields.Integer(
        related="order_id.cosmetic_vat",
    )
    set_cosmetic_vat = fields.Boolean()
    cosmetic_price_unit = fields.Float(string="(Price)")
    cosmetic_price_subtotal = fields.Monetary(
        string="(Subtotal)",
        compute="_compute_cosmetic_subtotal",
        store=True,
        readonly=False,
    )

    @api.onchange("product_qty", "price_unit")
    def _onchange_cosmetic_product_qty(self):
        if self._origin.cosmetic_vat:
            self.cosmetic_vat = False
            self.cosmetic_price_unit = False

    def apply_cosmetic_vat(self):
        for rec in self.filtered(lambda l: not l.set_cosmetic_vat):
            rec.cosmetic_price_unit = rec.price_unit
            rec.price_unit = rec.cosmetic_price_unit * (1 + rec.cosmetic_vat / 100)
            rec.order_id._compute_cosmetic_footer()
        self.write({"set_cosmetic_vat": True})

    def remove_cosmetic_vat(self):
        for rec in self.filtered(lambda l: l.set_cosmetic_vat):
            rec.price_unit = rec.cosmetic_price_unit
            rec.cosmetic_price_unit = False
            rec.order_id._compute_cosmetic_footer()
        self.write({"set_cosmetic_vat": False})

    @api.depends("cosmetic_price_unit", "product_qty")
    def _compute_cosmetic_subtotal(self):
        for rec in self:
            rec.cosmetic_price_subtotal = rec.cosmetic_price_unit * rec.product_qty
