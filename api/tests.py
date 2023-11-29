import pytest
from django.test import TestCase
from api.models import MetodoPago, TipoTransaccion, Categoria, Moneda
from django.contrib.auth.models import User

# class TestMetodoPago(TestCase):
#     def tearDown(self):
#         MetodoPago.objects.all().delete()

#     def test_MetodoPago(self):
#         objeto = MetodoPago.objects.create(id_metodotipo='1234', nombre_metodo='Nuevo Método')
#         self.assertEqual(objeto.nombre_metodo, "Nuevo Método")
        
#     def tearDown(self):
#         MetodoPago.objects.all().delete()
        
# class TestTipoTransaccion(TestCase):
#     def test_TipoTransaccion(self):
#         objeto = TipoTransaccion.objects.create(id_tipo='TP-90', tipo_transaccion='Mercado Pago')
#         self.assertEqual(objeto.tipo_transaccion, "Algo")
        
#     def tearDown(self):
#         TipoTransaccion.objects.all().delete()
        
# class TestMoneda(TestCase):
#     def test_Moneda(self):
#         moneda = Moneda.objects.create(id_moneda='123',
#                                        nombre_moneda="Peso Mexicano",
#                                        simbolo_moneda="$")
#         self.assertEqual(moneda.simbolo_moneda, "Ñí^d")
        
#     def eliminarMoneda(self):
#         Moneda.objects.all().delete()

# @pytest.mark.django_db
# class TestCategoriaModel(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.tipo_transaccion = TipoTransaccion.objects.create(id_tipo='TP-03',
#                                                               tipo_transaccion='Ejemplo de transacción')
#         cls.categoria = Categoria.objects.create(id_categoria='C-58',
#                                                  fk_tipo=cls.tipo_transaccion,
#                                                  nombre='Nueva categoría',
#                                                  descripcion='Esta es una categoría de ejemplo')

#     def test_categoria(self):
#         # Asegurarse de que los campos se guardaron correctamente
#         self.assertEqual(self.categoria.id_categoria, 'C-58')
#         self.assertEqual(self.categoria.fk_tipo.id_tipo, 'TP-04')
#         self.assertEqual(self.categoria.nombre, 'Nueva categoría')
#         self.assertEqual(self.categoria.descripcion, 'Esta es una categoría de ejemplo')
        
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
        authenticated = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(authenticated)

    def test_user_str_representation(self):
        # Verificar que la representación de cadena del usuario es su nombre de usuario
        self.assertEqual(str(self.user), 'testuser')