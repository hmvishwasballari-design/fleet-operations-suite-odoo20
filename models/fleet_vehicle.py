from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _name = "fleet.ops.vehicle"
    _description = "Fleet Vehicle"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    registration_number = fields.Char(required=True, copy=False, index=True, tracking=True)
    vin = fields.Char(string="VIN / Chassis Number", copy=False)
    make = fields.Char(required=True)
    model_name = fields.Char(string="Model")
    year = fields.Integer()
    vehicle_type = fields.Selection([
        ("car", "Car"), ("bike", "Bike"), ("van", "Van"),
        ("truck", "Truck"), ("other", "Other")
    ], default="car", required=True)
    state = fields.Selection([
        ("available", "Available"),
        ("assigned", "Assigned"),
        ("maintenance", "In Maintenance"),
        ("retired", "Retired"),
    ], default="available", required=True, tracking=True)
    driver_id = fields.Many2one("fleet.ops.driver", string="Current Driver", tracking=True)
    odometer_km = fields.Float(string="Odometer (km)")
    purchase_date = fields.Date()
    insurance_expiry = fields.Date()
    service_ids = fields.One2many("fleet.ops.service", "vehicle_id", string="Service Records")
    service_count = fields.Integer(compute="_compute_service_count")
    notes = fields.Text()

    _sql_constraints = [
        ("registration_unique", "unique(registration_number)", "Registration number must be unique."),
        ("odometer_nonnegative", "CHECK(odometer_km >= 0)", "Odometer cannot be negative."),
    ]

    @api.depends("service_ids")
    def _compute_service_count(self):
        for vehicle in self:
            vehicle.service_count = len(vehicle.service_ids)

    @api.constrains("year")
    def _check_year(self):
        current_year = fields.Date.today().year
        for vehicle in self:
            if vehicle.year and (vehicle.year < 1886 or vehicle.year > current_year + 1):
                raise ValidationError(_("Enter a valid vehicle manufacturing year."))

    def action_mark_available(self):
        self.write({"state": "available", "driver_id": False})

    def action_mark_maintenance(self):
        self.write({"state": "maintenance"})

    def action_retire(self):
        self.write({"state": "retired", "driver_id": False})
