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
            conn_pgs.execute("select name from occ_morador where id = (%s);",
                             (_morador_id, ))
            total_vagas_moto = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select total_vagas_carro from occ_morador where\
                             id = (%s);", (_morador_id, ))
            total_vagas_carro = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select dispo_vagas_moto from occ_morador where\
                             id = (%s);", (_morador_id, ))
            dispo_vagas_moto = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select dispo_vagas_carro from occ_morador where\
                             id = (%s);", (_morador_id, ))
            dispo_vagas_carro = reduce(add, conn_pgs.fetchone())
    if dispo_vagas_moto > total_vagas_moto:
        dispo_vagas_moto = total_vagas_moto

    if dispo_vagas_moto is None:
        dispo_vagas_moto = 0

    if dispo_vagas_carro > total_vagas_carro:
        dispo_vagas_carro = total_vagas_carro

    if dispo_vagas_carro is None:
        dispo_vagas_carro = 0

    if _terminal_id == 1:
        if tipo == 'moto':
            if dispo_vagas_moto == 0:
                return False
            else:
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

    if _terminal_id == 2:
        if tipo == 'moto':
            if dispo_vagas_moto == total_vagas_moto:
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
            else:
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
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select id from occ_tag where name = (%s)\
                             and active = 't';", (_tag_name,))
            _tag_id = conn_pgs.fetchone()
            if _tag_id is None:
                return False
            else:
                return _tag_id


def getDadosMorador(_tag_id):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select morador_id from occ_veiculos where tag_id = (%s)\
                             and active = 't';", (_tag_id,))
            _morador_id = conn_pgs.fetchone()
            if _morador_id is None:
                return False
            _morador_id = reduce(lambda x, y: x, conn_pgs.fetchone())

            conn_pgs.execute("select name from occ_morador where id = (%s)\
                             and active = 't';", (_morador_id,))
            _morador = reduce(lambda x, y: x, conn_pgs.fetchone())

            conn_pgs.execute("select image from occ_morador where id = (%s)\
                             and active = 't';", (_morador_id,))
            _foto = conn_pgs.fetchone()

            return {'0': _morador_id,
                    '1': _foto,
                    '2': _morador}


def getPlaca(_tag_id):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select name from occ_veiculos where name = (%s)\
                             and active = 't';", (_tag_id,))
            _placa = conn_pgs.fetchone()
            if _placa is None:
                return False
            return reduce(lambda x, y: x, _placa)


def getApto(_morador_id):
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
            return reduce(lambda x, y: x, _apto)


def getSentido(_terminal_id):
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
            return reduce(lambda x, y: x, _sentido)


