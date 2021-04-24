import sqlite3
from sqlite3 import Error

## TODO comments

def sqlConnection():
    try:
        con = sqlite3.connect('./Vacunacion.db')
        return con
    except Error:
        print(Error)

def crearTablas():
    con = sqlConnection()
    cursorObj = con.cursor()
    # cursorObj.execute('''DROP TABLE pacientes''')
    cursorObj.execute('''
                CREATE TABLE if not exists "pacientes" (
                    "noId"	NUMERIC(12),
                    "nombre"	CHAR(20),
                    "apellido"	CHAR(20),
                    "direccion"	CHAR(20),
                    "telefono"	NUMERIC(12),
                    "correo"	CHAR(20),
                    "ciudad"	CHAR(20),
                    "fechaNacimiento"	CHAR(10),
                    "fechaAfiliacion"	CHAR(10),
                    "vacunado"	CHAR(20),
                    "fechaDesafiliacion"	CHAR(10),
                    PRIMARY KEY("noId")
                );
                ''')
    # cursorObj.execute('''DROP TABLE lote_vacunas''')
    cursorObj.execute('''
                CREATE TABLE if not exists "lote_vacunas" (
                    "noLote"	NUMERIC(12),
                    "fabricante"	CHAR(12),
                    "tipoVacuna"	CHAR(21),
                    "cantidadRecibida"	NUMERIC(6),
                    "cantidadUsada"	NUMERIC(6),
                    "dosisNecesaria"	NUMERIC(1),
                    "temperatura"	NUMERIC(2,1),
                    "efectividad"	NUMERIC(2,1),
                    "tiempoProteccion"	NUMERIC(3),
                    "fechaVencimiento"	CHAR(10),
                    "imagen"	LARGEBLOB,
                    PRIMARY KEY("noLote")
                );
                ''')
    # cursorObj.execute('''DROP TABLE plan_vacunacion''')
    cursorObj.execute('''
                CREATE TABLE if not exists "plan_vacunacion" (
                    "idPlan"	NUMERIC(2),
                    "edadMinima"	NUMERIC(3),
                    "edadMaxima"	NUMERIC(3),
                    "fechaInicio"	TEXT(10),
                    "fechaFinal"	TEXT(10),
                    PRIMARY KEY("idPlan")
                );
                ''')
    # cursorObj.execute('''DROP TABLE programacion_vacunas''')
    cursorObj.execute('''
                CREATE TABLE if not exists "programacion_vacunas" (
                    "ciudadVacunacion"	CHAR(20),
                    "fechaProgramada"	CHAR(10),
                    "horaProgramada"	CHAR(4),
                    "noId"      NUMERIC(12),
                    "noLote"	NUMERIC(12),
                    FOREIGN KEY("noId") REFERENCES "pacientes"("noId"),
                    FOREIGN KEY("noLote") REFERENCES "lote_vacuna"("noLote")
                );
                ''')
    cursorObj.execute('''
                CREATE INDEX if not exists "ix_programacion_vacunas_noId" ON "programacion_vacunas" (
                    "noId"	ASC
                );
                ''')
    cursorObj.execute('''
                SELECT * FROM programacion_vacunas C 
                inner join pacientes P on (C.noId = P.noId);
                ''')
    con.commit()
    con.close()

def menuModuloUno():
    while True:
        opcion = input('Ingrese el numero de la opcion que desea realizar:\n1. Crear nuevo afiliado\n2. Consultar afiliado\n3. Desafiliar usuario\n4. Salir\n')
        if opcion != '': 
            opcion = int(opcion)
            if (opcion == 1): crearUsuario()
            if (opcion == 2): consultarUsuario()
            if (opcion == 3): desafiliarUsuario()
            if (opcion == 4): break
        else: continue

