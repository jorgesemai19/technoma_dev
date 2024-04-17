# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta, date

import logging

_logger = logging.getLogger(__name__)


class AccountAnalyticLineInh(models.Model):
    _inherit = 'account.analytic.line'

    is_used_hours = fields.Boolean(
        string='is used hours?',
        required=False)
    is_holiday = fields.Boolean(string="Is Holiday", compute='_check_holiday_or_sunday')
    is_sunday = fields.Boolean(string="Is Sunday", compute='_check_holiday_or_sunday')
    is_saturday = fields.Boolean(string="Is Saturday", compute='_check_holiday_or_sunday')
    overtime_hours = fields.Float(
        string='Overtime Hours',
        compute='_compute_overtime_hours',
        store=True,
        readonly=True
    )

    @api.depends('time_start', 'time_stop', 'date')
    def _compute_overtime_hours(self):
        for record in self:
            if record.time_start is not False and record.time_stop is not False:
                time_start = record.time_start
                time_stop = record.time_stop
                if record.is_sunday or record.is_holiday:
                    overtime_hours = time_stop - time_start
                else:
                    if record.is_saturday:
                        work_start_time = 8.0  # Representing 8:00 AM
                        work_end_time = 12.0  # Representing 12:00 PM
                    else:
                        work_start_time = 9.0  # Representing 9:00 AM
                        work_end_time = 18.0  # Representing 6:00 PM
                    ov1 = 0.0
                    ov2 = 0.0
                    overtime_hours = 0.0

                    if time_stop < time_start:
                        time_stop += 24.0  # Adding 24 hours to make it next day's time

                    if time_start < work_start_time:
                        if time_stop < work_start_time:
                            ov1 = time_stop - time_start
                        else:
                            ov1 = work_start_time - time_start
                            if time_stop > work_end_time:
                                ov2 = time_stop - work_end_time
                            else:
                                ov2 = 0.0
                        overtime_hours = ov1 + ov2
                    else:
                        if time_start > work_end_time:
                            overtime_hours = time_stop - time_start
                        else:
                            overtime_hours = time_stop - work_end_time
            else:
                overtime_hours = 0.0

            if overtime_hours < 0.0:
                record.overtime_hours = 0.0
            else:
                record.overtime_hours = overtime_hours

    @api.depends('date')
    def _check_holiday_or_sunday(self):
        for record in self:
            holiday_dates = [
                datetime(2024, 1, 1).date(),  # New Year's Day
                datetime(2024, 3, 1).date(),  # Day of Heroes
                datetime(2024, 3, 28).date(),  # Maundy Thursday (Jueves Santo)
                datetime(2024, 3, 29).date(),  # Good Friday (Viernes Santo)
                datetime(2024, 5, 1).date(),  # Labor Day
                datetime(2024, 5, 14).date(),  # Independence Day
                datetime(2024, 5, 15).date(),  # Independence Day
                datetime(2024, 6, 10).date(),  # Chaco Armistice Day
                datetime(2024, 8, 15).date(),  # Fundacion de Asuncion
                datetime(2024, 9, 29).date(),  # Batalla de Boqueron
                datetime(2024, 12, 8).date(),  # Virgin of Caacupé Day
                datetime(2024, 12, 25).date()  # Christmas Day
            ]
            # Check if the date is in the list of holiday dates
            _logger.warning('*************************')
            _logger.warning(record.date)
            _logger.warning(holiday_dates)
            if record.date in holiday_dates:
                record.is_holiday = True
            else:
                record.is_holiday = False

            # Check if the date is a Sunday
            if record.date.weekday() == 6:
                record.is_sunday = True
            else:
                record.is_sunday = False

            # Check if the date is a Saturday
            if record.date.weekday() == 5:
                record.is_saturday = True
            else:
                record.is_saturday = False

