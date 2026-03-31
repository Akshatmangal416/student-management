from odoo import models, fields, api   # 👈 MUST

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

    # 🔥 CREATE
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            student = record.student_id
            if student:
                total = sum(student.payment_ids.mapped('amount'))
                student.write({'fees_paid': total})

        return records

    # 🔥 WRITE (UPDATE)
    def write(self, vals):
        # old student save karo
        old_students = self.mapped('student_id')

        res = super().write(vals)

        # new student bhi include karo
        new_students = self.mapped('student_id')
        students = (old_students | new_students)

        for student in students:
            total = sum(student.payment_ids.mapped('amount'))
            student.write({'fees_paid': total})

        return res

    # 🔥 DELETE HANDLE (optional but pro level)
    def unlink(self):
        students = self.mapped('student_id')

        res = super().unlink()

        for student in students:
            total = sum(student.payment_ids.mapped('amount'))
            student.write({'fees_paid': total})

        return res