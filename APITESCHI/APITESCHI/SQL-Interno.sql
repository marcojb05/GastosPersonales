-- SQLite
-- INSERCIÓN DE MONEDAS
/* INSERT INTO moneda VALUES('Peso mexicano','$','MXN'),
('Dólar Estadounidense','$', 'USD'),
('Euro','€', 'EUR');

-- INSERCIÓN DE TIPOS DE TRANSACCIONES
INSERT INTO TipoTransaccion VALUES ('TP-ING','Gasto'),
('TP-GAS','Ingreso');

-- INSERCIÓN DE CATEGORÍAS (INGRESOS)
-- ID, nombre, descripcion, fk_tipo
INSERT INTO Categoria VALUES('CAT-01', 'Inversiones', 'Ingresos generados a partir de inversiones financieras, como intereses de cuentas de ahorro, ganancias de capital por la venta de acciones o bonos, y dividendos de acciones.', 'TP-ING'),
('CAT-02', 'Secundarios', 'Ingresos adicionales obtenidos de actividades secundarias o trabajos a tiempo parcial, como un segundo empleo o un negocio paralelo.', 'TP-ING'),
('CAT-03', 'No tributables', 'Ingresos que no están sujetos a impuestos, como becas educativas o ciertas indemnizaciones por accidentes.', 'TP-ING'),
('CAT-04', 'Salario', 'La cantidad de dinero que queda del salario después de deducir todos los impuestos y gastos de los ingresos brutos.', 'TP-ING'),
('CAT-05', 'Rentas', 'Ingresos provenientes de alquileres de propiedades, ya sea de bienes raíces residenciales o comerciales.', 'TP-ING'),
('CAT-06', 'Comisiones', 'Ingresos ganados por agentes de ventas, corredores u otros profesionales que reciben un porcentaje de las ventas que realizan.', 'TP-ING'),
('CAT-07', 'Regalías', 'Ingresos generados por el uso o la venta de derechos de propiedad intelectual, como música, libros o patentes.', 'TP-ING'),
('CAT-08', 'Comercio', 'Ingresos generados a través de la venta de productos o servicios.', 'TP-ING'),
('CAT-09', 'Alquiler de equipos', 'Ingresos obtenidos al alquilar equipos, maquinaria o vehículos a otras empresas o individuos.', 'TP-ING');

-- INSERCIÓN DE CATEGORÍAS (GASTOS)
INSERT INTO Categoria VALUES('CAT-10', 'Vivienda', 'Ingresos generados a partir de inversiones financieras, como intereses de cuentas de ahorro, ganancias de capital por la venta de acciones o bonos, y dividendos de acciones.', 'TP-GAS'),
('CAT-11', 'Mantenimiento', 'Gastos relacionados con tu lugar de residencia, como el alquiler o la hipoteca de tu casa o apartamento.', 'TP-GAS'),
('CAT-12', 'Servicios', 'Pagos regulares por servicios públicos como agua, electricidad y gas, así como servicios de telefonía e Internet.', 'TP-GAS'),
('CAT-13', 'Alimentación', 'Gastos en comestibles y comida fuera de casa, incluyendo restaurantes y comida para llevar.', 'TP-GAS'),
('CAT-14', 'Transporte', 'Costos asociados con tu movilidad, como combustible, mantenimiento del vehículo y transporte público.', 'TP-GAS'),
('CAT-15', 'Salud', 'Gastos relacionados con el cuidado de la salud, incluyendo seguros médicos, consultas médicas y medicamentos.', 'TP-GAS'),
('CAT-16', 'Educación', 'Gastos educativos que incluyen matrícula escolar o universitaria, libros y cursos adicionales.', 'TP-GAS'),
('CAT-17', 'Entretenimiento', 'Gastos para actividades de ocio como salidas al cine, conciertos, suscripciones a servicios de streaming y pasatiempos.', 'TP-GAS'),
('CAT-18', 'Deudas y Finanzas', 'Pagos de préstamos, tarjetas de crédito y otros costos relacionados con la gestión de tu situación financiera.', 'TP-GAS'),
('CAT-19', 'Seguros', 'Pagos de seguros, como seguro de vida, de automóvil o de vivienda, para proteger contra riesgos específicos.', 'TP-GAS'),
('CAT-20', 'Ahorro e Inversiones', 'Fondos destinados a cuentas de ahorro, inversiones o la compra de acciones y bonos.', 'TP-GAS'),
('CAT-21', 'Ropa y Accesorios', 'Gastos en vestimenta, calzado y accesorios personales.', 'TP-GAS'),
('CAT-22', 'Cuidado Personal', 'Gastos en productos y servicios de cuidado personal, como peluquería, productos de belleza y gimnasio.', 'TP-GAS'),
('CAT-23', 'Viajes y Vacaciones', 'Gastos relacionados con escapadas y vacaciones, incluyendo alojamiento, transporte y actividades turísticas.', 'TP-GAS'),
('CAT-24', 'Donaciones y Caridad', 'Contribuciones a organizaciones benéficas y causas sociales.', 'TP-GAS'),
('CAT-25', 'Impuestos', 'Pagos de impuestos, como el impuesto sobre la renta y los impuestos de propiedad.', 'TP-GAS'),
('CAT-26', 'Gastos de Negocio', 'Costos operativos relacionados con la administración y el crecimiento de una empresa.', 'TP-GAS'),
('CAT-27', 'Gastos de viaje de negocios', 'Gastos asociados con viajes relacionados con el trabajo, como alojamiento y comidas.', 'TP-GAS'),
('CAT-28', 'Tecnología y Comunicaciones', 'Gastos en tecnología, dispositivos electrónicos y servicios de comunicación, como teléfono e Internet.', 'TP-GAS'),
('CAT-29', 'Mascotas', 'Costos de cuidado y alimentación de tus animales domésticos, así como servicios veterinarios y accesorios para mascotas.', 'TP-GAS');

INSERT INTO MetodoDePago VALUES ('Efectivo','MP-EFEC'),
('Tarjeta','MP-TARJ'),
('Cuenta','MP-CUEN'); */

-- INSERT INTO Cuenta VALUES ('12358432547554','Mercado Pago','MP-TARJ','2');