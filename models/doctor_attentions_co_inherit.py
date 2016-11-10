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
from lxml import etree
from openerp.osv.orm import setup_modifiers

class doctor_co_attentios(osv.osv):

	_name = 'doctor.attentions'

	_inherit = 'doctor.attentions'



	_columns = {
		'remite_aux_enfermeria': fields.boolean('Tratamiento con auxiliar de enfermeria'),
	}


	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		
		res = super(doctor_co_attentios, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
		doc = etree.XML(res['arch'])
		seleccionado = False
		for node in doc.xpath("//field[@name='remite_aux_enfermeria']"):

			modelo_buscar = self.pool.get('doctor.nursing.configuracion')
			record = modelo_buscar.search(cr, uid, [('name', '=', True)], context=context)
			if record:
				for datos in modelo_buscar.browse(cr, uid, record, context=context):
					seleccionado = datos.name
				node.set('invisible', repr(seleccionado))
				setup_modifiers(node, res['fields']['remite_aux_enfermeria'])
		
		res['arch'] = etree.tostring(doc)
				
		return res



	def metodo_write(self, cr, uid, ids, lista_uno, lista_dos, context=None):
		lista_diagnostico = []
		id_paciente = None
		nombre_diagnostico = ''

		if not 'patient_id' in lista_dos:
			if 'patient' in lista_dos:
				id_paciente = lista_dos['patient'] or None
		else:
			if 'patient_id' in lista_dos:
				id_paciente = lista_dos['patient_id'] or None


		for i in self.browse(cr, uid, ids, context=context):
			id_paciente = i.patient_id.id


		fecha_nacimiento =  self.pool.get('doctor.patient').browse(cr, uid, id_paciente, context=context).birth_date
		res={}
		res['patient_id'] =  id_paciente
		res['conducta_medico'] = lista_uno['conduct'] if 'conduct' in lista_uno else None
		res['age_attention'] = self.calcular_edad(fecha_nacimiento)
		res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)

		if 'diseases_ids' in lista_uno:
			for i in range(0,len(lista_uno['diseases_ids']),1):

				if isinstance(lista_uno['diseases_ids'][i][2], bool) != True:
					lista_diagnostico.append(lista_uno['diseases_ids'][i][2]['diseases_id'])
				else:
					diseases_ids = self.pool.get('doctor.attentions.diseases').search(cr, uid, [('attentiont_id', 'in', ids)], context=context)
					for i in self.pool.get('doctor.attentions.diseases').browse(cr, uid, diseases_ids, context=context):
						if i.diseases_id.id not in lista_diagnostico:
							lista_diagnostico.append(i.diseases_id.id)


			lista_diagnostico = list(set(lista_diagnostico))				

			if len(lista_diagnostico) > 0:
				for i in lista_diagnostico:
					nombre_diagnostico += '\n' + self.pool.get('doctor.diseases').browse(cr, uid, i, context=context).name

				res['diagnostico_medico'] = nombre_diagnostico
		

		number = self.browse(cr, uid, ids[0], context=context).number
		res['origin'] = number

		ids_attencion_vieja = self.pool.get('doctor.nursing.assistan').search(cr, uid, [('origin', '=', number)], context=context)
		id_attention = None
		for i in self.pool.get('doctor.nursing.assistan').browse(cr, uid, ids_attencion_vieja, context=context):
			id_attention = i.id



		self.pool.get('doctor.nursing.assistan').write(cr, uid, id_attention, res, context)


	def metodo_create(self, cr, uid, lista_uno, lista_dos, context=None):
		_logger.info(context)
		lista_diagnostico = []
		id_paciente = None
		nombre_diagnostico = ''
		if not 'patient_id' in lista_dos:
			id_paciente = lista_dos['default_patient_id']
		else:
			id_paciente = lista_dos['patient_id']

		fecha_nacimiento =  self.pool.get('doctor.patient').browse(cr, uid, id_paciente, context=context).birth_date
		res={}
		res['patient_id'] =  id_paciente
		res['conducta_medico'] = lista_uno['conduct'] if 'conduct' in lista_uno else None
		res['age_attention'] = self.calcular_edad(fecha_nacimiento)
		res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)
		if 'diseases_ids' in lista_uno:
			for i in range(0,len(lista_uno['diseases_ids']),1):
				lista_diagnostico.append(lista_uno['diseases_ids'][i][2]['diseases_id'])
						
			if len(lista_diagnostico) > 0:
				for i in lista_diagnostico:
					nombre_diagnostico += '\n' + self.pool.get('doctor.diseases').browse(cr, uid, i, context=context).name

				res['diagnostico_medico'] = nombre_diagnostico
		res['origin'] = lista_uno['number']
		self.pool.get('doctor.nursing.assistan').create(cr, uid, res, context)


	def write(self, cr, uid, ids, vals, context=None):

		ejcutar_write = None
		modulo_predeterminado = self.pool.get('doctor.nursing.configuracion')
		bandera_id = modulo_predeterminado.search(cr, uid, [('name', '=', True)], context=context)
		if bandera_id:
			for i in modulo_predeterminado.browse(cr, uid, bandera_id, context=context):
				bandera_id = i.name
			if bandera_id:
				ejcutar_write = super(doctor_co_attentios,self).write(cr, uid, ids, vals, context)
				self.metodo_write(cr, uid, ids, vals, context, context=context)

		if 'remite_aux_enfermeria' in vals:
			if vals['remite_aux_enfermeria']:
				ejcutar_write = super(doctor_co_attentios,self).write(cr, uid, ids, vals, context)
				self.metodo_write(cr, uid, ids, vals, context, context=context)
			else:
				return super(doctor_co_attentios,self).write(cr, uid, ids, vals, context)
		else:
			return super(doctor_co_attentios,self).write(cr, uid, ids, vals, context)
		return ejcutar_write


	def create(self, cr, uid, vals, context=None):
		ejcutar_create = None
		modulo_predeterminado = self.pool.get('doctor.nursing.configuracion')
		bandera_id = modulo_predeterminado.search(cr, uid, [('name', '=', True)], context=context)
		if bandera_id:
			for i in modulo_predeterminado.browse(cr, uid, bandera_id, context=context):
				bandera_id = i.name
			if bandera_id:
				ejcutar_create = super(doctor_co_attentios,self).create(cr, uid, vals, context)
				self.metodo_create(cr, uid, vals, context, context=context)

		if 'remite_aux_enfermeria' in vals:
			if vals['remite_aux_enfermeria']:
				ejcutar_create = super(doctor_co_attentios,self).create(cr, uid, vals, context)
				self.metodo_create(cr, uid, vals, context, context=context)
			else:
				return super(doctor_co_attentios,self).create(cr, uid, vals, context)
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