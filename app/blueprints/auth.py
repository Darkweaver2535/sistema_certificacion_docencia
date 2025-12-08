from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models.usuario import Usuario
import os
import shutil
from datetime import datetime
from config import Config, BASE_DIR

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
    """Descarga un respaldo de la base de datos"""
    try:
        # Crear carpeta de respaldos si no existe
        backup_dir = os.path.join(BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nombre del archivo de respaldo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Obtener la URI de la base de datos
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        
        # Verificar el tipo de base de datos
        if db_uri.startswith('sqlite:///'):
            # Para SQLite, simplemente copiar el archivo
            db_path = db_uri.replace('sqlite:///', '')
            
            if not os.path.exists(db_path):
                flash('No se encontró el archivo de base de datos.', 'danger')
                return redirect(url_for('auth.dashboard'))
            
            backup_filename = f'certificacion_backup_{timestamp}.db'
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copiar el archivo de base de datos
            shutil.copy2(db_path, backup_path)
            
            flash('Respaldo SQLite generado exitosamente.', 'success')
            return send_file(
                backup_path,
                as_attachment=True,
                download_name=backup_filename,
                mimetype='application/x-sqlite3'
            )
            
        elif db_uri.startswith('postgresql://'):
            # Para PostgreSQL, usar pg_dump
            import subprocess
            import urllib.parse
            
            backup_filename = f'certificacion_backup_{timestamp}.sql'
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Parsear la URI de la base de datos
            parsed = urllib.parse.urlparse(db_uri)
            
            db_host = parsed.hostname
            db_port = parsed.port or 5432
            db_user = parsed.username
            db_password = parsed.password
            db_name = parsed.path[1:]  # Quitar el '/' inicial
            
            # Verificar que pg_dump esté disponible
            try:
                subprocess.run(['pg_dump', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                flash('pg_dump no está disponible en el sistema. Por favor, instale PostgreSQL client tools.', 'danger')
                return redirect(url_for('auth.dashboard'))
            
            # Crear el comando pg_dump
            env = os.environ.copy()
            if db_password:
                env['PGPASSWORD'] = db_password
            
            cmd = [
                'pg_dump',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-d', db_name,
                '-F', 'p',  # Formato plain (SQL)
                '-f', backup_path,
                '--no-owner',  # No incluir comandos de propiedad
                '--no-acl'     # No incluir comandos de ACL
            ]
            
            # Ejecutar pg_dump
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                error_msg = result.stderr or 'Error desconocido al crear respaldo'
                flash(f'Error al crear respaldo: {error_msg}', 'danger')
                return redirect(url_for('auth.dashboard'))
            
            # Verificar que el archivo se creó
            if not os.path.exists(backup_path) or os.path.getsize(backup_path) == 0:
                flash('El archivo de respaldo está vacío o no se pudo crear.', 'danger')
                return redirect(url_for('auth.dashboard'))
            
            flash('Respaldo PostgreSQL generado exitosamente.', 'success')
            return send_file(
                backup_path,
                as_attachment=True,
                download_name=backup_filename,
                mimetype='application/sql'
            )
        else:
            flash('Tipo de base de datos no soportado para respaldos automáticos.', 'warning')
            return redirect(url_for('auth.dashboard'))
            
    except subprocess.TimeoutExpired:
        flash('El respaldo tardó demasiado tiempo. Intente nuevamente.', 'danger')
        return redirect(url_for('auth.dashboard'))
    except Exception as e:
        flash(f'Error al generar respaldo: {str(e)}', 'danger')
        return redirect(url_for('auth.dashboard'))
