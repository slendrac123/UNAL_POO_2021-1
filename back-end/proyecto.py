import sqlite3
from sqlite3 import Error

def sqlConnection():
    try:
        con = sqlite3.connect('./Vacunacion.db')
        return con
    except Error:
        print(Error)

def crearTablas():
    con = sqlConnection()
    cursorObj = con.cursor()
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
    # cursorObj.execute('''INSERT INTO "pacientes" VALUES (1001345205, 'juan jose', 'garcia leon', 'calle 17A #7b 57', 3108567898, 'jugarciale@unal.edu.co', 'bogota', '23112001', '05102014', 'N', '');''')
    cursorObj.execute('''
                CREATE TABLE if not exists "lote_vacuna" (
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
                    "imagen"	IMAGE,
                    PRIMARY KEY("noLote")
                );
                ''')
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
        opcion = int(input('Ingrese el numero de la opcion que desea realizar:\n1. Crear nuevo afiliado\n2. Consultar afiliado\n3. Desafiliar usuario\n4. Salir\n'))
        if (opcion == 1): crearUsuario()
        if (opcion == 2): consultarUsuario()
        if (opcion == 3): desafiliarUsuario()
        if (opcion == 4): break

def crearUsuario():
    con = sqlConnection()
    cursorObj = con.cursor()
    print('Ingrese a continuacion los datos de la persona que desea registrar:')
    documentoID = int(input('Documento de Identidad:\n'))
    # cursorObj.execute('SELECT count(*) FROM pacientes WHERE noId = {}'.format(documentoID))
    # verificacion = int(cursorObj.fetchall()[0][0])
    # if verificacion == 0:
    cursorObj.execute('SELECT * FROM pacientes WHERE noId = {}'.format(documentoID))
    resultado = cursorObj.fetchall()
    if len(resultado) == 0:
        nombre = input('Nombre:\n')
        apellido = input('Apellido:\n')
        direccion = input('Direccion:\n')
        telefono = int(input('Telefono:\n'))
        correo = input('Correo:\n')
        ciudad = input('Ciudad:\n')
        fechaNacimiento = input('Fecha de nacimiento (DDMMAAAA):\n')
        fechaAfiliacion = input('Fecha de afiliacion (DDMMAAAA):\n')
        vacunado = input('¿Ha sido vacunado?:\n')
        fechaDesafiliacion = input('Fecha de desafiliacion en caso de haberla (DDMMAAAA):\n')
        cursorObj.execute('INSERT INTO pacientes VALUES ("{a}","{b}","{c}","{d}","{e}","{f}","{g}","{h}","{i}","{j}","{k}")'.format(a=documentoID, b=nombre, c=apellido, d=direccion, e=telefono, f=correo, g=ciudad, h =fechaNacimiento, i=fechaAfiliacion, j=vacunado, k=fechaDesafiliacion))
        con.commit()
    else:
        print('Este usuario ya existe\n')
    
    con.close()

def consultarUsuario():
    con = sqlConnection()
    cursorObj = con.cursor()
    print('Ingrese a continuacion los datos de la persona que desea consultar:')
    documentoID = int(input('Documento de Identidad:\n'))
    cursorObj.execute('SELECT * FROM pacientes WHERE noId = {}'.format(documentoID))
    resultado = cursorObj.fetchall()
    if len(resultado) != 0:
        for datos in resultado[0]:
            if datos != '': print(datos)
        print('\n')
    else: print('El paciente no se encuentra en los registros.\n')

    con.close()

def desafiliarUsuario():
    con = sqlConnection()
    cursorObj = con.cursor()
    print('Ingrese a continuacion los datos de la persona que desea desafiliar:')
    documentoID = int(input('Documento de Identidad:\n'))
    cursorObj.execute('SELECT * FROM pacientes WHERE noId = {}'.format(documentoID))
    resultado = cursorObj.fetchall()
    if len(resultado) != 0:
        fechaDesafiliacion = input('Fecha de desafiliacion (DDMMAAAA):\n')
        cursorObj.execute('UPDATE pacientes SET fechaDesafiliacion = {} WHERE noID = {}'.format(fechaDesafiliacion, documentoID))
        con.commit()
    else: print('El paciente no se encuentra en los registros.')

    con.close()

crearTablas()
menuModuloUno()