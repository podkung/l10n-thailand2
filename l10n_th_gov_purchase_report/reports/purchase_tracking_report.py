# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, fields, models
from odoo.exceptions import UserError


class PurchaseTrackingReportView(models.TransientModel):
    _name = "purchase.tracking.report.view"
    _description = "Purchase Report View"
    _order = "id"

    pr_id = fields.Many2one(comodel_name="purchase.request", index=True)
    po_id = fields.Many2one(
        comodel_name="purchase.order",
    )
    te_id = fields.Many2one(
        comodel_name="purchase.requisition",
    )
    agm_id = fields.Many2one(
        comodel_name="agreement",
    )
    wa_id = fields.Many2one(
        comodel_name="work.acceptance",
    )
    move_id = fields.Many2one(
        comodel_name="account.move",
    )
    company_id = fields.Many2one(
        comodel_name="res.company", string="Company", index=True
    )


class PurchaseTrackingReport(models.TransientModel):
    _name = "report.purchase.tracking.report"
    _description = "Purchase Tracking Report"

    date_from = fields.Date()
    date_to = fields.Date()
    company_id = fields.Many2one(comodel_name="res.company")
    requested_by = fields.Many2many(comodel_name="res.users")

    # Data fields, used to browse report data
    results = fields.Many2many(
        comodel_name="purchase.tracking.report.view",
        compute="_compute_results",
        help="Use compute fields, so there is nothing store in database",
    )

    def _get_where_purchase_report(self):
        # Users can see report with requested by yourself only
        if not self.env.user.has_group("purchase.group_purchase_user"):
            filter_user = "AND requested_by = {}".format(self.env.user.id)
        else:  # Procurement can see all users, if not filter user
            if not self.requested_by:
                filter_user = ""
            elif len(self.requested_by) > 1:
                filter_user = "AND requested_by in {}".format(
                    tuple(self.requested_by.ids)
                )
            else:
                filter_user = "AND requested_by = {}".format(self.requested_by.id)
        where_domain = (
            "WHERE company_id = {} AND date_start >= '{}' "
            "AND date_start <= '{}' {}".format(
                self.company_id.id, self.date_from, self.date_to, filter_user
            )
        )
        return where_domain

    def _get_query_purchase_tracking(self):
        self._cr.execute(
            """
            SELECT
                ROW_NUMBER() OVER(order by pr_table.id, po_table.id, te_table.id,
                    po_table.wa_id, po_table.move_id) AS id,
                pr_table.id AS pr_id, po_table.id AS po_id, te_table.id AS te_id,
                po_table.agm_id as agm_id, po_table.wa_id as wa_id,
                po_table.move_id as move_id
            FROM(
                -- PR
                SELECT pr.id
                FROM purchase_request pr
                {}
            ) pr_table
            FULL JOIN(
                -- PO
                SELECT po.id, max(pr_line.request_id) AS request_id, agm.id as agm_id,
                    wa.id as wa_id, move_po.account_move_id as move_id
                FROM purchase_order po
                LEFT JOIN purchase_order_line po_line ON po.id = po_line.order_id
                LEFT JOIN purchase_request_purchase_order_line_rel pr_po_line
                    ON po_line.id = pr_po_line.purchase_order_line_id
                LEFT JOIN purchase_request_line pr_line
                    ON pr_po_line.purchase_request_line_id = pr_line.id
                LEFT JOIN agreement agm ON agm.purchase_order_id = po.id
                LEFT JOIN work_acceptance wa ON wa.purchase_id = po.id
                    AND wa.state != 'cancel'
                LEFT JOIN account_move_purchase_order_rel move_po
                    ON move_po.purchase_order_id = po.id
                WHERE po.state != 'cancel'
                GROUP BY po.id, agm.id, wa.id, move_po.account_move_id
            ) po_table ON pr_table.id = po_table.request_id
            FULL JOIN(
                -- TE
                SELECT te.id, pr_line.request_id
                FROM purchase_requisition te
                LEFT JOIN purchase_requisition_line te_line
                    ON te.id = te_line.requisition_id
                LEFT JOIN purchase_request_purchase_requisition_line_rel pr_te_line
                    ON te_line.id = pr_te_line.purchase_requisition_line_id
                LEFT JOIN purchase_request_line pr_line
                    ON pr_te_line.purchase_request_line_id = pr_line.id
            ) te_table on pr_table.id = te_table.request_id
            WHERE pr_table.id IS NOT NULL
            """.format(
                self._get_where_purchase_report()
            )
        )
        return self.env.cr.dictfetchall()

    def _compute_results(self):
        self.ensure_one()
        procurement_report_results = self._get_query_purchase_tracking()
        ReportLine = self.env["purchase.tracking.report.view"]
        self.results = False
        for line in procurement_report_results:
            self.results += ReportLine.new(line)

    def _hook_print_report(self):
        raise UserError(
            _(
                "This report support type xlsx only. "
                "you can implement it at function '_hook_print_report'"
            )
        )

    def print_report(self, report_type="xlsx"):
        self.ensure_one()
        if report_type != "xlsx":
            return self._hook_print_report()
        action = self.env.ref(
            "l10n_th_gov_purchase_report.action_purchase_tracking_report_xlsx"
        )
        return action.report_action(self, config=False)
