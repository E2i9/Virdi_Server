import psycopg2.extensions
from operator import add
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

with psycopg2.connect(database="alpha", user="cezar") as conn_pg:
    with conn_pg.cursor() as conn_pgs:
        conn_pgs.execute("select name from occ_apto;")
	aptos = reduce(add, conn_pgs.fetchall())
	for apto in aptos:
		with conn_pg.cursor() as conn_pgs2:
			conn_pgs2.execute("select id from occ_vaga_moto where name = (%s);", (apto,))
        		_vaga_carro_id = conn_pgs2.fetchone()
			with conn_pg.cursor() as conn_pgs3:
				conn_pgs3.execute("update occ_apto set vaga_moto_id = (%s) where name = (%s);", (_vaga, apto,))
                with conn_pg.cursor() as conn_pgs4:
                        conn_pgs4.execute("select id from occ_vaga_carro where name = (%s);", (apto,))
                        _vaga = conn_pgs4.fetchone()
                        with conn_pg.cursor() as conn_pgs5:
                                conn_pgs5.execute("update occ_apto set vaga_carro_id = (%s) where name = (%s);", (_vaga, apto,))

