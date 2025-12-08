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
            Docente.nombre_completo.ilike(f'%{search}%')
        )
    
    # Paginación ordenada por nombre completo de docente
    pagination = query.join(DocenteCriterio.tipo_criterio).order_by(
        Docente.nombre_completo, DocenteCriterio.tipo_criterio_id
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
        # Crear nuevo docente
        docente = Docente(
            nombre_completo=request.form.get('nombre_completo'),
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
        # Actualizar datos
        docente.nombre_completo = request.form.get('nombre_completo')
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
                
                # Validar columna requerida
                if 'nombre_completo' not in df.columns:
                    flash('Falta la columna requerida: nombre_completo', 'danger')
                    return redirect(url_for('docentes.importar'))
                
                # Procesar cada fila
                exitosos = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        nombre = str(row['nombre_completo']).strip()
                        
                        if not nombre:
                            errores.append(f"Fila {idx+2}: nombre_completo vacío")
                            continue
                        
                        # Crear docente
                        docente = Docente(
                            nombre_completo=nombre,
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
    # Crear DataFrame con columna de ejemplo
    data = {
        'nombre_completo': [
            'Juan Pérez López',
            'María García Rojas',
            'Carlos Rodríguez Mamani'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Guardar en archivo temporal
    filepath = os.path.join(Config.UPLOAD_FOLDER, 'template_importacion_docentes.xlsx')
    df.to_excel(filepath, index=False)
    
    return send_file(filepath, as_attachment=True, download_name='template_importacion_docentes.xlsx')
