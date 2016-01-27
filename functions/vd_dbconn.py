# -*- coding: utf-8 -*-
from datetime import datetime
global db_name, db_user
db_name = "reserva"
db_user = "cezar"


def setTotalVagas():
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select morador_id from occ_veiculos where \
                             active = 't';")
            _morador_ids = conn_pgs.fetchall()
            for _morador_id in _morador_ids:
                _total_tag_vaga_moto = 0
                _total_tag_vaga_carro = 0
                with conn_pg.cursor() as conn_pgs2:
                        conn_pgs2.execute("select tag_id from occ_veiculos \
                                          where active = 't' and \
                                          morador_id = (%s);", (_morador_id, ))
                        _tag_ids = conn_pgs2.fetchall()
                        for _tag_id in _tag_ids:
                            conn_pgs2.execute("select tipo from occ_veiculos \
                                              where active = 't' and \
                                              tag_id = (%s);", (_tag_id, ))
                            _tag_tipo = reduce(add, conn_pgs2.fetchone())
                            if _tag_tipo == 'moto':
                                conn_pgs2.execute("select count(*) as records \
                                                  from occ_tag_moto_rel where \
                                                  tag_ids = (%s);", (_tag_id, )
                                                  )
                                _tag_vaga_moto = reduce(add,
                                                        conn_pgs2.fetchone())
                                if _tag_vaga_moto > _total_tag_vaga_moto:
                                        _total_tag_vaga_moto = _tag_vaga_moto
                            if _tag_tipo == 'carro':
                                conn_pgs2.execute("select count(*) as records \
                                                  from occ_tag_carro_rel where\
                                                  tag_ids = (%s);", (_tag_id, )
                                                  )
                                _tag_vaga_carro = reduce(add,
                                                         conn_pgs2.fetchone())
                                if _tag_vaga_carro > _total_tag_vaga_carro:
                                        _total_tag_vaga_carro = _tag_vaga_carro
                with conn_pg.cursor() as conn_pgs3:
                        conn_pgs3.execute("update occ_morador SET \
                                          total_vagas_carro = (%s), \
                                          total_vagas_moto = (%s) \
                                          where id = (%s);",
                                          (_total_tag_vaga_carro,
                                           _total_tag_vaga_moto,
                                           _morador_id, ))


def getVagasDispo(_tag_id, _morador_id, _terminal_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    setTotalVagas()
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select tipo from occ_veiculos where\
                             tag_id = (%s);", (_tag_id, ))
            tipo = conn_pgs.fetchone()
            if tipo is None:
                return False
            else:
                tipo = reduce(add, tipo)
            conn_pgs.execute("select total_vagas_moto from occ_morador where\
                             id = (%s);", (_morador_id, ))
            total_vagas_moto = reduce(add, conn_pgs.fetchone())
            # print 'T Vagas moto:', total_vagas_moto
            conn_pgs.execute("select total_vagas_carro from occ_morador where\
                             id = (%s);", (_morador_id, ))
            total_vagas_carro = reduce(add, conn_pgs.fetchone())
            # print 'T Vagas carro:', total_vagas_carro
            conn_pgs.execute("select dispo_vagas_moto from occ_morador where\
                             id = (%s);", (_morador_id, ))
            dispo_vagas_moto = reduce(add, conn_pgs.fetchone())
            # print 'D Vagas moto:', dispo_vagas_moto
            conn_pgs.execute("select dispo_vagas_carro from occ_morador where\
                             id = (%s);", (_morador_id, ))
            dispo_vagas_carro = reduce(add, conn_pgs.fetchone())
            # print 'D Vagas carro:', dispo_vagas_carro
            conn_pgs.execute("select terminal_tipo from occ_virdi where\
                             id = (%s);", (_terminal_id, ))
            sentido = reduce(add, conn_pgs.fetchone())
            # print 'Sentido', sentido

    if dispo_vagas_moto is None:
        dispo_vagas_moto = 0

    if dispo_vagas_moto > total_vagas_moto:
        dispo_vagas_moto = total_vagas_moto

    if dispo_vagas_carro is None:
        dispo_vagas_carro = 0

    if dispo_vagas_carro > total_vagas_carro:
        dispo_vagas_carro = total_vagas_carro

    if sentido == 'in':
        if tipo == 'moto':
            if dispo_vagas_moto == 0:
                return False
            else:
                # print 'D Vagas moto', dispo_vagas_moto, '->', dispo_vagas_moto - 1
                dispo_vagas_moto -= 1
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_moto = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_moto, _morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'vaga' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
        if tipo == 'carro':
            if dispo_vagas_carro == 0:
                return False
            else:
                # print 'D Vagas carro', dispo_vagas_carro, '->', dispo_vagas_carro - 1
                dispo_vagas_carro -= 1
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_carro = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_carro, _morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'vaga' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True

    if sentido == 'out':
        if tipo == 'moto':
            if dispo_vagas_moto == total_vagas_moto:
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
            else:
                # print 'D Vagas moto', dispo_vagas_moto, '->', dispo_vagas_moto + 1
                dispo_vagas_moto += 1
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_moto = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_moto, _morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))

                return True
        if tipo == 'carro':
            if dispo_vagas_carro == total_vagas_carro:
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
            else:
                # print 'D Vagas carro', dispo_vagas_carro, '->', dispo_vagas_carro + 1
                dispo_vagas_carro += 1
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_carro = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_carro, _morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True


