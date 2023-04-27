import pymssql


def open_connection():
    server = '200.155.4.157'
    database = 'WDWebDataEurofarmaPROD'
    user_name = 'alejandro'
    password = 'zelda2020'
    port = '16666'
    Cnx = pymssql.connect(server=server, user=user_name, password=password, database=database, port=port)
    return Cnx


def load_medico_table(cnx):
    """
    :return: Dataframe da tabela de usuários
    """
    query = 'SELECT TOP 10 * FROM _REPORT_Medico_LISTA' \
            ''
    cur = cnx.cursor(as_dict=True)
    cur.execute(query)
    reportMedico = pd.DataFrame.from_dict(cur)
    cur.close()

    return reportMedico


#cnx = open_connection()
#reportMedico = load_medico_table(cnx)
#print(reportMedico.keys())