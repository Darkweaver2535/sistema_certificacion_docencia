from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.docente import Docente
from app.models.tipo_criterio import TipoCriterio
from app.models.docente_criterio import DocenteCriterio

criterios_bp = Blueprint('criterios', __name__, url_prefix='/criterios')

@criterios_bp.route('/docente/<int:docente_id>', methods=['GET', 'POST'])
@login_required
def gestionar(docente_id):
    """Gestiona los criterios de un docente específico"""
    docente = Docente.query.get_or_404(docente_id)
    
    if request.method == 'POST':
        # Obtener todos los tipos de criterios
        tipos_criterios = TipoCriterio.query.filter_by(activo=True).order_by(TipoCriterio.orden).all()
        
        # Procesar cada criterio
        for tipo_criterio in tipos_criterios:
            criterio_key = f'criterio_{tipo_criterio.id}'
            detalles_key = f'detalles_{tipo_criterio.id}'
            
            # Verificar si el checkbox está marcado
            tiene_criterio = request.form.get(criterio_key) == 'on'
            detalles = request.form.get(detalles_key, '').strip()
            
            # Buscar si ya existe la relación
            docente_criterio = DocenteCriterio.query.filter_by(
                docente_id=docente_id,
                tipo_criterio_id=tipo_criterio.id
            ).first()
            
            if tiene_criterio and detalles:
                # Crear o actualizar
                if docente_criterio:
                    # Actualizar detalles existentes
                    docente_criterio.detalles = detalles
                else:
                    # Crear nuevo
                    nuevo_criterio = DocenteCriterio(
                        docente_id=docente_id,
                        tipo_criterio_id=tipo_criterio.id,
                        detalles=detalles
                    )
                    db.session.add(nuevo_criterio)
            else:
                # Eliminar si existe y no está marcado o no tiene detalles
                if docente_criterio:
                    db.session.delete(docente_criterio)
        
        # Marcar docente para regeneración de certificado
        docente.requiere_regeneracion = True
        
        db.session.commit()
        
        flash('Criterios actualizados exitosamente', 'success')
        return redirect(url_for('docentes.ver', id=docente_id))
    
    # GET - Mostrar formulario
    tipos_criterios = TipoCriterio.query.filter_by(activo=True).order_by(TipoCriterio.orden).all()
    
    # Obtener criterios actuales del docente
    criterios_actuales = {}
    for dc in DocenteCriterio.query.filter_by(docente_id=docente_id).all():
        criterios_actuales[dc.tipo_criterio_id] = dc.detalles
    
    return render_template('criterios/gestionar.html', 
                         docente=docente,
                         tipos_criterios=tipos_criterios,
                         criterios_actuales=criterios_actuales)
