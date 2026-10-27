from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FleetService(models.Model):
    _name = "fleet.ops.service"
    _description = "Fleet Service Record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "service_date desc, id desc"

    name = fields.Char(default="New", required=True, copy=False, readonly=True)
    vehicle_id = fields.Many2one("fleet.ops.vehicle", required=True, ondelete="restrict", tracking=True)
    service_date = fields.Date(default=fields.Date.context_today, required=True)
    service_type = fields.Selection([
        ("routine", "Routine Service"),
        ("repair", "Repair"),
        ("inspection", "Inspection"),
        ("tyre", "Tyre Replacement"),
        ("insurance", "Insurance"),
        ("other", "Other"),
    ], required=True, default="routine")
    odometer_km = fields.Float(required=True)
    vendor = fields.Char()
    cost = fields.Monetary(currency_field="currency_id", default=0.0)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    next_service_date = fields.Date()
    state = fields.Selection([
        ("planned", "Planned"), ("in_progress", "In Progress"),
        ("done", "Done"), ("cancelled", "Cancelled")
    ], default="planned", required=True, tracking=True)
    description = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("fleet.ops.service") or "New"
        return super().create(vals_list)

    @api.constrains("cost", "odometer_km")
    def _check_nonnegative_values(self):
        for record in self:
            if record.cost < 0 or record.odometer_km < 0:
                raise ValidationError(_("Cost and odometer must not be negative."))

    def action_start(self):
        self.write({"state": "in_progress"})
        self.mapped("vehicle_id").write({"state": "maintenance"})

    def action_complete(self):
        for service in self:
            service.state = "done"
            if service.odometer_km > service.vehicle_id.odometer_km:
                service.vehicle_id.odometer_km = service.odometer_km
            if service.vehicle_id.state == "maintenance":
                service.vehicle_id.state = "available"
