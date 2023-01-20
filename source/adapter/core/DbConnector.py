import os
from sqlalchemy import MetaData, Table, create_engine, engine
from sqlalchemy.sql.expression import func
from sqlalchemy import text


class DbConnector:
    def __init__(self, prop) -> None:
        value = os.getenv(prop['variable'])
        if (value):
            self.__connector = create_engine(value, connect_args={'connect_timeout': 10000}, pool_pre_ping=True)
            conn = self.__connector.connect()
            if conn.closed:
                print("ERROR DB: CONNECTION NOT ESTABLISHED")
        else:
            print("ERROR DB VALUES NOT FOUND")

    def get(self) -> engine.Engine:
        return self.__connector

    def insert(self, table, values: list[dict]):

        meta = MetaData()
        t = Table(table, meta, autoload=True,
                  autoload_with=self.__connector, schema='algoritmo')
        ins = t.insert()
        print("Insertando datos en esquema 'algoritmo' de Epok...")
        self.__connector.execute(ins, values)

    def clear_all(self, table):
        print(f"Eliminando datos de tabla 'algoritmo.{table}'...")
        self.__connector.execute(f"DELETE FROM algoritmo.{table}")

    def execute(self, sql):
        print("Insertando datos en esquema 'public' de Epok...")
        self.__connector.execute(text(sql).execution_options(autocommit=True))
        # self.__connector.execute(func.algoritmo.actualizarciudad3d_2())