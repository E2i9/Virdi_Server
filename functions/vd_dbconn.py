# -*- coding: utf-8 -*-
def setTotalVagas():
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
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


def tagSearch(_tag_name):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select id from occ_tag where name = (%s)\
                             and active = 't';", (_tag_name,))
            _tag_id = conn_pgs.fetchone()
            if _tag_id is None:
                return False
            else:
                return _tag_id


def getVeiculo(_tag_id):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    if _tag_id is False:
        return False
    else:
        with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
            with conn_pg.cursor() as conn_pgs:
                conn_pgs.execute("select name from occ_veiculos where tag_id = (%s)\
                                 and active = 't';", (_tag_id,))
                _veiculo_name = conn_pgs.fetchone()
                if _veiculo_name is None:
                    return False
                else:
                    return True


def getVagasDispo(_tag_id, _terminal_id):
    from operator import add
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    setTotalVagas()
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select tipo from occ_veiculos where\
                             tag_id = (%s);", (_tag_id, ))
            tipo = conn_pgs.fetchone()
            if tipo is None:
                return False
            else:
                tipo = reduce(add, tipo)
            conn_pgs.execute("select morador_id from occ_veiculos where\
                             tag_id = (%s);", (_tag_id, ))
            morador_id = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select name from occ_morador where id = (%s);",
                             (morador_id, ))
            morador = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select name from occ_veiculos where\
                             tag_id = (%s);", (_tag_id, ))
            veiculo = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select total_vagas_moto from occ_morador where\
                             id = (%s);", (morador_id, ))
            total_vagas_moto = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select total_vagas_carro from occ_morador where\
                             id = (%s);", (morador_id, ))
            total_vagas_carro = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select dispo_vagas_moto from occ_morador where\
                             id = (%s);", (morador_id, ))
            dispo_vagas_moto = reduce(add, conn_pgs.fetchone())
            conn_pgs.execute("select dispo_vagas_carro from occ_morador where\
                             id = (%s);", (morador_id, ))
            dispo_vagas_carro = reduce(add, conn_pgs.fetchone())
            print 'Morador', morador
            print 'Placa', veiculo
    if dispo_vagas_moto > total_vagas_moto:
        dispo_vagas_moto = total_vagas_moto

    if dispo_vagas_moto is None:
        dispo_vagas_moto = 0

    if dispo_vagas_carro > total_vagas_carro:
        dispo_vagas_carro = total_vagas_carro

    if dispo_vagas_carro is None:
        dispo_vagas_carro = 0

    if _terminal_id == 1:
        print 'Portão de Entrada'
        if tipo == 'moto':
            if dispo_vagas_moto == 0:
                return False
            else:
                dispo_vagas_moto -= 1
                print ("Dispo vaga moto", dispo_vagas_moto + 1, "->",
                       dispo_vagas_carro)
                with psycopg2.connect(database="reserva",
                                      user="cezar") as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_moto = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_moto, morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'vaga' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
        if tipo == 'carro':
            if dispo_vagas_carro == 0:
                return False
            else:
                dispo_vagas_carro -= 1
                print ("Dispo vaga carro", dispo_vagas_carro + 1, "->",
                       dispo_vagas_carro)
                with psycopg2.connect(database="reserva",
                                      user="cezar") as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_carro = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_carro, morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'vaga' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True

    if _terminal_id == 2:
        print 'Portão de saída'
        if tipo == 'moto':
            if dispo_vagas_moto == total_vagas_moto:
                print 'Vagas = Total', (dispo_vagas_moto - total_vagas_moto)
                with psycopg2.connect(database="reserva",
                                      user="cezar") as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
            else:
                dispo_vagas_moto += 1
                print ("Dispo vaga moto", dispo_vagas_moto - 1, "->",
                       dispo_vagas_moto)
                with psycopg2.connect(database="reserva",
                                      user="cezar") as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_moto = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_moto, morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))

                return True

        if tipo == 'carro':
            if dispo_vagas_carro == total_vagas_carro:
                with psycopg2.connect(database="reserva",
                                      user="cezar") as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True
            else:
                dispo_vagas_carro += 1
                print ("Dispo vaga carro", dispo_vagas_carro - 1, "->",
                       dispo_vagas_carro)
                with psycopg2.connect(database="reserva",
                                      user="cezar") as conn_pg:
                    with conn_pg.cursor() as conn_pgs:
                        conn_pgs.execute("update occ_morador SET \
                                         dispo_vagas_carro = (%s) \
                                         where id = (%s);",
                                         (dispo_vagas_carro, morador_id))
                        conn_pgs.execute("update occ_veiculos SET status = 'fora' \
                                         where tag_id = (%s);", (_tag_id, ))
                return True


def getAuth(_tag_name, _terminal_id):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    _tag_id = tagSearch(_tag_name)
    if _tag_id is False:
        return False
    else:
        print '\nTAG', _tag_name
        auth = getVeiculo(_tag_id)
        vaga = getVagasDispo(_tag_id, _terminal_id)
        print 'Auth:', auth
        print 'Vaga:', vaga
    if auth and vaga:
        return True
    else:
        return False


def setTerminal(_terminal_id, _terminal_ip, _terminal_port):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("update occ_virdi SET terminal_ip = (%s),\
                             terminal_port = (%s) where terminal_id = %s;",
                             (_terminal_ip, _terminal_port, _terminal_id, ))


def getTerminalStatus(_addr):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_status from occ_virdi where \
                             terminal_ip = (%s);", (_addr, ))
            return reduce(lambda x, y: x, conn_pgs.fetchone())


def getTerminalID(_addr):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select terminal_id from occ_virdi where \
                             terminal_ip = (%s);", (_addr, ))
            return conn_pgs.fetchone()


def setTerminalStatus(_tid):
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("update occ_virdi SET terminal_status = True \
                             where terminal_id = %s;", (_tid, ))