def crearUsuario():
    con = sqlConnection() 
    cursorObj = con.cursor()
    print('Ingrese a continuacion los datos de la persona que desea registrar:')
    documentoID = int(input('Documento de Identidad:\n'))
    cursorObj.execute('SELECT * FROM pacientes WHERE noId = {}'.format(documentoID))
    resultado = cursorObj.fetchall()
    if len(resultado) == 0:
        nombre = input('Nombre:\n').title()
        apellido = input('Apellido:\n').title()
        direccion = input('Direccion:\n').title()
        telefono = int(input('Telefono:\n'))
        correo = input('Correo:\n')
        ciudad = input('Ciudad:\n').title()
        print('Fecha de nacimiento:')
        diaNacimiento = input("Dia: ")
        diaNacimiento = diaNacimiento.ljust(2)
        mesNacimiento = input("Mes: ")
        mesNacimiento = mesNacimiento.ljust(2)
        añoNacimiento = input("Año: ")
        añoNacimiento = añoNacimiento.ljust(4)
        fechaNacimiento = "{}-{}-{}".format(añoNacimiento,mesNacimiento,diaNacimiento)
        print('Fecha de afiliacion:')
        diaAfiliacion = input("Dia: ")
        diaAfiliacion = diaAfiliacion.ljust(2)
        mesAfiliacion = input("Mes: ")
        mesAfiliacion = mesAfiliacion.ljust(2)
        añoAfiliacion = input("Año: ")
        añoAfiliacion = añoAfiliacion.ljust(4)
        fechaAfiliacion = "{}-{}-{}".format(añoAfiliacion,mesAfiliacion,diaAfiliacion)
        vacunado = input('¿Ha sido vacunado? (S/N):\n').title()
        cursorObj.execute('INSERT INTO pacientes VALUES ({a},"{b}","{c}","{d}",{e},"{f}","{g}",date("{h}"),date("{i}"),"{j}","")'.format(a=documentoID, b=nombre, c=apellido, d=direccion, e=telefono, f=correo, g=ciudad, h =fechaNacimiento, i=fechaAfiliacion, j=vacunado))
        con.commit()
    else:
        print('Este usuario ya existe\n')
    
    con.close()

def consultarUsuario():
    con = sqlConnection()
    cursorObj = con.cursor()
    documentoID = int(input('Ingrese a continuacion el documento de identidad de la persona que desea consultar:\n'))
    cursorObj.execute('SELECT * FROM pacientes WHERE noId = {}'.format(documentoID))
    resultado = cursorObj.fetchall()
    print('\n')
    if len(resultado) != 0:
        for datos in resultado[0]:
            if datos != '': print(datos)
        print('\n')
    else: print('El paciente no se encuentra en los registros.\n')

    con.close()

def desafiliarUsuario():
    con = sqlConnection()
    cursorObj = con.cursor()
    documentoID = int(input('Ingrese a continuacion el documento de identidad de la persona que desea desafiliar:\n'))
    cursorObj.execute('SELECT * FROM pacientes WHERE noId = {}'.format(documentoID))
    resultado = cursorObj.fetchall()
    if len(resultado) != 0:
        print('Fecha de desafiliacion:')
        diaDesafiliacion = input("Dia: ")
        diaDesafiliacion = diaDesafiliacion.ljust(2)
        mesDesafiliacion = input("Mes: ")
        mesDesafiliacion = mesDesafiliacion.ljust(2)
        añoDesafiliacion = input("Año: ")
        añoDesafiliacion = añoDesafiliacion.ljust(4)
        fechaDesafiliacion = "{}-{}-{}".format(añoDesafiliacion,mesDesafiliacion,diaDesafiliacion)
        cursorObj.execute('UPDATE pacientes SET fechaDesafiliacion = date("{}") WHERE noID = {}'.format(fechaDesafiliacion, documentoID))
        con.commit()
    else: print('El paciente no se encuentra en los registros.')

    con.close()

def menuModuloDos():
    while True:
        opcion = input('Ingrese el numero de la opcion que desea realizar:\n1. Crear nuevo lote de vacunas\n2. Consultar lote de vacunas\n3. Salir\n')
        if opcion != '': 
            opcion = int(opcion)
            if (opcion == 1): crearLote()
            if (opcion == 2): consultarLote()
            if (opcion == 3): break
        else: continue

