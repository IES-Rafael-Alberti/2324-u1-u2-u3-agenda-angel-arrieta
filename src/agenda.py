"""
Agenda
------

Práctica para realizar esta semana.

La fecha de entrega es el próximo viernes, 1 de diciembre.

   
   * RA1: Conoce la estructura de un programa informático, identificando y relacionando los elementos propios del lenguaje de programación utilizado.
      - CE: a), b), c), d), e), f), g), h) e i).
   * RA3: Escribe y depura código, analizando y utilizando las estructuras de control del lenguaje.
      - CE: a), b), c), d), e), f) y g).
   * RA6: Escribe programas que manipulen información seleccionando y utilizando tipos avanzados de datos.
      - CE: a), b), c), d) y e).
      
1. El programa debe estar correctamente documentado (Docstrings y comentarios).

2. Observad que las funciones existentes en el código del programa no están completamente bien documentadas.

3. Debes intentar ajustarte lo máximo posible a lo que se pide en los comentarios TODO que observarás en el programa agenda.py.

4. Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

5. Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py de la carpeta test.

6. Debido al punto anterior, estás obligado a desarrollar los métodos que se importan y prueban en los tests unitarios: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}
MENU = {1: "nuevo", 2: "modificar", 3: "eliminar", 4: "vaciar",
                 5: "cargar", 6: "mostrar_criterio", 7: "mostrar_todo", 8: "salir"}


def borrar_consola():
    """ Limpia la consola """
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")


def cargar_contactos() -> list:
    """
    Carga los contactos iniciales de la agenda desde un fichero
    -----------------
    :return: Lista con cada contacto como diccionario
    """
    contactos = list()
    with open(RUTA_FICHERO, 'r') as fichero:
        for linea in fichero:
            contacto = dict()
            campos = linea.split(";")
            for i in range(len(campos)):
                if "\n" in campos[i]:
                    campos[i] = campos[i][:-1]
            contacto.update({'nombre': campos[0], 'apellido': campos[1], 'correo': campos[2]})
            telefono_s = list()
            for i in range(3, len(campos)):
                telefono_s.append(campos[i])
            contacto.update({'telefonos': telefono_s})
            contactos.append(contacto)
    return contactos


def mostrar_menu(contactos: list):
    print(f"""
    # AGENDA ({len(contactos)})
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    # """)


def pedir_opcion():
    """
    Función que pide al usuario que escoja una opción a emplear en la agenda
    -----------------------
    :return: cadena asociada a la opción escogida
    """
    opcion = str(input("""    # >> Seleccione una opción:\t """))
    print("    #\n")
    opt_menu = set()
    [opt_menu.add(str(opt)) for opt in OPCIONES_MENU]
    if opcion in opt_menu:
        return int(opcion)
    else:
        return -1


def validar_telefono(telefono: str) -> bool:
    import re
    valido = True
    if re.search("^[+]", telefono) is not None:
        telefono = telefono[1:]
        if re.search("^34", telefono) is not None:
            telefono = telefono[2:]
        else:
            valido = False
    elif re.search("[^0-9]", telefono) is not None:
        valido = False
    elif len(telefono) != 9:
        valido = False
    if telefono == "":
        valido = True

    return valido


def validar_email(correo: str, contactos: list, comprobar_dentro: bool) -> bool:
    import re
    adecuado = True
    if comprobar_dentro is True:
        correos = [contacto.get('correo') for contacto in contactos]
        if correo in correos:
            adecuado = False
            error = "el email ya existe en la agenda"
    else:
        if len(correo) == 0:
            adecuado = False
            error = "el email no puede ser una cadena vacía"
        elif correo.count("@") != 1:
            error = "el email no es un correo válido"
            adecuado = False
        else:
            direccion, dominio = correo.split("@")
            if re.search("\W", direccion) is not None:
                error = "la direccion del email contiene caracteres no permitidos (permitidos: A-Za-z0-9)"
                adecuado = False
            elif re.search("[^a-z.]", dominio) is not None:
                error = "el dominio del email no es valido (solo debe tener minúsculas y puntos)"
                adecuado = False
    if adecuado is False:
        raise ValueError(error)

    return adecuado


