from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario para Flask-Login"""
    return Usuario.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario is None or not usuario.check_password(password):
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))
        
        if not usuario.activo:
            flash('Usuario inactivo. Contacte al administrador.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(usuario)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del administrador"""
    from app.models.docente import Docente
    from app.models.certificado import Certificado
    from app.models.unidad_academica import UnidadAcademica
    
    # Estadísticas generales
    total_docentes = Docente.query.filter_by(activo=True).count()
    total_certificados = Certificado.query.count()
    total_unidades = UnidadAcademica.query.filter_by(activo=True).count()
    docentes_sin_certificado = Docente.query.filter_by(activo=True).filter(
        ~Docente.id.in_(db.session.query(Certificado.docente_id))
    ).count()
    
    # Docentes por unidad académica
    unidades = UnidadAcademica.query.filter_by(activo=True).all()
    stats_unidades = []
    for unidad in unidades:
        count = Docente.query.filter_by(unidad_academica_id=unidad.id, activo=True).count()
        stats_unidades.append({
            'unidad': unidad,
            'count': count
        })
    
    # Docentes recientes
    docentes_recientes = Docente.query.filter_by(activo=True).order_by(
        Docente.fecha_registro.desc()
    ).limit(5).all()
    
    return render_template('auth/dashboard.html',
                         total_docentes=total_docentes,
                         total_certificados=total_certificados,
                         total_unidades=total_unidades,
                         docentes_sin_certificado=docentes_sin_certificado,
                         stats_unidades=stats_unidades,
                         docentes_recientes=docentes_recientes)