def tagSearch(_tag_name):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select id from occ_tag where name = (%s)\
                             and active = 't';", (_tag_name, ))
            _tag_id = conn_pgs.fetchone()
            if _tag_id is None:
                return False
            else:
                # print 'TAG ID:', reduce(add, _tag_id)
                return reduce(add, _tag_id)


def getMoradorID(_tag_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select morador_id from occ_veiculos where tag_id = (%s)\
                             and active = 't';", (_tag_id, ))
            _morador_id = conn_pgs.fetchone()
            if _morador_id is None:
                return False
            morador_id = reduce(add, _morador_id)
            # print 'MORADOR ID:', morador_id
            return morador_id


def getMorador(_morador_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select name from occ_morador where id = (%s)\
                             and active = 't';", (_morador_id, ))
            _morador = conn_pgs.fetchone()
            if _morador is None:
                return False
            morador = reduce(add, _morador)
            # print 'MORADOR:', morador
            return morador


def getPlacaID(_tag_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select id from occ_veiculos where tag_id = (%s)\
                             and active = 't';", (_tag_id,))
            _placa_id = conn_pgs.fetchone()
            if _placa_id is None:
                return False
            # print 'PLACA:', reduce(add, _placa_id)
            return reduce(add, _placa_id)

def getPlaca(_placa_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select name from occ_veiculos where id = (%s)\
                             and active = 't';", (_placa_id,))
            _placa = conn_pgs.fetchone()
            if _placa is None:
                return False
            # print 'PLACA:', reduce(add, _placa)
            return reduce(add, _placa)


def getApto(_morador_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select apto_id from occ_morador where id = (%s)\
                             and active = 't';", (_morador_id,))
            _apto_id = conn_pgs.fetchone()
            if _apto_id is None:
                return False
            conn_pgs.execute("select name from occ_apto where id = (%s);",
                             (_apto_id,))
            _apto = conn_pgs.fetchone()
            return reduce(add, _apto)


def getSentido(_terminal_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_tipo from occ_virdi where \
                             terminal_id = (%s);", (_terminal_id,))
            _sentido = conn_pgs.fetchone()
            if _sentido is None:
                return False
            return reduce(add, _sentido)


def getAuth(_tag_name, _terminal_id):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

    status_tag = False
    horario = datetime.strftime(datetime.now(), '%Y.%m.%d - %H:%M:%S')
    status_sentido = False
    status_morador = False
    status_placa = False
    status_vaga = False

    _sentido = getSentido(_terminal_id)
    if _sentido is False:
        status_sentido = 'Terminal não cadastrado'
        # print 'Status Terminal:', status_sentido
        return False
    else:
        sentido = _sentido
        status_sentido = True
        # print 'Status Sentido:', status_sentido

    _tag_id = tagSearch(_tag_name)
    if _tag_id is False:
        status_tag = 'TAG não cadastrado'
        # print 'Status TAG:', status_tag
        with psycopg2.connect(database=db_name,
                              user=db_user) as conn_pg:
            with conn_pg.cursor() as conn_pgs:
                conn_pgs.execute("INSERT INTO occ_controle_acesso \
                                 (horario, sentido, morador,\
                                 placa, status) VALUES (%s, \
                                 %s, Null, Null, %s);",
                                 (horario, sentido,
                                  status_tag))
        return False
    else:
        # return True
        tag_id = _tag_id
        status_tag = True
        # print 'Status TAG:', status_tag
        morador_id = getMoradorID(tag_id)
        if morador_id is False:
            status_morador = 'TAG não associado a morador'
            # print 'Status Morador ID:', status_morador
            with psycopg2.connect(database=db_name,
                                  user=db_user) as conn_pg:
                with conn_pg.cursor() as conn_pgs:
                    conn_pgs.execute("INSERT INTO occ_controle_acesso \
                                     (horario, sentido, morador,\
                                     placa, status) VALUES (%s, \
                                     %s, Null, Null, %s);",
                                     (horario, sentido,
                                      status_morador))
            return False
        else:
            placa_id = getPlacaID(tag_id)
            if placa_id is False:
                status_placa = 'Veículo associado ao TAG não tem placa \
                               cadastrada'
                # print 'Status Placa:', status_placa
                return False
            else: 
                _placa = getPlaca(placa_id)
                if _placa is False:
                    status_placa = 'Veículo associado ao TAG não tem placa \
                                   cadastrada'
                    # print 'Status Placa:', status_placa
                    return False
                else:
                    placa = _placa
                    status_placa = True
                    # print 'Status Placa:', status_placa

            vaga = getVagasDispo(tag_id, morador_id, _terminal_id)

            if vaga is False:
                status_vaga = 'Morador já utilizou todas as vagas disponíveis'
                # print 'Status Vaga:', status_vaga
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("INSERT INTO occ_controle_acesso \
                                         (horario, sentido, morador,\
                                         placa, status) VALUES (%s, \
                                         %s, %s, %s, %s);",
                                         (horario, sentido, morador_id,
                                          placa_id, status_vaga))
                return False
            else:
                status_vaga = vaga
                # print 'Status Vaga:', status_vaga

            morador = getMorador(morador_id)
            status_morador = True
            # print 'Status Morador:', status_morador

    if ((status_tag and status_sentido and status_morador and
         status_placa and status_vaga)):
        with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
            with conn_pg.cursor() as conn_pgs:
                conn_pgs.execute("INSERT INTO occ_controle_acesso \
                                 (horario, sentido, morador,\
                                 placa, status) VALUES (%s, \
                                 %s, %s, %s, %s);",
                                 (horario, sentido, morador_id,
                                  placa_id, 'Ok'))
        return True


def setTerminal(_terminal_id, _terminal_ip, _terminal_port):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("update occ_virdi SET terminal_ip = (%s),\
                             terminal_port = (%s) where terminal_id = %s;",
                             (_terminal_ip, _terminal_port, _terminal_id, ))


def getTerminalStatus(_addr):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_status from occ_virdi where \
                             terminal_ip = (%s);", (_addr, ))
            return reduce(add, conn_pgs.fetchone())


def getTerminalID(_addr):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_id from occ_virdi where \
                             terminal_ip = (%s);", (_addr, ))
            return reduce(add, conn_pgs.fetchone())


def setTerminalStatus(_tid):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("update occ_virdi SET terminal_status = 'close' \
                             where terminal_id = %s;", (_tid, ))
