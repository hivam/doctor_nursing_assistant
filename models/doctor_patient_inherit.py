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


class doctor_patient(osv.osv):

	_name = 'doctor.patient'

	_inherit = 'doctor.patient'


	_columns = {
		'attentions_aux_ids': fields.one2many('doctor.nursing.assistan', 'patient_id', 'Atenciones Aux de enfermeria'),
	}

	def atender_paciente_enfermera(self, cr, uid, ids, context=None):
		professional_id= self.pool.get('doctor.professional').browse(cr, uid, self.pool.get('doctor.professional').search(cr, uid, [( 'user_id',  '=', uid)]))[0].id
		for paciente in self.browse(cr,uid,ids):
			paciente_id = paciente.id
			context['default_patient_id'] = paciente_id
			context['default_professional_id'] = professional_id
			context['default_age_attention'] = self.calcular_edad(paciente.birth_date)
			context['default_age_unit'] = self.calcular_age_unit(paciente.birth_date)

			return {
				'type': 'ir.actions.act_window',
				'name': 'Hc Atencion enfermeria',
				'view_type': 'form',
				'view_mode': 'form',
				'res_id': False,
				'res_model': 'doctor.nursing.assistan',
				'context': context or None,
				'view_id': False,
				'nodestroy': False,
				'target': 'current'
			}

doctor_patient()