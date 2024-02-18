import time
import allure
from Andreani_QA_parameters.Parameters import Parameters
from Andreani_QA_Functions.Functions import Functions
import requests


class Api(Functions, Parameters):
    # Api Framework

    def send_request(self, data_request: dict):
        return RequestObj(data_request['METHOD'], data_request['ENDPOINT'], data_request['BODY'], data_request['HEADERS'])

class RequestObj:
    def __init__(self, metodo, endpoint, body, headers):
        self.metodo = metodo
        self.endpoint = endpoint
        self.body = body
        self.headers = headers
        self.request_result = None

    def send_request(self):
        # normalizar request_type
        method = self.metodo.upper()
        if method == "GET":
            self.request_result = self.send_get_request(self.endpoint, self.body, self.headers)
        if method == "POST":
            self.request_result = self.send_post_request(self.endpoint, self.body, self.headers)
        if method == "PUT":
            self.request_result = self.send_put_request(self.endpoint, self.body, self.headers)
        if method == "DELETE":
            self.request_result = self.send_delete_request(self.endpoint, self.body, self.headers)
        return self.request_result

    def send_get_request(self, endpoint, data=None, headers=None):
        get_response = None
        try:
            while get_response is None:
                # Se realiza el llamado a la api, si falla reintenta nuevamente.
                    if data is None:
                        get_response = requests.get(url=endpoint, headers=headers)
                    if headers is None:
                        get_response = requests.get(url=endpoint, data=data)
                    if headers is None and data is None:
                        get_response = requests.get(url=endpoint)
                    if headers is not None and data is not None:
                        get_response = requests.get(url=endpoint, data=data, headers=headers)
            return get_response
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def send_post_request(self, endpoint, data=None, headers=None):
        post_response = None
        try:
            while post_response is None:
                # Se realiza el llamado a la api, si falla reintenta nuevamente.
                    if data is None:
                        post_response = requests.post(url=endpoint, headers=headers)
                    if headers is None:
                        post_response = requests.post(url=endpoint, data=data)
                    if headers is not None and data is not None:
                        post_response = requests.post(url=endpoint, data=data, headers=headers)
            return post_response
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def send_put_request(self, endpoint, data=None, headers=None):
        put_response = None
        try:
            while put_response is None:
                # Se realiza el llamado a la api, si falla reintenta nuevamente.
                if data is None:
                    put_response = requests.put(url=endpoint, headers=headers)
                if headers is None:
                    put_response = requests.put(url=endpoint, data=data)
                if headers is not None and data is not None:
                    put_response = requests.put(url=endpoint, data=data, headers=headers)
            return put_response
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def send_delete_request(self, endpoint, data=None, headers=None):
        delete_response = None
        try:
            while delete_response is None:
                # Se realiza el llamado a la api, si falla reintenta nuevamente.
                if data is None:
                    delete_response = requests.delete(url=endpoint, headers=headers)
                if headers is None:
                    delete_response = requests.delete(url=endpoint, data=data)
                if headers is not None and data is not None:
                    delete_response = requests.delete(url=endpoint, data=data, headers=headers)
            return delete_response
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def calculate_response_time(self):
        """
            :param url: Obligatorio - Url del endpoint a consultar
            :param headers: Optativo
            :param body: Optativo
            :return: Retorna el tiempo resultante (float) desde el inicio del request hasta su respuesta.
        """
        inicio = time.time()
        if self.headers is None and self.body is None:
            requests.get(self.endpoint)
        else:
            requests.get(self.endpoint, data=self.body, headers=self.headers)
        fin = time.time()
        tiempo_total = fin - inicio
        return round(tiempo_total, 2)

    def validate_status_code(self, estado_deseado):
        self.send_request()
        if self.request_result.status_code == estado_deseado:
            print("El estado de la respuesta es el deseado:", estado_deseado)
            return True
        else:
            print("El estado de la respuesta no es el deseado. Se esperaba:", estado_deseado, "pero se recibió:",
                  self.request_result.status_code)
            return False

    def validate_request_body(self, estructura_deseada) -> dict:
        self.send_request()
        try:
            json_respuesta = self.request_result.json()
        except ValueError:
            print("La respuesta no es un JSON válido.")
            return {"Error": "La respuesta no es un JSON válido."}

        if type(json_respuesta) != type(estructura_deseada):
            print("La estructura de la respuesta no coincide con la estructura deseada.")
            return {"validate": False, "json_esperado": json_respuesta, "json_recibido": estructura_deseada}

        if json_respuesta != estructura_deseada:
            print("El contenido de la respuesta no coincide con la estructura deseada.")
            return {"validate": False, "json_esperado": json_respuesta, "json_recibido": estructura_deseada}

        print("La respuesta tiene la estructura deseada.")
        return {"validate": True, "json_esperado": json_respuesta, "json_recibido": estructura_deseada}

    def response_to_allure_report(self, estructura_deseada):
        self.send_request()
        allure.attach(self.request_result.text, "Respuesta JSON obtenida", allure.attachment_type.JSON)
        json_respuesta = self.request_result.json()

        allure.attach(json_respuesta, "JSON obtenido", allure.attachment_type.JSON)
        allure.attach(estructura_deseada, "JSON esperado", allure.attachment_type.JSON)

        if json_respuesta != estructura_deseada:
            print("El contenido de la respuesta no coincide con la estructura deseada.")
            print("Respuesta obtenida:", json_respuesta)
            print("Respuesta esperada:", estructura_deseada)
            return False

        print("La respuesta tiene la estructura deseada.")
        return True

    ###########################################   BASES DE DATOS  ######################################################
    def set_timeout_base_sql_server(self, time_seconds):

        """
            Description:
                Configura el value de timeout (segundos) configurado para las conexiones a bases sqlServer.
            Args:
                time_seconds: Valor (int) que representa una cantidad en segundos.
        """

        Functions.set_timeout_base_sql_server(self, time_seconds)

    def get_timeout_base_sql_server(self):

        """
            Description:
                Devuelve el value de timeout configurado para la conexion a bases sqlServer.
            Return:
                Devuelve el value de timeout (segundos) configurado para la conexion a bases sqlServer.
        """

        return Functions.get_timeout_base_sql_server(self)

    def establish_connection_sqlserver(self, db_name):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                server: Servidor ip
                base: nombre de la base
                user: usuario
                password: Contraseña
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return Functions.establish_connection_sqlserver(self, db_name)

    def check_base_sqlserver(self, db_name, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                db_name: Nombre de la data base.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """

        return Functions.check_base_sqlserver(self, db_name, query)

    def execute_sp_base_sqlserver(self, db_name, query, parameters: tuple):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server (str): Servidor ip.
                base (str): Nombre de la base.
                user (str): Usuario.
                password (str): Contraseña.
                query (str): Consulta Query.
                parameters (tuple): Tupla con parametros para el sp.
            Returns:
                Lista con los resultados.
        """

        return Functions.execute_sp_base_sqlserver(self, db_name, query, parameters)

    def get_list_base_sqlserver(self, db_name, query):
        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server (str): Servidor ip.
                base (str): Nombre de la base.
                user (str): Usuario.
                password (str): Contraseña.
                query (str): Consulta Query.
            Returns:
                Lista con los resultados.
        """

        return Functions.get_list_base_sqlserver(self, db_name, query)

    def delete_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Elimina un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.delete_reg_base_sqlserver(self, db_name, query)

    def insert_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Inserta un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.insert_row_base_sqlserver(self, db_name, query)

    def update_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Actualiza un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.update_row_base_sqlserver(self, db_name, query)

    def establish_connection_oracle(self, db_name):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                server: Servidor ip
                base: nombre de la base
                user: usuario
                password: Contraseña
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return Functions.establish_connection_oracle_db(self, db_name)

    def check_base_oracle(self, db_name, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria xOracle. El metodo incluye la
                desconexión.
            Args:
                db_name: Nombre de la data base.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """
        return Functions.check_base_oracle_db(self, db_name, query)
