# Fleet Operations Suite — Odoo 20

A custom Odoo addon for fleet vehicles, drivers, and maintenance/service history.

## Features
- Vehicle registry with unique registration numbers and non-negative odometer checks.
- Driver registry with unique employee/license identifiers and license-expiry validation.
- Vehicle status actions: available, maintenance, retired.
- Service records with sequence-generated references, cost/odometer validation, and lifecycle actions.
- Chatter tracking, search filters, grouping, role groups, and access-control CSV.
- Service history shown on each vehicle.

## Requirements
- Odoo 20.0 (manifest version is set to 20.0).
- `base` and `mail` installed.

## Installation
1. Copy `fleet_ops_suite` into an Odoo custom addons directory.
2. Add that directory to `addons_path` in `odoo.conf`.
3. Restart Odoo.
4. Enable developer mode, update the Apps list, and install **Fleet Operations Suite**.
5. Assign users to the **Fleet User** or **Fleet Manager** group.

## Demo workflow
1. Create a driver with a unique employee code and valid license expiry date.
2. Create a vehicle and assign the driver.
3. Create a service record for the vehicle.
4. Click **Start Service**, then **Complete**; verify the vehicle odometer and status.
5. Test duplicate registration numbers and negative odometer/cost values.

## Portfolio note
This repository is a starter implementation and should be installed and tested in your own Odoo instance before you claim it as production-ready. Add screenshots and a short demo video after validation.
