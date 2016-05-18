# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name'        : 'Doctor_nursing_assistant',
    'version'     : '1.0',
    'summary'     : 'Create historia clinica de auxiliar de enfermeria',
    'description' : 'Doctor_nursing_assistant agrega la posibilidad de que el doctor cuente con una auxiliar de enfermeria',
    'category'    : 'medical',
    'author'      : 'Proyecto Evoluzion',
    'website'     : 'http://www.proyectoevoluzion.com/',
    'license'     : 'AGPL-3',
    'depends'     : ['doctor', 'l10n_co_doctor'],
    'data'        : [
                    'security/ir.model.access.csv',
                    'views/doctor_nursing_assistant_view.xml',
                    'views/doctor_notas_auxiliar_view.xml',
                    'views/doctor_signos_vitales_view.xml',
                    'views/doctor_attentions_inherit_view.xml',  
                    'views/doctor_patient_inherit_view.xml', 
    ],      
    'installable' : True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
