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
	_order = "date_attention desc"


	def button_closed(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'cerrada'}, context=context)
	
	_columns = {
		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict', readonly=True),
		'patient_photo': fields.related('patient_id', 'photo', type="binary", relation="doctor.patient", readonly=True),
		'date_attention': fields.datetime('Fecha de atencion', required=True, readonly=True),
		'origin': fields.char('Documento origen', size=64,
							  help="Reference of the document that produced this attentiont.", readonly=True),
		'professional_id': fields.many2one('doctor.professional', 'Profesional de la salud', required=True, readonly=True),
		'speciality': fields.related('professional_id', 'speciality_id', type="many2one", relation="doctor.speciality",
									 string='Especialidad', required=True, store=True),
		'professional_photo': fields.related('professional_id', 'photo', type="binary", relation="doctor.professional",
											 readonly=True, store=False),
		'age_attention': fields.integer('Edad actual', readonly=True),
		'age_unit': fields.selection([('1', u'Años'), ('2', 'Meses'), ('3', 'Dias'), ], 'Unidad de medida de la edad',
									 readonly=True),
		'diagnostico_medico':fields.text('Diagnostico medico', states={'cerrada': [('readonly', True)]}),
		'conducta_medico':fields.char('Conducta', states={'cerrada': [('readonly', True)]}),
		'notas_auxiliar_ids': fields.one2many('doctor.notas.auxiliar', 'attentiont_id', 'Notas', ondelete='restrict', states={'cerrada': [('readonly', True)]}),
		'signos_vitales_ids': fields.one2many('doctor.signos.vitales', 'attentiont_id', 'Tabla signos vitales', ondelete='restrict', states={'cerrada': [('readonly', True)]}),
		'state': fields.selection([('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 'Estado', readonly=True, required=True),
		'plantilla_aux_enfermeria_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas'),
	}

	def onchange_patient(self, cr, uid, ids, patient_id, context=None):
		values = {}
		if not patient_id:
			return values
		patient_data = self.pool.get('doctor.patient').browse(cr, uid, patient_id, context=context)
		photo_patient = patient_data.photo

		values.update({
			'patient_photo': photo_patient,
			'age_attention': 20

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



	def calcular_edad(self,fecha_nacimiento):
		current_date = datetime.today()
		st_birth_date = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
		re = current_date - st_birth_date
		dif_days = re.days
		age = dif_days
		age_unit = ''
		if age < 30:
			age_attention = age,
			age_unit = '3'

		elif age > 30 and age < 365:
			age = age / 30
			age = int(age)
			age_attention = age,
			age_unit = '2'

		elif age >= 365:
			age = int((current_date.year-st_birth_date.year-1) + (1 if (current_date.month, current_date.day) >= (st_birth_date.month, st_birth_date.day) else 0))
			age_attention = age,
			age_unit = '1'
		
		return age

	def calcular_age_unit(self,fecha_nacimiento):
		current_date = datetime.today()
		st_birth_date = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
		re = current_date - st_birth_date
		dif_days = re.days
		age = dif_days
		age_unit = ''
		if age < 30:
			age_unit = '3'
		elif age > 30 and age < 365:
			age_unit = '2'

		elif age >= 365:
			age_unit = '1'

		return age_unit


	def onchange_plantillas(self, cr, uid, ids, plantilla_id, campo, context=None):
		res={'value':{}}
		registros = []
		if plantilla_id:
			cuerpo = self.pool.get('doctor.attentions.recomendaciones').browse(cr,uid,plantilla_id,context=context).cuerpo
			fecha = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
			registros.append((0,0,{'name' : cuerpo, 'fecha_y_hora_nota': fecha}))

			res['value'][campo]=registros
		else:
			res['value'][campo]=''

		_logger.info(res)
		return res		


	_defaults = {
		'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
		'state': 'abierta',
	}

auxiliar_enfermeria()
