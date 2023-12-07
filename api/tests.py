import pytest
from django.test import TestCase
from api.models import MetodoPago, TipoTransaccion, Categoria, Moneda, Tarjeta
from django.contrib.auth.models import User

class TestMetodoPago(TestCase):
    def test_MetodoPago(self):
        objeto = MetodoPago.objects.create(id_metodotipo='1234', nombre_metodo='Nuevo Método')
        self.assertEqual(objeto.nombre_metodo, "Nuevo Método")
    def test_MetodoPagoCaracteres(self):
        objeto = MetodoPago.objects.create(id_metodotipo='MP-934', nombre_metodo='Método nuevo')
        self.assertEqual(objeto.nombre_metodo, "Método nuevo")
    def test_MetodoPagoBusqueda(self):
        objeto = MetodoPago.objects.create(id_metodotipo='MP-23', nombre_metodo='Ejemplo')
        self.assertEqual(objeto.nombre_metodo, "Un método")
    def test_MetodoPagoOutIndex(self):
        objeto = MetodoPago.objects.create(id_metodotipo='MP-AZ283293234', nombre_metodo='Ejemplo 2')
        self.assertEqual(objeto.nombre_metodo, "Ejemplo 2")
        
    def tearDown(self):
        MetodoPago.objects.all().delete()
        
class TestTipoTransaccion(TestCase):
    def test_TipoTransaccion(self):
        objeto = TipoTransaccion.objects.create(id_tipo='1250', tipo_transaccion='Tipo Transacción')
        self.assertEqual(objeto.tipo_transaccion, "Tipo Transacción")
    def test_TipoTransaccionCaracteres(self):
        objeto = TipoTransaccion.objects.create(id_tipo='TP-90', tipo_transaccion='Cheque')
        self.assertEqual(objeto.tipo_transaccion, "Cheque")
    def test_TipoTransaccionConsuta(self):
        objeto = TipoTransaccion.objects.create(id_tipo='TP-91', tipo_transaccion='Una transacción')
        self.assertEqual(objeto.tipo_transaccion, "Algo")
    def test_TipoTransaccionOutIndex(self):
        objeto = TipoTransaccion.objects.create(id_tipo='TP-92384743f34', tipo_transaccion='Otra transacción')
        self.assertEqual(objeto.tipo_transaccion, "Otra transacción")
        
    def tearDown(self):
        TipoTransaccion.objects.all().delete()
        
class TestMoneda(TestCase):
    def test_Moneda(self):
        moneda = Moneda.objects.create(id_moneda='123',
                                       nombre_moneda="Bolivar",
                                       simbolo_moneda="$")
        self.assertEqual(moneda.simbolo_moneda, "$")
    def test_MonedaCaracter(self):
        moneda = Moneda.objects.create(id_moneda='ARS',
                                       nombre_moneda="Peso Argentino",
                                       simbolo_moneda="$")
        self.assertEqual(moneda.nombre_moneda, "Peso Argentino")
    def test_MonedaOutIndex(self):
        moneda = Moneda.objects.create(id_moneda='ARS123',
                                       nombre_moneda="Peso Argentino",
                                       simbolo_moneda="$")
        self.assertEqual(moneda.nombre_moneda, "Peso Argentino")
    def test_MonedaConsulta(self):
        moneda = Moneda.objects.create(id_moneda='ASN',
                                       nombre_moneda="Dólar Australiano",
                                       simbolo_moneda="$")
        self.assertEqual(moneda.nombre_moneda, "Dólar Canadiense")
        
    def eliminarMoneda(self):
        Moneda.objects.all().delete()

@pytest.mark.django_db
class TestCategoriaModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tipo_transaccion = TipoTransaccion.objects.create(id_tipo='TP-03',
                                                              tipo_transaccion='Ejemplo de transacción')
        cls.categoria = Categoria.objects.create(id_categoria='C-58',
                                                 fk_tipo=cls.tipo_transaccion,
                                                 nombre='Nueva categoría',
                                                 descripcion='Esta es una categoría de ejemplo')

    def test_categoria(self):
        # Asegurarse de que los campos se guardaron correctamente
        self.assertEqual(self.categoria.id_categoria, 'C-58')
        self.assertEqual(self.categoria.fk_tipo.id_tipo, 'TP-03')
        self.assertEqual(self.categoria.nombre, 'Nueva categoría')
        self.assertEqual(self.categoria.descripcion, 'Esta es una categoría de ejemplo')
        
class TestTarjeta(TestCase):
    def setUp(self):
        # Crea un usuario y un método de pago para utilizar en las pruebas
        self.usuario = User.objects.create_user(
            username='MarcoAJB',
            email='antonio2552001@gmail.com',
            password='Az.-192837'
        )
        self.metodo_pago = MetodoPago.objects.create(
            id_metodotipo='1234',
            nombre_metodo='Nuevo Método'
        )

        # Crea una tarjeta de prueba
        self.tarjeta = Tarjeta.objects.create(
            id_cuenta='1234-5678-9012-3456',
            fk_usuario=self.usuario,
            nombre_cuenta='Tarjeta de Prueba',
            fk_metodo_pago=self.metodo_pago
        )
    def testTarjetaOutIndex(self):
        # Crea un usuario y un método de pago para utilizar en las pruebas
        self.usuario = User.objects.create_user(
            username='MarcoJB',
            email='antonio25052001@gmail.com',
            password='Az.-192837'
        )
        self.metodo_pago = MetodoPago.objects.create(
            id_metodotipo='MP-053',
            nombre_metodo='Nuevo Método'
        )

        # Crea una tarjeta de prueba
        self.tarjeta = Tarjeta.objects.create(
            id_cuenta='1234-5678-9012-3456-3456-3456',
            fk_usuario=self.usuario,
            nombre_cuenta='Tarjeta de Prueba',
            fk_metodo_pago=self.metodo_pago
        )

    def test_tarjeta_creation(self):
        # Verifica que la tarjeta se haya creado correctamente
        self.assertEqual(self.tarjeta.id_cuenta, 'Cuenta-001')
        self.assertEqual(self.tarjeta.fk_usuario, self.usuario)
        self.assertEqual(self.tarjeta.nombre_cuenta, 'Tarjeta de Prueba')
        self.assertEqual(self.tarjeta.fk_metodo_pago, self.metodo_pago)

    def test_str_representation(self):
        self.assertEqual(str(self.tarjeta), 'Tarjeta de Prueba')
        
    def eliminar(self):
        User.objects.all().delete()
        MetodoPago.objects.all().delete()
        Tarjeta.objects.all().delete()
        
class testUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='MarcoJB',
            email='antonio2552001@gmail.com',
            password='Az.-19283'
        )

    def test_CrearUsuario(self):
        self.assertEqual(self.user.username, 'MarcoJB')
        self.assertEqual(self.user.email, 'antonio2552001@gmail.com')
        self.assertTrue(self.user.check_password('Az.-19283'))

    def test_IniciarSesion(self):
        # Verificar que el usuario se pueda autenticar con las credenciales correctas
        authenticated = self.client.login(username='MarcoJB', password='Az.-19283')
        self.assertTrue(authenticated)

    def test_user_str_representation(self):
        # Verificar que la representación de cadena del usuario es su nombre de usuario
        self.assertEqual(str(self.user), 'MarcoJB')