import sqlite3


connection = None 
cursor = None

def connect():
    global connection,  cursor
    connection = sqlite3.connect("banco.db")
    cursor = connection.cursor()

def execute(sql, final = 'retorno'):
    global connection,  cursor
    try:
        try: 
            cursor.execute(sql)
        except:
            connect()
            cursor.execute(sql)

        if final == 'commit':
            connection.commit()

            return 'ok'
        elif final == 'retorno':
            retorno = cursor.fetchall() 
            return retorno
        else:
            return 'sem_final'
    except Exception as e:
        print(e)
        return 'falha'

def exemplo_select():
    sql = f"""
    SELECT coluna1
    FROM exemplo
    """
    consulta = execute(sql,'retorno')
    resposta = []
    for linha in consulta:
        resposta.append(linha[0])
    return resposta

def exemplo_insert(info):
    
    sql = f"""
    INSERT INTO exemplo
    (coluna1)
    VALUES('{info}');
    """
    acao = execute(sql,'commit')
    if acao == 'ok':
        return 'ok'
    else:
        return 'falha'

def select_status_captacao():
    sql = f"""
    SELECT valor
    FROM controle
    where chave = 'captacao'
    """
    consulta = execute(sql,'retorno')
    return consulta[0][0]

def insert_nova_captura(arquivo):
    sql = f"""
    INSERT INTO transcricoes
    (arquivo)
    VALUES('{arquivo}');
    """
    acao = execute(sql,'commit')
    if acao == 'ok':
        return 'ok'
    else:
        return 'falha'

def update_transcricao(arquivo,transcricao):
    sql = f"""
    UPDATE transcricoes
    SET transcricao='{transcricao}'
    WHERE arquivo='{arquivo}';
    """
    acao = execute(sql,'commit')
    if acao == 'ok':
        return 'ok'
    else:
        return 'falha'

def update_traducao(arquivo,traducao):
    sql = f"""
    UPDATE transcricoes
    SET traducao='{traducao}'
    WHERE arquivo='{arquivo}';
    """
    acao = execute(sql,'commit')
    if acao == 'ok':
        return 'ok'
    else:
        return 'falha'

def insert_nova_saida(
      nome_arquivo
    , portugues
    , ingles):
    
    
    sql = f"""
    INSERT INTO saida
    (
      nome_arquivo
    , portugues
    , ingles
    )
    VALUES
    (
      '{nome_arquivo    }'
    , '{portugues       }'
    , '{ingles          }'
    )
    """
    acao = execute(sql,'commit')
    if acao == 'ok':
        return 'ok'
    else:
        return 'falha'

def select_saidas_existentes():
    sql = f"""
    
    SELECT nome_arquivo, portugues, ingles
    FROM saida    
    order by id_saida
    """
    consulta = execute(sql,'retorno')
    resposta = []
    for linha in consulta:
        resposta.append({
              'nome_arquivo'    : linha[0]
            , 'portugues'       : linha[1]
            , 'ingles'          : linha[2]
        })
        pass

    return resposta

if __name__ == "__main__":
    # status_captacao = select_status_captacao()
    # print(status_captacao)


    print('\n\n')
    saidas_existentes = select_saidas_existentes()
    print(saidas_existentes)

    pass