def crearLote():
    con = sqlConnection() 
    cursorObj = con.cursor()
    print('Ingrese a continuacion los datos del lote que desea registrar:')
    numeroLote = int(input('Numero del lote:\n'))
    cursorObj.execute('SELECT * FROM lote_vacunas WHERE noLote = {}'.format(numeroLote))
    resultado = cursorObj.fetchall()
    if len(resultado) == 0:
        fabricante = input('Fabricante:\n').title()
        tipoVacuna = input('Tipo de vacuna:\n').title()
        cantidadRecibida = int(input('Cantidad de vacunas recibidas:\n'))
        cantidadUsada = int(input('Cantidad de vacunas usadas:\n'))
        dosisNecesaria = int(input('Dosis necesarias:\n'))
        temperatura = float(input('Temperatura de almacenamiento:\n'))
        efectividad = float(input('Efectividad de la vacuna:\n'))
        tiempoProteccion = int(input('Tiempo de proteccion (meses):\n'))
        print('Fecha de vencimiento:')
        diaVencimiento = input("Dia: ")
        diaVencimiento = diaVencimiento.ljust(2)
        mesVencimiento = input("Mes: ")
        mesVencimiento = mesVencimiento.ljust(2)
        añoVencimiento = input("Año: ")
        añoVencimiento = añoVencimiento.ljust(4)
        fechaVencimiento = "{}-{}-{}".format(añoVencimiento,mesVencimiento,diaVencimiento)
        rutaImagen = input('Ruta completa a la imagen:\n')
        rutaImagen = '/home/alpha23/Pictures/Screenshot_20210316_011734.png'
        with open(rutaImagen, "rb") as File:
            imagenBinaria = File.read()
        # print(imagenBinaria)
        # print(type(imagenBinaria))
        # Direccion de prueba: /home/alpha23/Pictures/Screenshot_20210316_011734.png

        # # TODO Encontrar forma de almacenar la imagen
        cursorObj.execute('INSERT INTO lote_vacunas VALUES ({a},"{b}","{c}",{d},{e},{f},{g},{h},{i},date("{j}"),"")'.format(a=numeroLote, b=fabricante, c=tipoVacuna, d=cantidadRecibida, e=cantidadUsada, f=dosisNecesaria, g=temperatura, h =efectividad, i=tiempoProteccion, j=fechaVencimiento, k=imagenBinaria))
        con.commit()
    else:
        print('Este lote de vacunas ya existe\n')
    
    con.close()

def consultarLote():
    con = sqlConnection()
    cursorObj = con.cursor()
    noLote = int(input('Ingrese a continuacion numero de lote que desea consultar:\n'))
    cursorObj.execute('SELECT * FROM lote_vacunas WHERE noLote = {}'.format(noLote))
    resultado = cursorObj.fetchall()
    print('\n')
    if len(resultado) != 0:
        for datos in resultado[0]:
            if datos != '': print(datos)
        print('\n')
    else: print('El lote no se encuentra registrado.\n')

    con.close()

def menuModuloTres():
    while True:
        opcion = input('Ingrese el numero de la opcion que desea realizar:\n1. Crear plan de vacunación\n2. Consultar plan de vacunación\n3. Salir\n')
        if opcion != '': 
            opcion = int(opcion)
            if (opcion == 1): crearPlanVacunacion()
            if (opcion == 2): consultarPlanVacunacion()
            if (opcion == 3): break
        else: continue

def crearPlanVacunacion():
    con = sqlConnection() 
    cursorObj = con.cursor()
    print('Ingrese a continuacion los datos del plan de vacunación que desea crear:')
    idPlan = int(input('Codigo del plan:\n'))
    cursorObj.execute('SELECT * FROM plan_vacunacion WHERE idPlan = {}'.format(idPlan))
    resultado = cursorObj.fetchall()
    if len(resultado) == 0:
        edadMinima = int(input('Edad minima requerida:\n'))
        edadMaxima = int(input('Edad maxima requerida:\n'))
        print('Fecha de inicio:')
        diaInicio = input("Dia: ")
        diaInicio = diaInicio.ljust(2)
        mesInicio = input("Mes: ")
        mesInicio = mesInicio.ljust(2)
        añoInicio = input("Año: ")
        añoInicio = añoInicio.ljust(4)
        fechaInicio = "{}-{}-{}".format(añoInicio,mesInicio,diaInicio)
        print('Fecha de finalizacion:')
        diaFinal = input("Dia: ")
        diaFinal = diaFinal.ljust(2)
        mesFinal = input("Mes: ")
        mesFinal = mesFinal.ljust(2)
        añoFinal = input("Año: ")
        añoFinal = añoFinal.ljust(4)
        fechaFinal = "{}-{}-{}".format(añoFinal,mesFinal,diaFinal)
        cursorObj.execute('INSERT INTO plan_vacunacion VALUES ({a},{b},{c},date("{d}"),date("{e}"))'.format(a=idPlan, b=edadMinima, c=edadMaxima, d=fechaInicio, e=fechaFinal))
        con.commit()
    else:
        print('Este plan de vacunacion ya existe\n')
    
    con.close()

def consultarPlanVacunacion():
    con = sqlConnection()
    cursorObj = con.cursor()
    idPlan = int(input('Ingrese a continuacion el codigo del plan de vacunacion que desea consultar:\n'))
    cursorObj.execute('SELECT * FROM plan_vacunacion WHERE idPlan = {}'.format(idPlan))
    resultado = cursorObj.fetchall()
    print('\n')
    if len(resultado) != 0:
        for datos in resultado[0]:
            if datos != '': print(datos)
        print('\n')
    else: print('El plan de vacunación no se encuentra registrado.\n')

    con.close()

crearTablas()
menuModuloUno()
menuModuloDos()
menuModuloTres()
