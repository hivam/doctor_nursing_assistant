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
	}



	def write(self, cr, uid, ids, vals, context=None):
		lista_diagnostico = []
		id_paciente = None
		nombre_diagnostico = ''
		ejcutar_write = None

		if 'remite_aux_enfermeria' in vals:
			if vals['remite_aux_enfermeria']:
		
				if not 'patient_id' in vals:
					id_paciente = context['default_patient_id']
				else:
					id_paciente = vals['patient_id']

				fecha_nacimiento =  self.pool.get('doctor.patient').browse(cr, uid, id_paciente, context=context).birth_date
				res={}
				res['patient_id'] =  id_paciente
				res['conducta_medico'] = vals['conduct']
				res['age_attention'] = self.calcular_edad(fecha_nacimiento)
				res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)

				ejcutar_write = super(doctor_co_attentios,self).write(cr, uid, ids, vals, context)

				if 'diseases_ids' in vals:
					for i in range(0,len(vals['diseases_ids']),1):
						lista_diagnostico.append(vals['diseases_ids'][i][2]['diseases_id'])
						
					if len(lista_diagnostico) > 0:
						for i in lista_diagnostico:

							nombre_diagnostico += '\n' + self.pool.get('doctor.diseases').browse(cr, uid, i, context=context).name

					res['diagnostico_medico'] = nombre_diagnostico
					
				res['origin'] = vals['number']
				self.pool.get('doctor.nursing.assistan').create(cr, uid, res, context)
			else:
				return super(doctor_co_attentios,self).write(cr, uid, ids, vals, context)
		
		return ejcutar_create


	def create(self, cr, uid, vals, context=None):
		lista_diagnostico = []
		id_paciente = None
		nombre_diagnostico = ''
		ejcutar_create = None
		_logger.info(context)
		if 'remite_aux_enfermeria' in vals:
			if vals['remite_aux_enfermeria']:
				#id_especialidad = self.pool.get('doctor.professional').browse(cr, uid, vals['aux_enfermeria_id'], context=context).speciality_id.id
				if not 'patient_id' in context:
					id_paciente = context['default_patient_id']
				else:
					id_paciente = context['patient_id']

				fecha_nacimiento =  self.pool.get('doctor.patient').browse(cr, uid, id_paciente, context=context).birth_date
				res={}
				res['patient_id'] =  id_paciente
				#res['professional_id'] = vals['aux_enfermeria_id']
				res['conducta_medico'] = vals['conduct']
				#res['speciality'] = id_especialidad
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
			else:
				return super(doctor_co_attentios,self).create(cr, uid, vals, context)
		
		return ejcutar_create



	def onchange_domain_auxiliar(self,cr,uid,ids,context=None):
		res={'value':{}}
		lista_usuarios = []
		aux_enfermeria_grupo_id = self.pool.get('res.groups').search(cr, uid, [('name', '=', 'Aux. enfermeria')], context=context)
		
		cr.execute("SELECT uid FROM res_groups_users_rel WHERE gid = %s" %(aux_enfermeria_grupo_id[0]))
		
		for i in cr.fetchall():
			lista_usuarios.append(i[0])


		_logger.info(lista_usuarios)
		dominio=''
		dominio=[('user_id','in',lista_usuarios)]
		#repr
		res.setdefault('domain', {})
		res['domain']['aux_enfermeria_id']=repr(dominio)
		return res

doctor_co_attentios()