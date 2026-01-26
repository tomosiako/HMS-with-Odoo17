#from pkg_resources import require
from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string="Name",required=True, tracking=True)
    date_of_birth = fields.Date(string="DOB",tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender",tracking=True)
    tag_ids = fields.Many2many(
        'patient.tag','patient_tag_rel','patient_id',string="Tags")

    product_ids = fields.Many2many(
        'product.product',string="Products"
    )

    def unlink(self):
        for rec in self:
            domain = [('patient_id','=',rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise UserError(_("You cannot delete the patient now "
                                        "\n Appointments exist for this patient: %s" %rec.name))
        return super().unlink()

