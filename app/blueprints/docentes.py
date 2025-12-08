from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models.docente import Docente
from app.models.docente_criterio import DocenteCriterio
import pandas as pd
import os
from datetime import datetime
from config import Config

docentes_bp = Blueprint('docentes', __name__, url_prefix='/docentes')

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@docentes_bp.route('/')
@login_required
def listar():
    """Lista todos los criterios de docentes con paginación y búsqueda"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    # Cambiar a listar criterios en lugar de docentes
    query = DocenteCriterio.query.join(DocenteCriterio.docente).filter(Docente.activo == True)
    
    # Filtro de búsqueda por nombre de docente
    if search:
        query = query.filter(
            db.or_(
                Docente.nombres.ilike(f'%{search}%'),
                Docente.apellidos.ilike(f'%{search}%')
            )
        )
    
    # Paginación ordenada por apellido y nombre de docente
    pagination = query.join(DocenteCriterio.tipo_criterio).order_by(
        Docente.apellidos, Docente.nombres, DocenteCriterio.tipo_criterio_id
    ).paginate(page=page, per_page=15, error_out=False)
    
    criterios = pagination.items
    
    return render_template('docentes/listar.html', 
                         criterios=criterios, 
                         pagination=pagination,
                         search=search)

@docentes_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crea un nuevo docente y redirige a gestión de criterios"""
    if request.method == 'POST':
        # Crear nuevo docente (solo nombres y apellidos)
        docente = Docente(
            nombres=request.form.get('nombres'),
            apellidos=request.form.get('apellidos'),
            requiere_regeneracion=True
        )
        
        db.session.add(docente)
        db.session.commit()
        
        flash(f'Docente {docente.nombre_completo} creado exitosamente. Ahora agregue los criterios.', 'success')
        # Redirigir directamente a gestión de criterios
        return redirect(url_for('criterios.gestionar', docente_id=docente.id))
    
    return render_template('docentes/crear.html')

@docentes_bp.route('/<int:id>')
@login_required
def ver(id):
    """Muestra el detalle de un docente"""
    docente = Docente.query.get_or_404(id)
    criterios = DocenteCriterio.query.filter_by(docente_id=id).all()
    
    return render_template('docentes/ver.html', docente=docente, criterios=criterios)

@docentes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita un docente existente"""
    docente = Docente.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizar datos (solo nombres y apellidos)
        docente.nombres = request.form.get('nombres')
        docente.apellidos = request.form.get('apellidos')
        docente.requiere_regeneracion = True
        
        db.session.commit()
        
        flash(f'Docente {docente.nombre_completo} actualizado exitosamente', 'success')
        return redirect(url_for('docentes.ver', id=docente.id))
    
    return render_template('docentes/editar.html', docente=docente)

@docentes_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Elimina (desactiva) un docente"""
    docente = Docente.query.get_or_404(id)
    docente.activo = False
    db.session.commit()
    
    flash(f'Docente {docente.nombre_completo} eliminado exitosamente', 'info')
    return redirect(url_for('docentes.listar'))

@docentes_bp.route('/importar', methods=['GET', 'POST'])
@login_required
def importar():
    """Importa docentes desde archivo Excel/CSV"""
    if request.method == 'POST':
        # Verificar si se subió un archivo
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        
        file = request.files['archivo']
        
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Procesar archivo
            try:
                # Leer archivo con pandas
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                
                # Validar columnas requeridas
                columnas_requeridas = ['nombres', 'apellidos', 'ci', 'unidad_codigo', 'cargo', 'años_servicio']
                columnas_opcionales = ['email', 'telefono']
                
                for col in columnas_requeridas:
                    if col not in df.columns:
                        flash(f'Falta la columna requerida: {col}', 'danger')
                        return redirect(url_for('docentes.importar'))
                
                # Procesar cada fila
                exitosos = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        # Validar CI único
                        ci = str(row['ci']).strip()
                        if Docente.query.filter_by(ci=ci).first():
                            errores.append(f"Fila {idx+2}: CI {ci} ya existe")
                            continue
                        
                        # Buscar unidad académica
                        unidad = UnidadAcademica.query.filter_by(codigo=row['unidad_codigo']).first()
                        if not unidad:
                            errores.append(f"Fila {idx+2}: Unidad {row['unidad_codigo']} no existe")
                            continue
                        
                        # Crear docente
                        docente = Docente(
                            nombres=row['nombres'],
                            apellidos=row['apellidos'],
                            ci=ci,
                            unidad_academica_id=unidad.id,
                            cargo=row['cargo'],
                            años_servicio=int(row['años_servicio']) if pd.notna(row['años_servicio']) else None,
                            email=row.get('email', ''),
                            telefono=row.get('telefono', ''),
                            requiere_regeneracion=True
                        )
                        
                        db.session.add(docente)
                        exitosos += 1
                    
                    except Exception as e:
                        errores.append(f"Fila {idx+2}: {str(e)}")
                
                db.session.commit()
                
                flash(f'Importación completada: {exitosos} docentes importados exitosamente', 'success')
                if errores:
                    flash(f'{len(errores)} errores encontrados. Revise el log.', 'warning')
                    for error in errores[:10]:  # Mostrar solo los primeros 10 errores
                        flash(error, 'danger')
                
                return redirect(url_for('docentes.listar'))
            
            except Exception as e:
                flash(f'Error al procesar el archivo: {str(e)}', 'danger')
                return redirect(url_for('docentes.importar'))
        
        else:
            flash('Tipo de archivo no permitido. Use Excel (.xlsx, .xls) o CSV (.csv)', 'danger')
            return redirect(request.url)
    
    return render_template('docentes/importar.html')

@docentes_bp.route('/template')
@login_required
def descargar_template():
    """Descarga plantilla de importación"""
    # Crear DataFrame con columnas de ejemplo
    data = {
        'nombres': ['Juan', 'María'],
        'apellidos': ['Pérez López', 'García Rojas'],
        'ci': ['12345678', '87654321'],
        'unidad_codigo': ['UALP', 'UACB'],
        'cargo': ['Docente Titular', 'Docente Asociado'],
        'años_servicio': [10, 5],
        'email': ['juan.perez@emi.edu.bo', 'maria.garcia@emi.edu.bo'],
        'telefono': ['70123456', '71234567']
    }
    
    df = pd.DataFrame(data)
    
    # Guardar en archivo temporal
    filepath = os.path.join(Config.UPLOAD_FOLDER, 'template_importacion_docentes.xlsx')
    df.to_excel(filepath, index=False)
    
    return send_file(filepath, as_attachment=True, download_name='template_importacion_docentes.xlsx')
