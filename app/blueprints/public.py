from flask import Blueprint, render_template, abort
from app.models.certificado import Certificado

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Página de inicio pública"""
    return render_template('public/index.html')

@public_bp.route('/verificar/<codigo>')
def verificar(codigo):
    """Verificación pública de certificado mediante código QR"""
    certificado = Certificado.query.filter_by(codigo_unico=codigo).first()
    
    if not certificado:
        abort(404)
    
    if not certificado.valido:
        return render_template('public/verificar.html', 
                             certificado=None, 
                             error='Certificado no válido o revocado')
    
    return render_template('public/verificar.html', certificado=certificado)
