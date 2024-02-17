import psycopg2


# POSTGRE ADMIN
class PostgreSQL():
    def __init__(self,dbname, user, password, host, port="5432"):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.parameters = f"dbname={self.dbname} user={self.user} password={self.password} host={self.host} port={self.port}"

    def __call__(self):
        return {"host":self.host,"dbname":self.dbname,"user":self.user,"password":self.password}

    # SE CONECTAR-SE AO BANCO
    def connect(self):
        """open database connection"""
        self.conn = psycopg2.connect(self.parameters)
        self.cursor = self.conn.cursor()
        return self.conn
 
    # SE DESCONECTAR-SE DO BANCO
    def disconnect(self):
        """close the database connection"""
        self.conn.close()

    # CHECAR VERSAO
    def version(self):
        """check the version"""
        self.execute("SELECT version();")
        return self.cursor.fetchone()
    
    # EXECUTAR COMANDOS
    def execute(self,instruction):
        """Execute the instructions"""
        self.cursor.execute(instruction)

    # SALVAR ALTERACOES
    def commit(self):
        """save Changes"""
        return self.conn.commit()
        
    # DELETAR UMA TABELA
    def deleteTable(self,table:str):
        """Delete for table"""
        self.execute(f"""DROP TABLE IF EXISTS {table}""")

    # PEGAR TODOS OS VALORES
    def get(self,table:str):
        """get all values"""
        self.execute(f"""SELECT * FROM {table}""")

        return self.cursor.fetchall()
    
    # PEGAR VALORES ESPECIFICOS
    def getSingleData(self,value:str,table:str,column:str):
        """Get a specific value"""
        self.execute(f"""SELECT * FROM {table} WHERE {column} LIKE ?""", ('%' + value + '%',))

        return self.cursor.fetchall()

    # PEGAR VALORES COMPLETOS
    def getFullData(self,table:str,unique:str):
        """Needs to receive a unique value within a table"""
        self.execute(f"""SELECT * FROM {table} WHERE id LIKE {unique}""")

        return self.cursor.fetchall()


