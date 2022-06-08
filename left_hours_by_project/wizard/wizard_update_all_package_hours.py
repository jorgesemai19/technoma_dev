# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api,_
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class UpdateAllRecordTransientModel(models.TransientModel):
    _name = "update.all.package.hours"
    _description = "Update all hours package"

    @api.multi
    def update_all_package_hours(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        update = self.env['hours.package'].browse(active_ids)
        for p in update:
            p.get_hours_used_and_available()
