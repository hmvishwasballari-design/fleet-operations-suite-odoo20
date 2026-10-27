from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FleetDriver(models.Model):
    _name = "fleet.ops.driver"
    _description = "Fleet Driver"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    employee_code = fields.Char(required=True, copy=False, index=True)
    phone = fields.Char()
    email = fields.Char()
    license_number = fields.Char(required=True)
    license_expiry = fields.Date()
    active = fields.Boolean(default=True)
    vehicle_ids = fields.One2many("fleet.ops.vehicle", "driver_id", string="Assigned Vehicles")
    notes = fields.Text()

    _sql_constraints = [
        ("employee_code_unique", "unique(employee_code)", "Employee code must be unique."),
        ("license_unique", "unique(license_number)", "License number must be unique."),
    ]

    @api.constrains("license_expiry")
    def _check_license_expiry(self):
        today = fields.Date.today()
        for driver in self:
            if driver.license_expiry and driver.license_expiry < today:
                raise ValidationError(_("Driver's license has expired. Update the record before assigning a vehicle."))