def getAuth(_tag_name, _terminal_id):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

    horario = datetime.strftime(datetime.now(), '%H:%M:%S - %d/%m/%Y')

    _tag_id = tagSearch(_tag_name)
    if _tag_id is False:
        status_tag = 'TAG não cadastrado'
    else:
        tag_id = _tag_id
        status_tag = True
        _dadosmorador = getDadosMorador(_tag_id)
        if _dadosmorador is False:
            status_morador = 'Morador não cadastrado'
        else:
            morador_id = _dadosmorador[0]
            foto = _dadosmorador[1]
            morador = _dadosmorador[2]
            status_morador = True

        _placa = getPlaca(tag_id)
        if _placa is False:
            status_placa = 'Veículo não cadastrado'
        else:
            placa = _placa
            status_placa = True

        _apto = getApto(tag_id)
        if _apto is False:
            status_apto = 'Apartamento não cadastrado'
        else:
            apto = _apto
            status_apto = True
        vaga = getVagasDispo(tag_id, morador_id, _terminal_id)

    _sentido = getSentido(_terminal_id)
    if _sentido is False:
        status_sentido = 'Terminal não cadastrado'
    else:
        sentido = _sentido
        status_sentido = True

    if ((status_tag and status_sentido and status_morador and
         status_placa and status_apto and vaga)):
        with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
            with conn_pg.cursor() as conn_pgs:
                conn_pgs.execute("INSERT INTO occ_acesso \
                                 (image, morador, apto, placa, \
                                  sentido, horario, status) \
                                 VALUES (%s, %s, %s, %s, %s, %s, %s);",
                                 (foto, morador, apto, placa,
                                  sentido, horario, 'OK'))
        return True
    else:
        if status_tag is True:
            if status_sentido is True:
                if status_morador is True:
                    if status_placa is True:
                        if status_apto is True:
                            with psycopg2.connect(database=db_name,
                                                  user=db_user) as conn_pg:
                                with conn_pg.cursor() as conn_pgs:
                                    conn_pgs.execute("INSERT INTO occ_acesso \
                                                     (sentido, image, morador,\
                                                      placa, apto, horario, \
                                                     status) VALUES (%s, %s, \
                                                     %s, %s, %s, %s, %s);",
                                                     (sentido, foto, morador,
                                                      placa, apto, horario,
                                                      'Sem vaga disponível'))
                            return False
                        else:
                            with psycopg2.connect(database=db_name,
                                                  user=db_user) as conn_pg:
                                with conn_pg.cursor() as conn_pgs:
                                    conn_pgs.execute("INSERT INTO occ_acesso \
                                                     (sentido, image, morador,\
                                                      placa, apto, horario, \
                                                     status) VALUES (%s, %s, \
                                                     %s, %s, %s, %s, %s);",
                                                     (sentido, foto, morador,
                                                      placa, 'Erro', horario,
                                                      status_apto))
                            return False
                    else:
                        with psycopg2.connect(database=db_name,
                                              user=db_user) as conn_pg:
                            with conn_pg.cursor() as conn_pgs:
                                conn_pgs.execute("INSERT INTO occ_acesso \
                                                 (sentido, image, morador,\
                                                  placa, apto, horario, \
                                                 status) VALUES (%s, %s, \
                                                 %s, %s, %s, %s, %s);",
                                                 (sentido, foto, morador,
                                                  'Erro', 'nc', horario,
                                                  status_placa))
                        return False
                else:
                    with psycopg2.connect(database=db_name,
                                          user=db_user) as conn_pg:
                        with conn_pg.cursor() as conn_pgs:
                            conn_pgs.execute("INSERT INTO occ_acesso \
                                             (sentido, image, morador,\
                                              placa, apto, horario, \
                                             status) VALUES (%s, %s, \
                                             %s, %s, %s, %s, %s);",
                                             (sentido, None, 'Erro',
                                              'nc', 'nc', horario,
                                              status_morador))
                    return False
            else:
                with psycopg2.connect(database=db_name,
                                      user=db_user) as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("INSERT INTO occ_acesso \
                                         (sentido, image, morador,\
                                          placa, apto, horario, \
                                         status) VALUES (%s, %s, \
                                         %s, %s, %s, %s, %s);",
                                         ('Erro', None, 'nc',
                                          'nc', 'nc', horario,
                                          status_sentido))
                return False
        else:
            with psycopg2.connect(database=db_name,
                                  user=db_user) as conn_pg:
                with conn_pg.cursor() as conn_pgs:
                    conn_pgs.execute("INSERT INTO occ_acesso \
                                     (sentido, image, morador,\
                                      placa, apto, horario, \
                                     status) VALUES (%s, %s, \
                                     %s, %s, %s, %s, %s);",
                                     ('Erro', None, 'nc',
                                      'nc', 'nc', horario,
                                      status_tag))
            return False


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
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_status from occ_virdi where \
                             terminal_ip = (%s);", (_addr, ))
            return reduce(lambda x, y: x, conn_pgs.fetchone())


def getTerminalID(_addr):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_id from occ_virdi where \
                             terminal_ip = (%s);", (_addr, ))
            return conn_pgs.fetchone()


def setTerminalStatus(_tid):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database=db_name, user=db_user) as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("update occ_virdi SET terminal_status = 'close' \
                             where terminal_id = %s;", (_tid, ))
