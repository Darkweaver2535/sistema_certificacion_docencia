from flask import Blueprint, render_template, redirect, url_for, flash, send_file, abort, current_app
from flask_login import login_required
from app import db
from app.models.docente import Docente
from app.models.certificado import Certificado
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
@certificados_bp.route('/generar/<int:docente_id>/<formato>')
@login_required
def generar(docente_id, formato='pdf'):
    """Genera un certificado para un docente en formato PDF o DOCX"""
    docente = Docente.query.get_or_404(docente_id)
    
    # Verificar si tiene criterios
    if not docente.criterios.count():
        flash('El docente no tiene criterios registrados. Agregue criterios antes de generar el certificado.', 'warning')
        return redirect(url_for('docentes.ver', id=docente_id))
    
    try:
        generator = CertificadoGenerator(docente)
        
        if formato.lower() == 'docx':
            # Generar solo Word
            docx_path, codigo = generator.generar_certificado_docx()
            flash(f'Certificado Word generado exitosamente para {docente.nombre_completo}', 'success')
            return send_file(docx_path, as_attachment=True, 
                            download_name=f'certificado_{docente.ci}.docx')
        else:
            # Generar PDF (primero Word, luego conversión)
            archivo_path = generator.generar_certificado_pdf()
            
            # Determinar extensión del archivo generado
            extension = 'pdf' if archivo_path.endswith('.pdf') else 'docx'
            
            if extension == 'docx':
                flash(f'Certificado generado como Word (conversión a PDF no disponible en este servidor)', 'warning')
            else:
                flash(f'Certificado PDF generado exitosamente para {docente.nombre_completo}', 'success')
            
            return send_file(archivo_path, as_attachment=True, 
                            download_name=f'certificado_{docente.ci}.{extension}')
    
    except Exception as e:
        flash(f'Error al generar el certificado: {str(e)}', 'danger')
        return redirect(url_for('docentes.ver', id=docente_id))

@certificados_bp.route('/descargar/<int:id>')
@login_required
def descargar(id):
    """Descarga un certificado existente"""
    certificado = Certificado.query.get_or_404(id)
    
    try:
        # Si requiere regeneración, generar nuevamente
        if certificado.docente.requiere_regeneracion:
            generator = CertificadoGenerator(certificado.docente)
            pdf_path = generator.generar_certificado_pdf()
        else:
            # Buscar archivo existente
            pdf_path = os.path.join(
                current_app.config['QR_FOLDER'],
                f'certificado_{certificado.codigo_unico}.pdf'
            )
            
            # Si no existe, regenerar
            if not os.path.exists(pdf_path):
                generator = CertificadoGenerator(certificado.docente)
                pdf_path = generator.generar_certificado_pdf()
        
        return send_file(pdf_path, as_attachment=True, 
                        download_name=f'certificado_{certificado.docente.ci}.pdf')
    
    except Exception as e:
        flash(f'Error al descargar el certificado: {str(e)}', 'danger')
        return redirect(url_for('certificados.listar'))

@certificados_bp.route('/regenerar/<int:id>')
@login_required
def regenerar(id):
    """Fuerza la regeneración de un certificado"""
    certificado = Certificado.query.get_or_404(id)
    
    try:
        generator = CertificadoGenerator(certificado.docente)
        pdf_path = generator.generar_certificado_pdf()
        
        flash(f'Certificado regenerado exitosamente', 'success')
        return send_file(pdf_path, as_attachment=True, 
                        download_name=f'certificado_{certificado.docente.ci}.pdf')
    
    except Exception as e:
        flash(f'Error al regenerar el certificado: {str(e)}', 'danger')
        return redirect(url_for('certificados.listar'))
