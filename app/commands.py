import click
from flask.cli import with_appcontext
from app import db
from app.models.usuario import Usuario
from app.models.unidad_academica import UnidadAcademica
from app.models.tipo_criterio import TipoCriterio
from getpass import getpass

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Crea todas las tablas de la base de datos"""
    db.create_all()
    click.echo('Base de datos inicializada correctamente.')

@click.command('create-admin')
@click.option('--username', prompt='Nombre de usuario', help='Username del administrador')
@click.option('--password', prompt='Contraseña', hide_input=True, confirmation_prompt=True, help='Contraseña del administrador')
@click.option('--nombre', prompt='Nombre completo', help='Nombre completo del administrador')
@click.option('--email', prompt='Email', help='Email del administrador')
@with_appcontext
def create_admin_command(username, password, nombre, email):
    """Crea un usuario administrador"""
    # Verificar si ya existe el usuario
    if Usuario.query.filter_by(username=username).first():
        click.echo(f'Error: El usuario "{username}" ya existe.')
        return
    
    # Crear nuevo usuario
    usuario = Usuario(
        username=username,
        nombre_completo=nombre,
        email=email
    )
    usuario.set_password(password)
    
    db.session.add(usuario)
    db.session.commit()
    
    click.echo(f'Usuario administrador "{username}" creado exitosamente.')

@click.command('seed-data')
@with_appcontext
def seed_data_command():
    """Puebla la base de datos con datos iniciales (Unidades Académicas y Tipos de Criterios)"""
    
    # Seed de Unidades Académicas
    unidades = [
        {'codigo': 'UALP', 'nombre': 'Unidad Académica La Paz', 'ciudad': 'La Paz'},
        {'codigo': 'UACB', 'nombre': 'Unidad Académica Cochabamba', 'ciudad': 'Cochabamba'},
        {'codigo': 'UASC', 'nombre': 'Unidad Académica Santa Cruz', 'ciudad': 'Santa Cruz'},
        {'codigo': 'UARB', 'nombre': 'Unidad Académica Riberalta', 'ciudad': 'Riberalta'},
        {'codigo': 'UATP', 'nombre': 'Unidad Académica Trópico', 'ciudad': 'Trópico'},
    ]
    
    click.echo('Insertando Unidades Académicas...')
    for idx, u in enumerate(unidades, 1):
        if not UnidadAcademica.query.filter_by(codigo=u['codigo']).first():
            unidad = UnidadAcademica(**u)
            db.session.add(unidad)
            click.echo(f"  ✓ {u['codigo']} - {u['nombre']}")
        else:
            click.echo(f"  - {u['codigo']} ya existe")
    
    # Seed de Tipos de Criterios
    criterios = [
        {'orden': 1, 'nombre': 'TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE - EMI'},
        {'orden': 2, 'nombre': 'TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE'},
        {'orden': 3, 'nombre': 'TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS - EMI'},
        {'orden': 4, 'nombre': 'TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS'},
        {'orden': 5, 'nombre': 'LIBROS (SENAPI o ISBN) - EMI'},
        {'orden': 6, 'nombre': 'LIBROS (SENAPI o ISBN)'},
        {'orden': 7, 'nombre': 'ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA) - EMI'},
        {'orden': 8, 'nombre': 'ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA)'},
        {'orden': 9, 'nombre': 'ARTÍCULOS CIENTÍFICOS INDEXADOS (QS) - EMI'},
        {'orden': 10, 'nombre': 'ARTÍCULOS CIENTÍFICOS INDEXADOS (QS)'},
    ]
    
    click.echo('\nInsertando Tipos de Criterios...')
    for c in criterios:
        if not TipoCriterio.query.filter_by(nombre=c['nombre']).first():
            criterio = TipoCriterio(**c)
            db.session.add(criterio)
            click.echo(f"  ✓ {c['orden']}. {c['nombre']}")
        else:
            click.echo(f"  - {c['nombre']} ya existe")
    
    db.session.commit()
    click.echo('\n¡Datos iniciales insertados correctamente!')
