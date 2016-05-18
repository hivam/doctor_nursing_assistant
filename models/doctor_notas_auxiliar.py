# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
_logger = logging.getLogger(__name__)
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import date, datetime, timedelta


class doctor_notas_auxiliar(osv.osv):


	_name = 'doctor.notas.auxiliar'


	_columns = {
		'name': fields.char("Nota"),
		'fecha_y_hora_nota': fields.datetime('Fecha y hora'),
		'attentiont_id': fields.many2one('doctor.nursing.assistan', 'Attention', ondelete='restrict'),
		'patient_id': fields.many2one('doctor.patient', 'Patient', ondelete='restrict'),
	}


	_defaults = {
		'fecha_y_hora_nota': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
	}



	

doctor_notas_auxiliar()
