# -*- coding: utf-8 -*-


def tagSearch(_tag_name):

    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="alpha", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select id from occ_tag where name = (%s)\
                             and active = 't';", (_tag_name,))
            _tag_id = conn_pgs.fetchone()
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select name from occ_veiculos where tag_id = (%s)\
                             ;", (_tag_id,))
            veiculo = conn_pgs.fetchone()
            return veiculo


def vagaSearch(_tag_name):

    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    with psycopg2.connect(database="alpha", user="cezar") as conn_pg:
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select id from occ_tag where name = (%s);",
                             (_tag_name,))
            _tag_id = conn_pgs.fetchone()
        with conn_pg.cursor() as conn_pgs:
            conn_pgs.execute("select name from occ_veiculos where tag_id = (%s)\
                             ;", (_tag_id,))
            veiculo = conn_pgs.fetchone()
            return veiculo
