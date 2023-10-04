from django.db import models
from django.contrib.auth.models import User

# Create your models here.

""" # Creación de una tabla con dependencias
class Genero(models.Model):
    idGenero = models.IntegerField(primary_key=True, db_column='idGenero')
    tipoGenero = models.TextField(db_column='tipoGenero')
    class Meta:
        db_table = 'Generos'

# Creación de una tabla sin dependencias
class Alumno (models.Model):
    idAlumno = models.IntegerField(primary_key=True, db_column='idAlumno')
    nameAlumno= models.CharField(max_length=100, db_column='nameAlumno')
    #fk_genero = models.ForeignKey(Genero, on_delete=models.CASCADE, default = 1, db_column='fk_genero')
    class Meta:
        db_table="Alumnos"
        
# Tabla N:M
class alumno_has_genero (models.Model):
    # Columna autoincrementable
    idAlumno_has_genero = models.AutoField(primary_key=True, default=1, db_column='idAlumno_has_genero')
    fk_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='fk_alumno')
    fk_genero = models.ForeignKey(Genero, on_delete=models.CASCADE, db_column='fk_genero')
    class Meta:
        db_table = 'alumno_has_genero' """
        
# Modelo de métodos de pago
class TipoTransaccion(models.Model):
    id_tipo = models.IntegerField(primary_key=True, db_column='id_tipo')
    tipo_transaccion = models.CharField(max_length=255)
    class Meta:
        db_table='TipoTransaccion'

# Modelo de métodos de pago
class MetodoDePago(models.Model):
    id_metodotipo = models.IntegerField(primary_key=True, db_column='id_metodotipo')
    nombre_metodo = models.CharField(max_length=255)
    class Meta:
        db_table='MetodoDePago'

# Modelo de categorías de transacciones
class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True, db_column='id_categoria')
    fk_tipo = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE, default=None, db_column='fk_tipo')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    class Meta:
        db_table='Categoria'

# Modelo de cuentas bancarias
class Cuenta(models.Model):
    id_cuenta = models.IntegerField(primary_key=True, db_column='id_cuenta', default=1)
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1, db_column='fk_usuario')
    nombre_cuenta= models.CharField(max_length=100, db_column='nombre_cuenta')
    fk_metodo_pago = models.ForeignKey(MetodoDePago, on_delete=models.CASCADE, default=None, db_column='fk_metodo_pago')
    class Meta:
        db_table='Cuenta'

# Modelo de ahorros
class Ahorro(models.Model):
    id_ahorro = models.IntegerField(primary_key=True, db_column='id_ahorro')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, db_column='fk_usuario')
    fk_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, default=1, db_column='fk_cuenta')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    class Meta:
        db_table='Ahorro'

# Modelo de pagos
class Pago(models.Model):
    id_pago = models.IntegerField(primary_key=True, db_column='id_pago')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, db_column='fk_usuario')
    nombre_deuda = models.CharField(max_length=255)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fechaInicio = models.DateField()
    fechaTermino = models.DateField()
    frecuencia = models.CharField(max_length=255)
    class Meta:
        db_table='Pago'

# Modelo de metas financieras
class MetaFinanciera(models.Model):
    id_meta = models.IntegerField(primary_key=True, db_column='id_meta')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, db_column='fk_usuario')
    descripcion = models.TextField()
    objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    fechaInicio = models.DateField()
    fechaTermino = models.DateField()
    class Meta:
        db_table='MetaFinanciera'

# Modelo de monedas
class Moneda(models.Model):
    id_moneda = models.IntegerField(primary_key=True, db_column='id_moneda')
    codigo_moneda = models.CharField(max_length=3)
    nombre_moneda = models.CharField(max_length=255)
    simbolo_moneda = models.CharField(max_length=10)
    class Meta:
        db_table='Moneda'

# Modelo de transacciones
class Transaccion(models.Model):
    id_transaccion = models.IntegerField(primary_key=True, db_column='id_transaccion')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, db_column='fk_usuario')
    fk_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, default=1, db_column='fk_cuenta')
    fkcategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=None, db_column='fkcategoria')
    fk_tipo = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE, default=None, db_column='fk_tipo')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    fk_moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, default=None, db_column='fk_moneda')
    class Meta:
        db_table='Transaccion'