def pedir_email(contactos: list, comprobar_dentro: bool) -> tuple:
    correo = str(input("Introduce un correo\n>\t"))
    adecuado = validar_email(correo, contactos, comprobar_dentro)
    return correo, adecuado


def validar_nom_ape(nom_ape: str) -> bool:
    import re
    valido = True
    if re.search("[^A-Za-z ]", nom_ape) is not None:
        print("El nombre o apellido contiene caracteres no palabra")
        valido = False
    return valido


def agregar_contacto(contactos: list) -> dict:
    seguir = False
    nombre = str(input("Introduce un nombre (no acentuar)\n>\t"))
    while not seguir:
        seguir = validar_nom_ape(nombre)
        if seguir is False:
            nombre = str(input("Introduce otro nombre\n>\t"))

    seguir = False
    apellidos = str(input("Introduce apellido (sin acentuaciones)\n>\t"))
    while not seguir:
        seguir = validar_nom_ape(apellidos)
        if seguir is False:
            apellidos = str(input("Introduce otro apellido (no acentuar)\n>\t"))

    seguir = False
    while not seguir:
        try:
            email, adecuado = pedir_email(contactos, False)
            if adecuado is True:
                seguir = adecuado
        except ValueError:
            print("Correo no permitido")
    seguir = False
    telefonos = []
    telefono = str(input("Introduce un teléfono (<ENTER> para terminar)\n>\t"))
    while not seguir:
        if " " in telefono:
            telefono = "".join(telefono.split(" "))
        if telefono == "":
            seguir = True
        else:
            telefono = str(input("Introduce otro teléfono (<ENTER> para terminar)\n>\t"))
            anadir = validar_telefono(telefono)
            if anadir is False:
                print("Telefono invalido (Ejemplos de tlf. validos: +34111222333 ó 123456789)\n")
            else:
                telefonos.append(telefono)

    contacto = {'nombre': nombre.capitalize().strip(), 'apellido': apellidos.capitalize().strip(),
                'correo': email, 'telefonos': telefonos}
    return contacto


def eliminar_contacto(contactos: list, email: str) -> list:
    """ Elimina un contacto de la agenda
    ...
    """
    pos = buscar_contacto(contactos, email)
    if type(pos) is int:
        contactos.pop(pos)
        print("Se eliminó 1 contacto\n")
        return contactos
    else:
        print("No se encontró el contacto para eliminar\n")


def buscar_contacto(contactos: list, email: str) -> int or None:
    correos_en_orden = [contacto.get('correo') for contacto in contactos]
    if email not in correos_en_orden:
        posicion_contacto_en_agenda = None
    else:
        posicion_contacto_en_agenda = correos_en_orden.index(email)

    return posicion_contacto_en_agenda


def almacenar_por_criterio(contactos: list) -> list:
    claves = ['nombre', 'apellido', 'correo', 'telefonos']
    import re
    clave = ""

    while clave not in claves:
        clave = str(input("Introduce por cual campo quieres buscar [nombre, apellido, correo ó telefonos]\n>\t"))
        if clave not in claves:
            print("Campo de contacto no existente\n")

    valores_clave_ordenados = list()
    for contacto in contactos:
        valores_clave_ordenados.append(contacto.get(clave))
    criterio = str(input("Introduce el criterio por el que buscar: "))

    CCC = list()  # Contactos con Campos Coincidentes
    for valor in valores_clave_ordenados:
        if clave == 'telefonos':
            if len(valor) != 0:
                for telefono in valor:
                    if re.search(f"^[+34]", telefono) is not None:
                        tlf = telefono[3:]
                    else:
                        tlf = telefono
                    if re.search(f"^{criterio}", tlf) is not None:
                        indice = valores_clave_ordenados.index(valor)
                        if contactos[indice] not in CCC:
                            CCC.append(contactos[indice])
        else:
            if re.search(f"^{criterio}", valor) is not None:
                indice = valores_clave_ordenados.index(valor)
                CCC.append(contactos[indice])
    print(f"Contactos donde el inicio de {clave} coincide con {criterio}\n")
    if len(contactos) == 0:
        print("Busqueda .... \n"
              "No se encuentran contactos coincidentes\n")
    return CCC


