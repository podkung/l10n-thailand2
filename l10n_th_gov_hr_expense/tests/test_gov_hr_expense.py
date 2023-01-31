# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.addons.l10n_th_gov_purchase_request.tests.test_gov_purchase_request import (
    TestGovPurchaseRequest,
)


class TestGovHrExpense(TestGovPurchaseRequest):
    def setUp(self):
        super().setUp()
        self.HrExpenseSheet = self.env["hr.expense.sheet"]
        self.HrExpense = self.env["hr.expense"]

        self.expense_product = self.env.ref("hr_expense.product_product_zero_cost")

    def test_01_create_expense_ref_pr(self):
        # Create purchase request
        purchase_request = self.purchase_request_model.create(
            {
                "procurement_type_id": self.procurement_type1.id,
                "procurement_method_id": self.procurement_method1.id,
                "purchase_type_id": self.purchase_type3.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "estimated_cost": 100.0,
                            "product_qty": 1,
                        },
                    )
                ],
            }
        )
        # Create expense sheet
        expense_sheet = self.HrExpenseSheet.create(
            {
                "name": "Expense test",
                "employee_id": self.employee1.id,
                "purchase_request_id": purchase_request.id,
            }
        )
        expenses = self.HrExpense.create(
            [
                {
                    "name": "Expense Line 1",
                    "employee_id": self.employee1.id,
                    "product_id": self.expense_product.id,
                    "unit_amount": 1,
                    "quantity": 10,
                    "sheet_id": expense_sheet.id,
                    "payment_mode": "own_account",
                },
                {
                    "name": "Expense Line 2",
                    "employee_id": self.employee1.id,
                    "product_id": self.expense_product.id,
                    "unit_amount": 1,
                    "quantity": 20,
                    "sheet_id": expense_sheet.id,
                    "payment_mode": "own_account",
                },
            ]
        )
        for expense in expenses:
            self.assertEqual(
                expense.purchase_type_id, purchase_request.purchase_type_id
            )
