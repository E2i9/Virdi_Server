import psycopg2.extensions
from operator import add
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

with psycopg2.connect(database="reserva", user="cezar") as conn_pg:
    with conn_pg.cursor() as conn_pgs:
        conn_pgs.execute("select tag_id from occ_veiculos where active = 't';")
        _tag_ids = conn_pgs.fetchall()
	for _tag_id in _tag_ids:
		with conn_pg.cursor() as conn_pgs2:
			conn_pgs2.execute("select morador_id from occ_veiculos where active = 't' and tag_id = (%s);", (_tag_id, ))
			_morador_id = conn_pgs2.fetchone()
		with conn_pg.cursor() as conn_pgs2:
			conn_pgs2.execute("select apto_id from occ_morador where active = 't' and id = (%s);", (_morador_id, ))
			_apto_id = conn_pgs2.fetchone()
                with conn_pg.cursor() as conn_pgs2:
                        conn_pgs2.execute("select vaga_carro_id from occ_apto where id = (%s);", (_apto_id, ))
                        _vaga_carro_id = conn_pgs2.fetchone()
			conn_pgs2.execute("select vaga_moto_id from occ_apto where id = (%s);", (_apto_id, ))
                        _vaga_moto_id = conn_pgs2.fetchone()
			conn_pgs2.execute("select tipo from occ_tag where id = (%s);", (_tag_id, ))
			_tag_tipo = reduce(add, conn_pgs2.fetchone())
			if _tag_tipo == 'carro':
				conn_pgs2.execute("INSERT INTO occ_tag_carro_rel (vaga_carro_ids, tag_ids) VALUES (%s, %s);", (_vaga_carro_id, _tag_id))
				conn_pgs2.execute("delete from occ_tag_moto_rel where tag_ids = (%s);", (_tag_id, ))
			if _tag_tipo == 'moto':
	                        conn_pgs2.execute("INSERT INTO occ_tag_moto_rel (vaga_moto_ids, tag_ids) VALUES (%s, %s);", (_vaga_moto_id, _tag_id))
				conn_pgs2.execute("delete from occ_tag_carro_rel where tag_ids = (%s);", (_tag_id, ))