def presentar_contactos(contactos: list):
    import re
    if len(contactos) == 0:
        print("(No hay contactos)\n")
    else:
        contactos_ordenados = sorted(contactos, key=lambda i: i['nombre'])

        print(f"    AGENDA ({len(contactos)})\n"
              f"    ------")
        for contacto in contactos_ordenados:
            if len(contacto.get('telefonos')) == 0:
                print(f"""    Nombre: {contacto.get('nombre')} {contacto.get('apellido')} ({contacto.get('correo')})
    Teléfono(s): ninguno
    ......\n """)
            else:
                telefonos = list()
                for telefono in contacto.get('telefonos'):
                    if re.search("^[+]34", telefono) is not None:
                        sin_prefijo = telefono[3:]
                        tlf_bomnito = "+34-" + sin_prefijo
                        telefonos.append(tlf_bomnito)
                telefono_s = " / ".join(contacto.get('telefonos'))
                print(f"""    Nombre: {contacto.get('nombre')} {contacto.get('apellido')} ({contacto.get('correo')})
    Teléfono(s): {telefono_s}
    ......\n """)


def agenda(contactos: list) -> list:
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    opcion = 0
    while opcion != 8:
        mostrar_menu(contactos)
        opcion = pedir_opcion()
        if opcion in OPCIONES_MENU:
            accion = MENU.get(opcion)
            if accion == "nuevo":
                contacto = agregar_contacto(contactos)
                contactos.append(contacto)
            elif accion == "modificar":
                seguir = False
                while not seguir:
                    try:
                        email, adecuado = pedir_email(contactos, False)
                        if adecuado is True:
                            seguir = adecuado
                    except ValueError:
                        print("Correo no permitido")
                posicion_contacto = buscar_contacto(contactos, email)
                contacto = contactos[posicion_contacto]
                if len(list(contacto.items())) > 3:
                    telefono_s = ", ".join(contacto.get('telefonos'))
                    print(f"""    Contacto a cambiar:
    nombre: {contacto.get('nombre')}
    apellidos: {contacto.get('apellido')}
    correo: {contacto.get('correo')}
    tefono(s): {telefono_s} """)
                else:
                    print(f"""    Contacto a cambiar:
    nombre: {contacto.get('nombre')}
    apellidos: {contacto.get('apellido')}
    correo: {contacto.get('correo')} """)
                contactos[posicion_contacto] = agregar_contacto(contactos)
            elif accion == "eliminar":
                seguir = False
                while not seguir:
                    try:
                        email, adecuado = pedir_email(contactos, False)
                        if adecuado is True:
                            seguir = adecuado
                    except ValueError:
                        print("Correo no permitido")
                contactos = eliminar_contacto(contactos, email)
                print(f"Contacto con correo {email} eliminado\n")
            elif accion == "vaciar":
                contactos.clear()
                print("Agenda completamente eliminada\n")
            elif accion == "cargar":
                contactos = cargar_contactos()
                print("Agenda inicial cargada\n")
            elif accion == "mostrar_criterio":
                ensenar_contactos = almacenar_por_criterio(contactos)
                presentar_contactos(ensenar_contactos)
            elif accion == "mostrar_todo":
                presentar_contactos(contactos)
            elif accion == "salir":
                print("Saliendo...")

        else:
            print("Opción inválida. Inténtalo de nuevo.")

        pulse_tecla_para_continuar()
        borrar_consola()

    return contactos


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("Pulse cualquier tecla para continuar\n")
    os.system("pause")


def main():
    """ Función principal del programa
    """
    borrar_consola()
    contactos = cargar_contactos()
    agenda(contactos)


if __name__ == "__main__":
    main()
