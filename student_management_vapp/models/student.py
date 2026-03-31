
from odoo import models, fields, api


# ================================
# 🔹 STUDENT MODEL
# ================================
class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Management'

    # 🔹 Basic Info
    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    course = fields.Char(string="Course")

    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], default='active')

    student_code = fields.Char(string="Student ID", readonly=True)

    # 🔥 Fees System
    fees_total = fields.Float(string="Total Fees")
    fees_paid = fields.Float(string="Fees Paid")

    fees_due = fields.Float(
        string="Fees Due",
        compute="_compute_fees",
        store=True
    )

    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('unpaid', 'Unpaid')
    ],
        string="Payment Status",
        compute="_compute_fees",
        store=True
    )

    # 🔥 Payment Relation
    payment_ids = fields.One2many(
        'student.payment',
        'student_id',
        string="Payments"
    )

    # 🔥 Auto Fees Logic
    @api.depends('fees_total', 'fees_paid')
    def _compute_fees(self):
        for rec in self:
            rec.fees_due = rec.fees_total - rec.fees_paid

            if rec.fees_paid == 0:
                rec.payment_status = 'unpaid'
            elif rec.fees_paid < rec.fees_total:
                rec.payment_status = 'partial'
            else:
                rec.payment_status = 'paid'

    # 🔥 Auto Student ID
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['student_code'] = self.env['ir.sequence'].next_by_code('student.seq') or 'STU000'
        return super().create(vals_list)


# ================================
# 🔹 PAYMENT MODEL
# ================================
class StudentPayment(models.Model):
    _name = 'student.payment'
    _description = 'Student Payment'

    student_id = fields.Many2one(
        'student.student',
        string="Student",
        required=True,
        ondelete='cascade'
    )

    amount = fields.Float(string="Amount", required=True)

    payment_date = fields.Date(
        string="Payment Date",
        default=fields.Date.today
    )

    # 🔥 CREATE OVERRIDE
    @api.model
    def create(self, vals):
        record = super().create(vals)

        if record.student_id:
            total = sum(record.student_id.payment_ids.mapped('amount'))

            record.student_id.write({
                'fees_paid': total
            })

        return record

    # 🔥 WRITE OVERRIDE
    def write(self, vals):
        res = super().write(vals)

        for rec in self:
            if rec.student_id:
                total = sum(rec.student_id.payment_ids.mapped('amount'))

                rec.student_id.write({
                    'fees_paid': total
                })

        return res


