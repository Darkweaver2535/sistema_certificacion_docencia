import os
import secrets
import hashlib
import hmac
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx2pdf import convert
import qrcode
from flask import current_app, request
from app.models.certificado import Certificado
from app.models.docente_criterio import DocenteCriterio
from app.models.tipo_criterio import TipoCriterio
from app import db

class CertificadoGenerator:
    """Generador de certificados PDF con clonación dinámica de tablas"""
    
    def __init__(self, docente):
        self.docente = docente
        self.template_path = current_app.config['CERTIFICATE_TEMPLATE']
        self.qr_folder = current_app.config['QR_FOLDER']
        self.salt = current_app.config['CERTIFICATE_SALT']
    
    def generar_codigo_unico(self):
        """
        Genera un código único alfanumérico en formato ABCD-1234-EFGH
        usando HMAC-SHA256 para garantizar unicidad y evitar falsificaciones
        """
        # Verificar si ya existe un certificado para este docente
        if self.docente.certificado:
            return self.docente.certificado.codigo_unico
        
        # Generar código único basado en docente_id + timestamp + random
        timestamp = datetime.now().isoformat()
        random_part = secrets.token_hex(4)
        data = f"{self.docente.id}:{timestamp}:{random_part}"
        
        # Generar HMAC
        hmac_obj = hmac.new(
            self.salt.encode(),
            data.encode(),
            hashlib.sha256
        )
        hash_hex = hmac_obj.hexdigest()
        
        # Tomar los primeros 12 caracteres y formatear
        codigo_base = hash_hex[:12].upper()
        codigo_formateado = f"{codigo_base[:4]}-{codigo_base[4:8]}-{codigo_base[8:12]}"
        
        return codigo_formateado
    
    def generar_qr_code(self, codigo):
        """Genera el código QR para verificación pública usando la URL base actual"""
        # Obtener la URL base de la solicitud actual
        # Si estamos en un contexto de solicitud, usar request.url_root
        # Si no, usar una URL por defecto configurable
        try:
            base_url = request.url_root.rstrip('/')
        except RuntimeError:
            # No hay contexto de solicitud (ej: CLI), usar localhost
            base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
        
        # URL de verificación
        url_verificacion = f"{base_url}/verificar/{codigo}"
        
        # Crear QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url_verificacion)
        qr.make(fit=True)
        
        # Generar imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar QR
        qr_filename = f"{codigo}.png"
        qr_path = os.path.join(self.qr_folder, qr_filename)
        
        # Crear carpeta si no existe
        os.makedirs(self.qr_folder, exist_ok=True)
        
        img.save(qr_path)
        return qr_path
    
    def clonar_tabla(self, tabla_original):
        """Clona una tabla de Word manteniendo su estructura y estilos"""
        # Esta función se usará para duplicar la tabla template por cada criterio
        # Por ahora retorna la referencia a la tabla original
        return tabla_original
    
    def poblar_tabla_criterio(self, tabla, nombre_criterio, detalles):
        """
        Puebla una tabla de criterio con los datos correspondientes
        tabla: objeto Table de python-docx
        nombre_criterio: nombre del tipo de criterio
        detalles: string con los detalles (multi-línea)
        """
        # Cambiar el título de la tabla (primera fila, primera celda)
        if len(tabla.rows) > 0:
            tabla.rows[0].cells[0].text = nombre_criterio
        
        # Poblar las filas de detalle
        detalles_lineas = [d.strip() for d in detalles.split('\n') if d.strip()]
        
        # Empezar desde la segunda fila (índice 1)
        fila_idx = 1
        for detalle in detalles_lineas[:5]:  # Máximo 5 filas según template
            if fila_idx < len(tabla.rows):
                # Assuming second column (index 1) is for details
                if len(tabla.rows[fila_idx].cells) > 0:
                    tabla.rows[fila_idx].cells[0].text = detalle
                fila_idx += 1
    
    def generar_certificado_pdf(self, output_path=None):
        """
        Genera el certificado PDF completo
        Retorna la ruta del archivo PDF generado
        """
        # Abrir el template Word
        doc = Document(self.template_path)
        
        # 1. Generar código único primero
        codigo = self.generar_codigo_unico()
        
        # 2. Reemplazar placeholders básicos (ahora incluye el código)
        self._reemplazar_placeholders(doc)
        
        # 3. Generar QR code
        qr_path = self.generar_qr_code(codigo)
        
        # 4. Insertar QR en el documento
        self._insertar_qr(doc, qr_path)
        
        # 5. Procesar tablas de criterios
        self._procesar_tablas_criterios(doc)
        
        # 6. Guardar documento Word temporal
        temp_docx_path = os.path.join(self.qr_folder, f"temp_{codigo}.docx")
        doc.save(temp_docx_path)
        
        # 7. Convertir a PDF
        if not output_path:
            output_path = os.path.join(self.qr_folder, f"certificado_{codigo}.pdf")
        
        convert(temp_docx_path, output_path)
        
        # 8. Limpiar archivo temporal
        if os.path.exists(temp_docx_path):
            os.remove(temp_docx_path)
        
        # 9. Crear o actualizar registro en base de datos
        self._guardar_certificado_db(codigo, qr_path)
        
        return output_path
    
    def _reemplazar_placeholders(self, doc):
        """Reemplaza los placeholders en el documento preservando el formato"""
        # Agregar el código único a los reemplazos
        codigo_unico = self.generar_codigo_unico()
        
        replacements = {
            '{{CODIGO}}': codigo_unico,
            '{{NOMBRE}}': self.docente.nombre_completo,
            '{{NOMBRES}}': self.docente.nombres,
            '{{APELLIDOS}}': self.docente.apellidos,
            '{{CI}}': self.docente.ci,
            '{{UNIDAD}}': self.docente.unidad.nombre,
            '{{UNIDAD_CODIGO}}': self.docente.unidad.codigo,
            '{{CIUDAD}}': self.docente.unidad.ciudad,
            '{{CARGO}}': self.docente.cargo or '',
            '{{AÑOS_SERVICIO}}': str(self.docente.años_servicio) if self.docente.años_servicio else '',
            '{{FECHA}}': datetime.now().strftime('%d de %B de %Y'),
        }
        
        # Reemplazar en párrafos
        for paragraph in doc.paragraphs:
            self._replace_in_paragraph(paragraph, replacements)
        
        # Reemplazar en tablas
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_in_paragraph(paragraph, replacements)
        
        return codigo_unico
    
    def _replace_in_paragraph(self, paragraph, replacements):
        """Reemplaza texto en un párrafo manejando runs fragmentados"""
        # Primero, consolidar el texto del párrafo
        full_text = paragraph.text
        
        # Verificar si hay algún placeholder
        has_placeholder = False
        for key in replacements.keys():
            if key in full_text:
                has_placeholder = True
                break
        
        if not has_placeholder:
            return
        
        # Si hay placeholders, reemplazar en el texto completo
        new_text = full_text
        for key, value in replacements.items():
            new_text = new_text.replace(key, value)
        
        # Si el texto cambió, reconstruir el párrafo
        if new_text != full_text:
            # Guardar el formato del primer run
            style = paragraph.runs[0].style if paragraph.runs else None
            font_name = paragraph.runs[0].font.name if paragraph.runs else None
            font_size = paragraph.runs[0].font.size if paragraph.runs else None
            bold = paragraph.runs[0].bold if paragraph.runs else None
            italic = paragraph.runs[0].italic if paragraph.runs else None
            
            # Limpiar el párrafo
            for run in paragraph.runs:
                run.text = ''
            
            # Agregar el nuevo texto con formato
            new_run = paragraph.add_run(new_text)
            if style:
                new_run.style = style
            if font_name:
                new_run.font.name = font_name
            if font_size:
                new_run.font.size = font_size
            if bold is not None:
                new_run.bold = bold
            if italic is not None:
                new_run.italic = italic
    
    def _insertar_qr(self, doc, qr_path):
        """Inserta el código QR en el documento"""
        # Buscar placeholder {{QR}} o agregar al final
        qr_insertado = False
        
        for paragraph in doc.paragraphs:
            if '{{QR}}' in paragraph.text:
                paragraph.clear()
                run = paragraph.add_run()
                run.add_picture(qr_path, width=Inches(1.5))
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                qr_insertado = True
                break
        
        # Si no se encontró placeholder, agregar al final
        if not qr_insertado:
            paragraph = doc.add_paragraph()
            run = paragraph.add_run()
            run.add_picture(qr_path, width=Inches(1.5))
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    def _procesar_tablas_criterios(self, doc):
        """
        Procesa las tablas de criterios:
        - Reemplaza el placeholder {{CRITERIOS}} con la lista de criterios
        """
        # Obtener criterios del docente
        criterios_docente = DocenteCriterio.query.filter_by(
            docente_id=self.docente.id
        ).join(DocenteCriterio.tipo_criterio).order_by(TipoCriterio.orden).all()
        
        if not criterios_docente:
            return
        
        # Buscar el índice del párrafo con {{CRITERIOS}}
        placeholder_index = None
        for idx, paragraph in enumerate(doc.paragraphs):
            if '{{CRITERIOS}}' in paragraph.text:
                placeholder_index = idx
                break
        
        if placeholder_index is not None:
            # Reemplazar el placeholder con los criterios
            # Primero, limpiar el párrafo del placeholder
            doc.paragraphs[placeholder_index].clear()
            
            # Construir el texto de criterios en el mismo párrafo
            criterios_texto = []
            for idx, docente_criterio in enumerate(criterios_docente, 1):
                criterios_texto.append(f"{idx}. {docente_criterio.tipo_criterio.nombre}")
                if docente_criterio.detalles:
                    # Indentar los detalles
                    detalles_lineas = docente_criterio.detalles.split('\n')
                    for linea in detalles_lineas:
                        if linea.strip():
                            criterios_texto.append(f"   {linea.strip()}")
                criterios_texto.append("")  # Línea en blanco entre criterios
            
            # Agregar todo el texto al párrafo
            nuevo_texto = '\n'.join(criterios_texto)
            doc.paragraphs[placeholder_index].add_run(nuevo_texto)
        else:
            # Si no se encontró placeholder, agregar al final
            doc.add_paragraph()
            p_titulo = doc.add_paragraph()
            run = p_titulo.add_run('Producción Intelectual y Científica')
            run.bold = True
            run.font.size = Pt(14)
            doc.add_paragraph()
            
            for idx, docente_criterio in enumerate(criterios_docente, 1):
                p = doc.add_paragraph()
                run = p.add_run(f"{idx}. {docente_criterio.tipo_criterio.nombre}")
                run.bold = True
                run.font.size = Pt(11)
                
                if docente_criterio.detalles:
                    p_detalle = doc.add_paragraph(docente_criterio.detalles)
                    p_detalle.paragraph_format.left_indent = Inches(0.5)
                    p_detalle.paragraph_format.space_after = Pt(6)
    
    def _guardar_certificado_db(self, codigo, qr_path):
        """Crea o actualiza el registro del certificado en la base de datos"""
        # Generar hash de verificación
        hash_verificacion = hmac.new(
            self.salt.encode(),
            f"{self.docente.id}:{codigo}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if self.docente.certificado:
            # Actualizar existente
            self.docente.certificado.fecha_ultima_actualizacion = datetime.utcnow()
            self.docente.certificado.qr_path = qr_path
        else:
            # Crear nuevo
            certificado = Certificado(
                docente_id=self.docente.id,
                codigo_unico=codigo,
                hash_verificacion=hash_verificacion,
                qr_path=qr_path
            )
            db.session.add(certificado)
        
        # Resetear flag de regeneración
        self.docente.requiere_regeneracion = False
        
        db.session.commit()
