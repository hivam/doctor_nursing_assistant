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


class auxiliar_enfermeria(osv.osv):


	_name = 'doctor.nursing.assistan'


	_columns = {
		'patient_id': fields.many2one('doctor.patient', 'Patient', ondelete='restrict', readonly=True),
		'patient_photo': fields.related('patient_id', 'photo', type="binary", relation="doctor.patient", readonly=True),
		'professional_id': fields.many2one('doctor.professional', 'Doctor', required=True, readonly=True),
		'speciality': fields.related('professional_id', 'speciality_id', type="many2one", relation="doctor.speciality",
									 string='Speciality', required=True, store=True),
		'professional_photo': fields.related('professional_id', 'photo', type="binary", relation="doctor.professional",
											 readonly=True, store=False),
		'age_attention': fields.integer('Current age', readonly=True),
		'age_unit': fields.selection([('1', u'Años'), ('2', 'Meses'), ('3', 'Dias'), ], 'Unit of measure of age',
									 readonly=True),
		'diagnostico_medico':fields.char('Diagnostico medico'),
		'conducta_medico':fields.char('Conducta'),
		'notas_auxiliar_ids': fields.one2many('doctor.notas.auxiliar', 'attentiont_id', 'Notas', ondelete='restrict'),
		'signos_vitales_ids': fields.one2many('doctor.signos.vitales', 'attentiont_id', 'Tabla signos vitales', ondelete='restrict'),
	}

	def onchange_patient(self, cr, uid, ids, patient_id, context=None):
		values = {}
		if not patient_id:
			return values
		patient_data = self.pool.get('doctor.patient').browse(cr, uid, patient_id, context=context)
		photo_patient = patient_data.photo

		values.update({
			'patient_photo': photo_patient,
		})
		return {'value': values}

	def onchange_professional(self, cr, uid, ids, professional_id, context=None):
		values = {}
		if not professional_id:
			return values
		professional_data = self.pool.get('doctor.professional').browse(cr, uid, professional_id, context=context)
		professional_img = professional_data.photo
		if professional_data.speciality_id.id:
			professional_speciality = professional_data.speciality_id.id
			values.update({
				'speciality': professional_speciality,
			})

		values.update({
			'professional_photo': professional_img,
		})
		return {'value': values}


auxiliar_enfermeria()
