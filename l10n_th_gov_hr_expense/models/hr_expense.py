# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrExpense(models.Model):
    _inherit = "hr.expense"

    pr_line_id = fields.Many2one(
        comodel_name="purchase.request.line",
        ondelete="cascade",
        help="Expense created from this purchase request line",
    )
    purchase_type_id = fields.Many2one(
        string="Purchase Type",
        comodel_name="purchase.type",
        compute="_compute_purchase_type_id",
        domain=[("to_create", "=", "expense")],
        store=True,
        readonly=False,
        index=True,
        ondelete="restrict",
    )

    @api.depends("sheet_id.purchase_request_id")
    def _compute_purchase_type_id(self):
        for expense in self:
            if expense.sheet_id.purchase_request_id:
                expense.purchase_type_id = (
                    expense.sheet_id.purchase_request_id.purchase_type_id
                )


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    employee_user_id = fields.Many2one(
        related="employee_id.user_id",
        readonly=True,
    )
    purchase_request_id = fields.Many2one(
        comodel_name="purchase.request",
        string="Purchase Request",
        ondelete="restrict",
        domain="[('requested_by', '=', employee_user_id), ('state', '=', 'approved'), "
        "('purchase_type_id.to_create', '=', 'expense')]",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        index=True,
        help="Select purchase request of this employee, to create expense lines",
    )
    pr_for = fields.Selection(
        selection=[("expense", "Expense"), ("advance", "Advance")],
        string="Use PR for",
        compute="_compute_pr_for",
        required=True,
        store=True,
        readonly=False,
    )
    pr_line_ids = fields.One2many(
        comodel_name="hr.expense.sheet.prline",
        inverse_name="sheet_id",
        copy=False,
    )
    no_pr_check = fields.Boolean(
        string="Skip Amount Check",
        groups="hr_expense.group_hr_expense_manager",
        copy=False,
    )

    @api.depends("advance")
    def _compute_pr_for(self):
        for rec in self:
            rec.pr_for = "advance" if rec.advance else "expense"

    @api.onchange("employee_id")
    def _onchange_purchase_request_employee(self):
        self.purchase_request_id = False

    @api.onchange("purchase_request_id")
    def _onchange_purchase_request_id(self):
        SheetPRLine = self.env["hr.expense.sheet.prline"]
        self.pr_line_ids = False
        for line in self.purchase_request_id.line_ids:
            sheet_prline = self._prepare_sheet_prline(line)
            self.pr_line_ids += SheetPRLine.new(sheet_prline)

    @api.onchange("advance_sheet_id")
    def _onchange_advance_sheet_id(self):
        res = super()._onchange_advance_sheet_id()
        # Advance and PR should not work together
        if self.advance_sheet_id:
            self.purchase_request_id = False
        return res

    def _prepare_sheet_prline(self, line):
        """Prepare data, to create hr.expense. All must be hr.expense's fields"""
        unit_amount = (
            line.estimated_cost / line.product_qty if line.product_qty > 0 else 0
        )
        return {
            "unit_amount": unit_amount,
            "quantity": line.product_qty,
            "pr_line_id": line.id,
        }

    @api.model
    def create(self, vals):
        sheet = super().create(vals)
        if "purchase_request_id" in vals:
            sheet.mapped("expense_line_ids").filtered("pr_line_id").unlink()
        sheet._do_process_from_purchase_request()
        sheet.pr_line_ids.unlink()  # clean after use
        return sheet

    def write(self, vals):
        res = super().write(vals)
        if "purchase_request_id" in vals:
            self.mapped("expense_line_ids").filtered("pr_line_id").unlink()
        self._do_process_from_purchase_request()
        self.mapped("pr_line_ids").unlink()  # clean after use
        return res

    def _do_process_from_purchase_request(self):
        """Hook method"""
        # Expense
        sheets = self.filtered(
            lambda l: l.purchase_request_id and l.pr_for == "expense"
        )
        sheets._create_expenses_from_prlines()
        # Advance
        av_sheets = self.filtered(
            lambda l: l.purchase_request_id and l.pr_for == "advance"
        )
        av_sheets.with_context(advance=True)._create_expenses_from_prlines()

    def _create_expenses_from_prlines(self):
        for sheet in self:
            expenses_list = []
            sheet.pr_line_ids.read()  # Force prefetch
            for line in sheet.pr_line_ids:
                pr_line = self._prepare_expense_from_prline(line)
                expenses_list.append(pr_line)
            self.env["hr.expense"].sudo().create(expenses_list)

    def _prepare_expense_from_prline(self, line):
        # Read origin prline values with same columns as Expense object
        pr_line = self.env["hr.expense"]._convert_to_write(line.pr_line_id.read()[0])
        # Remove unused fields, i.e., one2many, mail.thread and mail.activity.mixin
        _fields = line.pr_line_id._fields
        del_cols = [k for k in _fields.keys() if _fields[k].type == "one2many"]
        del_cols += list(self.env["mail.thread"]._fields.keys())
        del_cols += list(self.env["mail.activity.mixin"]._fields.keys())
        del_cols = list(set(del_cols))
        pr_line = {k: v for k, v in pr_line.items() if k not in del_cols}
        # sheet_pr_line gets higher priority
        sheet_pr_line = self.env["hr.expense"]._convert_to_write(line._cache)
        pr_line.update(sheet_pr_line)
        # Convert list of int to [(6, 0, list)]
        pr_line = {
            k: isinstance(v, list) and [(6, 0, v)] or v for k, v in pr_line.items()
        }
        # Case Advance
        if self.env.context.get("advance"):
            # Change to advance, and product to clearing_product_id
            av_line = self.env["hr.expense"].new({"advance": True})
            av_line.onchange_advance()
            av_line._compute_from_product_id_company_id()
            av_line = av_line._convert_to_write(av_line._cache)
            # Assign known values
            pr_line["clearing_product_id"] = pr_line["product_id"]
            pr_line["product_id"] = av_line["product_id"]
            pr_line["advance"] = av_line["advance"]
            pr_line["name"] = av_line["name"]
            pr_line["account_id"] = av_line["account_id"]
        return pr_line

    def action_submit_sheet(self):
        for rec in self.filtered("purchase_request_id"):
            pr_amount = sum(rec.purchase_request_id.line_ids.mapped("estimated_cost"))
            ex_amount = sum(rec.expense_line_ids.mapped("untaxed_amount"))
            if not rec.sudo().no_pr_check and ex_amount > pr_amount:
                raise UserError(
                    _(
                        "Requested amount exceed the approved amount from "
                        "purchase request.\nPlease contact your HR manager."
                    )
                )
        return super().action_submit_sheet()

    def approve_expense_sheets(self):
        purchase_requests = self.mapped("purchase_request_id")
        for purchase_request in purchase_requests:
            if purchase_request.state != "approved":
                raise UserError(
                    _(
                        "Purchase Request %s should be in status "
                        "'Approved' when approving this expense"
                    )
                    % purchase_request.name
                )
        purchase_requests.button_done()
        return super().approve_expense_sheets()


class HrExpenseSheetPRLine(models.Model):
    _name = "hr.expense.sheet.prline"
    _description = "Temp Holder of PR Lines data, used to create hr.expense"

    sheet_id = fields.Many2one(
        comodel_name="hr.expense.sheet",
        string="Expense Report",
    )
    pr_line_id = fields.Many2one(
        comodel_name="purchase.request.line",
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        related="sheet_id.employee_id",
        readonly=True,
    )
    name = fields.Char(
        string="Description",
        related="pr_line_id.name",
        readonly=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        related="pr_line_id.product_id",
        readonly=True,
    )
    quantity = fields.Float(
        digits="Product Unit of Measure",
    )
    total_amount = fields.Monetary(
        string="Total",
        compute="_compute_total_amount",
        readonly=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="pr_line_id.currency_id",
        readonly=True,
    )
    unit_amount = fields.Monetary(
        string="Unit Price",
    )
    description = fields.Text(
        string="Notes...",
        related="pr_line_id.description",
        readonly=True,
    )
    reference = fields.Text(
        string="Bill Reference",
        related="pr_line_id.specifications",
        readonly=True,
    )

    @api.depends("unit_amount", "quantity")
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.unit_amount * rec.quantity
