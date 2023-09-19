from django.db import models

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
        
# Tabla CategoriasGastos
class CategoriasGastos (models.Model):
    idCategoriaGasto = models.AutoField(primary_key=True, default=1, db_column='idCategoriaGasto')
    categoria= models.CharField(max_length=100, db_column='categoria')
    class Meta:
        db_table="CategoriasGastos"

# Tabla CategoriasIngresos
class CategoriasIngresos (models.Model):
    idCategoriaIngreso = models.AutoField(primary_key=True, default=1, db_column='idCategoriaIngreso')
    categoria= models.CharField(max_length=100, db_column='categoria')
    class Meta:
        db_table="CategoriasIngresos"
    
# Tabla MetodosPago
class MetodosPago (models.Model):
    idMetodo = models.AutoField(primary_key=True, default=1, db_column='idMetodo')
    metodo= models.CharField(max_length=30, db_column='metodo')
    class Meta:
        db_table="MetodosPago"
        
# Tabla TiposMoneda
class TiposMoneada (models.Model):
    idTipoMoneda = models.AutoField(primary_key=True, default=1, db_column='idTipoMoneda')
    tipoMoneda= models.CharField(max_length=30, db_column='tipoMoneda')
    class Meta:
        db_table="TiposMoneda"
        
# Tabla MetasFinancieras
class MetasFinancieras (models.Model):
    idMeta = models.AutoField(primary_key=True, default=1, db_column='idMeta')
    descripcion= models.CharField(max_length=100, db_column='descripcion')
    cantidad = models.IntegerField(db_column='cantidad')
    fecha = models.DateField(db_column='fecha')
    class Meta:
        db_table="MetasFinancieras"
        
# Tabla Cuenta
class Cuenta (models.Model):
    idCuenta = models.AutoField(primary_key=True, default=1, db_column='idCuenta')
    numCuenta = models.CharField(max_length=18, db_column='numCuenta')
    fk_idMetodo = models.ForeignKey(MetodosPago, on_delete=models.CASCADE, db_column='fk_idMetodo')
    class Meta:
        db_table="Cuenta"
    
# Tabla Ingresos
class Ingresos (models.Model):
    idIngreso = models.IntegerField(primary_key=True, default=1, db_column='idIngreso')
    cantidad = models.IntegerField(db_column='cantidad')
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    fecha = models.DateField(db_column='fechaIngreso')
    fk_CategoriaIngreso = models.ForeignKey(CategoriasIngresos, on_delete=models.CASCADE, db_column='fk_idCategoriaIngreso')
    fk_idTipoMoneda = models.ForeignKey(TiposMoneada, on_delete=models.CASCADE, db_column='fk_idTipoMoneda')
    fk_idCuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='fk_idCuenta')
    class Meta:
        db_table="Ingresos"
        
# Tabla Gastos
class Gastos (models.Model):
    idGasto = models.IntegerField(primary_key=True, default=1, db_column='idIngreso')
    cantidad = models.IntegerField(db_column='cantidad')
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    fecha = models.DateField(db_column='fecha')
    fk_CategoriaIngreso = models.ForeignKey(CategoriasGastos, on_delete=models.CASCADE, db_column='fk_idCategoriaIngreso')
    fk_idTipoMoneda = models.ForeignKey(TiposMoneada, on_delete=models.CASCADE, db_column='fk_idTipoMoneda')
    fk_idCuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='fk_idCuenta')
    class Meta:
        db_table="Gastos"
        
########### Tabla Ahorros
class Ahorros (models.Model):
    idAhorro = models.IntegerField(primary_key=True, default=1, db_column='idAhorro')
    cantidad = models.IntegerField(db_column='cantidad')
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    fecha = models.DateField(db_column='fecha')
    fk_Ingreso = models.ForeignKey(Ingresos, on_delete=models.CASCADE, db_column='fk_idIngreso')
    class Meta:
        db_table="Ahorros"
        
# Tabla Deudas
class Deudas (models.Model):
    idDeuda = models.IntegerField(primary_key=True, default=1, db_column='idDeuda')
    cantidad = models.IntegerField(db_column='cantidad')
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    fechaPago = models.DateField(db_column='fechaPago')
    fk_idTipoMoneda = models.ForeignKey(TiposMoneada, on_delete=models.CASCADE, db_column='fk_idTipoMoneda')
    class Meta:
        db_table="Deudas"
        
# Tabla BalanceGeneral
class BalanceGeneral (models.Model):
    idBalance = models.IntegerField(primary_key=True, default=1, db_column='idBalance')
    fk_idGasto = models.ForeignKey(Gastos, on_delete=models.CASCADE, db_column='fk_idGasto')
    fk_idIngreso = models.ForeignKey(Ingresos, on_delete=models.CASCADE, db_column='fk_idIngreso')
    fk_idDeuda = models.ForeignKey(Deudas, on_delete=models.CASCADE, db_column='fk_idDeuda')
    fk_idMeta = models.ForeignKey(MetasFinancieras, on_delete=models.CASCADE, db_column='fk_idMeta')
    class Meta:
        db_table="BalanceGeneral"