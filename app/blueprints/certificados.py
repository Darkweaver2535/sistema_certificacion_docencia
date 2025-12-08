from flask import Blueprint, render_template, redirect, url_for, flash, send_file, abort, current_app
from flask_login import login_required
from app import db
from app.models.docente import Docente
from app.models.certificado import Certificado
from app.models.docente_criterio import DocenteCriterio
from app.utils import CertificadoGenerator
import os

certificados_bp = Blueprint('certificados', __name__, url_prefix='/certificados')

@certificados_bp.route('/')
@login_required
def listar():
    """Lista todos los certificados generados"""
    certificados = Certificado.query.join(Certificado.docente).order_by(
        Certificado.fecha_generacion.desc()
    ).all()
    
    return render_template('certificados/listar.html', certificados=certificados)

@certificados_bp.route('/generar/<int:docente_id>')
@login_required
def generar(docente_id):
    """Genera certificados para todos los criterios del docente"""
    docente = Docente.query.get_or_404(docente_id)
    
    # Verificar si tiene criterios
    if not docente.criterios.count():
        flash('El docente no tiene criterios registrados. Agregue criterios antes de generar certificados.', 'warning')
        return redirect(url_for('docentes.ver', id=docente_id))
    
    try:
        certificados_generados = 0
        
        # Generar un certificado por cada criterio
        for docente_criterio in docente.criterios:
            # Verificar si ya existe certificado para este criterio
            cert_existente = Certificado.query.filter_by(
                docente_criterio_id=docente_criterio.id
            ).first()
            
            if not cert_existente:
                generator = CertificadoGenerator(docente_criterio)
                generator.generar_certificado()
                certificados_generados += 1
        
        if certificados_generados > 0:
            flash(f'Se generaron {certificados_generados} certificados para {docente.nombre_completo}', 'success')
        else:
            flash(f'Todos los certificados ya están generados para {docente.nombre_completo}', 'info')
        
        return redirect(url_for('certificados.listar'))
    
    except Exception as e:
        flash(f'Error al generar certificados: {str(e)}', 'danger')
        return redirect(url_for('docentes.ver', id=docente_id))

@certificados_bp.route('/descargar-qr/<int:id>')
@login_required
def descargar_qr(id):
    """Descarga el código QR de un certificado"""
    certificado = Certificado.query.get_or_404(id)
    
    try:
        if certificado.qr_path and os.path.exists(certificado.qr_path):
            return send_file(certificado.qr_path, as_attachment=True, 
                            download_name=f'qr_{certificado.codigo_unico}.png')
        else:
            flash('El código QR no existe. Regenere el certificado.', 'warning')
            return redirect(url_for('certificados.listar'))
    
    except Exception as e:
        flash(f'Error al descargar el QR: {str(e)}', 'danger')
        return redirect(url_for('certificados.listar'))

@certificados_bp.route('/regenerar/<int:id>')
@login_required
def regenerar(id):
    """Fuerza la regeneración de un certificado específico"""
    certificado = Certificado.query.get_or_404(id)
    
    try:
        # Eliminar el certificado existente
        db.session.delete(certificado)
        db.session.commit()
        
        # Regenerar
        generator = CertificadoGenerator(certificado.docente_criterio)
        nuevo_cert = generator.generar_certificado()
        
        flash(f'Certificado {nuevo_cert.codigo_emi} regenerado exitosamente', 'success')
        return redirect(url_for('certificados.listar'))
    
    except Exception as e:
        flash(f'Error al regenerar el certificado: {str(e)}', 'danger')
        return redirect(url_for('certificados.listar'))

@certificados_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    """Elimina un certificado"""
    certificado = Certificado.query.get_or_404(id)
    
    try:
        # Eliminar archivo QR si existe
        if certificado.qr_path and os.path.exists(certificado.qr_path):
            os.remove(certificado.qr_path)
        
        db.session.delete(certificado)
        db.session.commit()
        
        flash('Certificado eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el certificado: {str(e)}', 'danger')
    
    return redirect(url_for('certificados.listar'))
