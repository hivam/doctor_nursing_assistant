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


class doctor_co_attentios(osv.osv):

	_name = 'doctor.attentions'

	_inherit = 'doctor.attentions'

	_columns = {
		'remite_aux_enfermeria': fields.boolean('Tratamiento con auxiliar de enfermeria'),
		'aux_enfermeria_id': fields.many2one('doctor.professional', 'Aux. Enfermeria', domain="[('speciality_id.name','=','Auxiliar de enfermeria')]"),
	}



	def create(self, cr, uid, vals, context=None):
		lista_diagnostico = []
		id_paciente = None
		nombre_diagnostico = ''
		id_especialidad = self.pool.get('doctor.professional').browse(cr, uid, vals['aux_enfermeria_id'], context=context).speciality_id.id
		if not 'patient_id' in vals:
			id_paciente = context['default_patient_id']
		else:
			id_paciente = vals['patient_id']

		fecha_nacimiento =  self.pool.get('doctor.patient').browse(cr, uid, id_paciente, context=context).birth_date
		res={}
		res['patient_id'] =  id_paciente
		res['professional_id'] = vals['aux_enfermeria_id']
		res['conducta_medico'] = vals['conduct']
		res['speciality'] = id_especialidad
		res['age_attention'] = self.calcular_edad(fecha_nacimiento)
		res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)
		
		ejcutar_create = super(doctor_co_attentios,self).create(cr, uid, vals, context)

		if 'diseases_ids' in vals:
			for i in range(0,len(vals['diseases_ids']),1):
				lista_diagnostico.append(vals['diseases_ids'][i][2]['diseases_id'])
				
			if len(lista_diagnostico) > 0:
				for i in lista_diagnostico:

					nombre_diagnostico += '\n' + self.pool.get('doctor.diseases').browse(cr, uid, i, context=context).name

			res['diagnostico_medico'] = nombre_diagnostico
			
		res['origin'] = vals['number']
		self.pool.get('doctor.nursing.assistan').create(cr, uid, res, context)
		return ejcutar_create

doctor_co_attentios()