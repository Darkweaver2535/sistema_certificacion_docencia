from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models.usuario import Usuario
import os
import shutil
from datetime import datetime
from config import Config

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
    
    # Estadísticas generales simplificadas
    total_docentes = Docente.query.filter_by(activo=True).count()
    total_certificados = Certificado.query.count()
    docentes_sin_certificado = Docente.query.filter_by(activo=True).filter(
        ~Docente.id.in_(db.session.query(Certificado.docente_id))
    ).count()
    
    # Docentes recientes
    docentes_recientes = Docente.query.filter_by(activo=True).order_by(
        Docente.fecha_registro.desc()
    ).limit(5).all()
    
    return render_template('auth/dashboard.html',
                         total_docentes=total_docentes,
                         total_certificados=total_certificados,
                         docentes_sin_certificado=docentes_sin_certificado,
                         docentes_recientes=docentes_recientes)

@auth_bp.route('/respaldo/descargar')
@login_required
def descargar_respaldo():
    """Descarga un respaldo de la base de datos PostgreSQL"""
    try:
        # Crear carpeta de respaldos si no existe
        backup_dir = os.path.join(Config.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nombre del archivo de respaldo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'certificacion_backup_{timestamp}.sql'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Obtener credenciales de la base de datos desde la URI
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        
        # Ejecutar pg_dump para crear respaldo
        # Formato: postgresql://usuario:password@host:puerto/database
        import subprocess
        
        # Parsear la URI de la base de datos
        if db_uri.startswith('postgresql://'):
            # Extraer componentes de la URI
            import urllib.parse
            parsed = urllib.parse.urlparse(db_uri)
            
            db_host = parsed.hostname
            db_port = parsed.port or 5432
            db_user = parsed.username
            db_password = parsed.password
            db_name = parsed.path[1:]  # Quitar el '/' inicial
            
            # Crear el comando pg_dump
            env = os.environ.copy()
            env['PGPASSWORD'] = db_password
            
            cmd = [
                'pg_dump',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-d', db_name,
                '-F', 'p',  # Formato plain (SQL)
                '-f', backup_path
            ]
            
            # Ejecutar pg_dump
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                flash(f'Error al crear respaldo: {result.stderr}', 'danger')
                return redirect(url_for('auth.dashboard'))
            
            # Enviar archivo para descarga
            return send_file(
                backup_path,
                as_attachment=True,
                download_name=backup_filename,
                mimetype='application/sql'
            )
        else:
            flash('Tipo de base de datos no soportado para respaldos automáticos', 'warning')
            return redirect(url_for('auth.dashboard'))
            
    except Exception as e:
        flash(f'Error al generar respaldo: {str(e)}', 'danger')
        return redirect(url_for('auth.dashboard'))
