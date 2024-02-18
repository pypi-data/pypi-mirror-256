import os.path
import subprocess
import mysql.connector
import sshtunnel
import sqlalchemy
import pandas as pd


with sshtunnel.SSHTunnelForwarder(
        # ("131.234.124.111", 22),
        ("vtux03.lea.uni-paderborn.de", 22),
        ssh_username="nikolasf",
        ssh_password="Doenerbude_4711:)",
        local_bind_address=("127.0.0.1", 3305),
        remote_bind_address=("127.0.0.1", 6432),

) as tunnel:
        print("tunnel establisehd")
        print("---------------------------------")
        print("using sqlalchemy")
        local_port = str(tunnel.local_bind_port)

        # database_url = f"postgresql+pg8000://monty:monty@127.0.0.1:3305/mydb"

        database_url = "postgresql+psycopg2://monty:monty@127.0.0.1:3305/mydb"

        # engine = sqlalchemy.create_engine(f"mysql://monty:@127.0.0.1:3305/mydb")
        engine = sqlalchemy.create_engine(database_url)

        print("done create engine")

        dataDF = pd.read_sql("studies", engine)
        print(dataDF)

        dataDF = pd.read_sql_query("select study_id, study_name from studies;", engine)
        print(dataDF)

        dataDF = pd.read_sql("SELECT * FROM \"{}\";".format("studies"), engine)
        print(dataDF)

        # study = optuna.load_study(study_name=study_name, storage=database_url)
        # #
        # df = study.trials_dataframe(attrs=("number", "value", "params"))

        # print(len(study.best_trials))