import os
import secrets
import hashlib
import hmac
from datetime import datetime
import qrcode
from flask import current_app
from app.models.certificado import Certificado
from app import db

class CertificadoGenerator:
    """Generador simplificado de certificados: solo códigos y QR"""
    
    def __init__(self, docente_criterio):
        self.docente_criterio = docente_criterio
        self.docente = docente_criterio.docente
        self.qr_folder = current_app.config.get('QR_FOLDER', 'app/static/qr_codes')
        self.salt = current_app.config.get('CERTIFICATE_SALT', 'emi-salt-2025')
    
    def generar_codigo_unico(self):
        """
        Genera un código único alfanumérico en formato ABCD-1234-EFGH
        usando HMAC-SHA256 para garantizar unicidad
        """
        # Generar código único basado en docente_id + criterio_id + timestamp + random
        timestamp = datetime.now().isoformat()
        random_part = secrets.token_hex(4)
        data = f"{self.docente.id}:{self.docente_criterio.id}:{timestamp}:{random_part}"
        
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
    
    def generar_codigo_emi(self):
        """
        Genera código EMI secuencial: EMI-DNICYT-CERT.00001/2025
        """
        año_actual = datetime.now().year
        
        # Obtener el último número secuencial del año actual
        ultimo_cert = Certificado.query.filter(
            Certificado.codigo_emi.like(f'%/{año_actual}')
        ).order_by(Certificado.id.desc()).first()
        
        if ultimo_cert:
            # Extraer número del código (EMI-DNICYT-CERT.00001/2025 -> 00001)
            try:
                numero_str = ultimo_cert.codigo_emi.split('.')[1].split('/')[0]
                numero = int(numero_str) + 1
            except:
                numero = 1
        else:
            numero = 1
        
        # Formatear código EMI
        codigo_emi = f"EMI-DNICYT-CERT.{numero:05d}/{año_actual}"
        return codigo_emi
    
    def generar_qr_code(self, codigo_unico, codigo_emi):
        """
        Genera el código QR con texto simple (no URL)
        Contenido: Nombres, Apellidos, Código Alfanumérico, Código EMI, Criterio y Descripción
        """
        # Obtener detalles del criterio (puede ser largo, limitamos a 200 caracteres)
        detalles = self.docente_criterio.detalles or "Sin detalles"
        if len(detalles) > 200:
            detalles = detalles[:197] + "..."
        
        # Texto simple para el QR
        texto_qr = f"""Docente: {self.docente.nombre_completo}
Código: {codigo_unico}
EMI: {codigo_emi}
Criterio: {self.docente_criterio.tipo_criterio.nombre}
Descripción: {detalles}"""
        
        # Crear QR con versión automática para ajustar al contenido
        qr = qrcode.QRCode(
            version=None,  # Versión automática según contenido
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # Nivel medio para más datos
            box_size=10,
            border=4,
        )
        qr.add_data(texto_qr)
        qr.make(fit=True)
        
        # Generar imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar QR
        qr_filename = f"{codigo_unico}.png"
        qr_path = os.path.join(self.qr_folder, qr_filename)
        
        # Crear carpeta si no existe
        os.makedirs(self.qr_folder, exist_ok=True)
        
        img.save(qr_path)
        return qr_path
    
    def generar_certificado(self):
        """
        Genera un certificado para el criterio del docente
        Retorna el objeto Certificado creado
        """
        # 1. Generar códigos
        codigo_unico = self.generar_codigo_unico()
        codigo_emi = self.generar_codigo_emi()
        
        # 2. Generar hash de verificación
        data_verificacion = f"{self.docente.id}:{self.docente_criterio.id}:{codigo_unico}:{codigo_emi}"
        hash_verificacion = hmac.new(
            self.salt.encode(),
            data_verificacion.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # 3. Generar QR code
        qr_path = self.generar_qr_code(codigo_unico, codigo_emi)
        
        # 4. Crear registro en base de datos
        certificado = Certificado(
            docente_id=self.docente.id,
            docente_criterio_id=self.docente_criterio.id,
            codigo_unico=codigo_unico,
            codigo_emi=codigo_emi,
            hash_verificacion=hash_verificacion,
            qr_path=qr_path,
            valido=True
        )
        
        db.session.add(certificado)
        db.session.commit()
        
        return certificado
