from django.db import models
from django.contrib.auth.models import User

        
# Modelo de tipo de transacción
class TipoTransaccion(models.Model):
    id_tipo = models.CharField(primary_key=True, max_length=10, db_column='id_tipo')
    tipo_transaccion = models.CharField(max_length=255)
    class Meta:
        db_table='TipoTransaccion'

# Modelo de métodos de pago
class MetodoPago(models.Model):
    id_metodotipo = models.CharField(primary_key=True, max_length=7, db_column='id_metodotipo')
    nombre_metodo = models.CharField(max_length=255)
    class Meta:
        db_table='MetodoPago'

# Modelo de categorías de transacciones
class Categoria(models.Model):
    id_categoria = models.CharField(primary_key=True, max_length=10, db_column='id_categoria')
    fk_tipo = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE, default=None, db_column='fk_tipo')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    class Meta:
        db_table='Categoria'
      
class Tarjeta(models.Model):
    id_cuenta = models.CharField(primary_key=True, max_length=24, db_column='id_cuenta')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1, db_column='fk_usuario')
    nombre_cuenta = models.CharField(max_length=100, db_column='nombre_cuenta')
    fk_metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, default=1, db_column='fk_metodo_pago')
    class Meta:
        db_table = 'Tarjeta'

# Modelo de ahorros
class Ahorro(models.Model):
    id_ahorro = models.CharField(primary_key=True, max_length=20, db_column='id_ahorro')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1, db_column='fk_usuario')
    fk_cuenta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, default=1, db_column='fk_cuenta')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    class Meta:
        db_table='Ahorro'

# Modelo de pagos
class Pago(models.Model):
    id_pago = models.CharField(primary_key=True, max_length=20, db_column='id_pago')
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
    id_meta = models.CharField(primary_key=True, max_length=20, db_column='id_meta')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, db_column='fk_usuario')
    descripcion = models.TextField()
    objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    fechaInicio = models.DateField()
    fechaTermino = models.DateField()
    class Meta:
        db_table='MetaFinanciera'

# Modelo de monedas
class Moneda(models.Model):
    id_moneda = models.CharField(primary_key=True, max_length=3, db_column='id_moneda')
    nombre_moneda = models.CharField(max_length=255)
    simbolo_moneda = models.CharField(max_length=10)
    class Meta:
        db_table='Moneda'

# Modelo de transacciones
class Transaccion(models.Model):
    id_transaccion = models.CharField(primary_key=True, max_length=20, db_column='id_transaccion')
    fk_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, db_column='fk_usuario')
    fk_cuenta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, default=None, db_column='fk_cuenta')
    fkcategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=None, db_column='fkcategoria')
    fk_tipo = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE, default=None, db_column='fk_tipo')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    fk_moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, default=None, db_column='fk_moneda')
    class Meta:
        db_table='Transaccion'
        
class encuesta(models.Model):
	pregunta1 = models.TextField(db_column='Satisfacción con el sistema')
	pregunta2 = models.TextField(db_column='Dacilidad de uso y la amigabilidad de la interfaz')
	pregunta3 = models.TextField(db_column='Facilidad de usar y entender')
	pregunta4 = models.TextField(db_column='Frecuencia de problemas técnicos o errores')
	pregunta5 = models.TextField(db_column='Adaptabilidad a necesidades específicas y requisitos comerciales')
	pregunta6 = models.TextField(db_column='Mejoras en la eficiencia')
	pregunta7 = models.TextField(db_column='Utilidad de informes y análisis financieros')
	pregunta8 = models.TextField(db_column='Capacidad para manejar múltiples divisas y tasas de cambio')
	pregunta9 = models.TextField(db_column='Interrupciones en el servicio')
	pregunta10 = models.TextField(db_column='Perdida de datos críticos o información financiera')
	class Meta:
		db_table: 'encuesta'