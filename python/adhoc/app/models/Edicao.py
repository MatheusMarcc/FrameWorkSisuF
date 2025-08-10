from orator import Model
from orator.exceptions.query import QueryException
from models.EdicaoCurso import EdicaoCurso

class Edicao(Model):
    __table__ = 'edicao'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False

    def validate(self):
        if not getattr(self, 'nome', None) or str(self.nome).strip() == '':
            return False
        if len(str(self.nome)) > 40:
            return False
        return True

    def _validate_detalhe(self, idx, cd):
        try:
            curso_id = int(cd.get('curso_id', 0))
            if curso_id < 1:
                return False
        except:
            return False
        campos = [
            'vagas_ac', 'vagas_ppi_br', 'vagas_publica_br',
            'vagas_ppi_publica', 'vagas_publica', 'vagas_deficientes'
        ]
        for c in campos:
            v = cd.get(c, 0)
            try:
                iv = int(v if v not in (None, '') else 0)
                if iv < 0:
                    return False
                cd[c] = iv 
            except:
                return False
        cd['curso_id'] = curso_id
        return True

    def save_many(self, cursos_data):
        if not self.validate():
            return False
        db = Model.get_connection_resolver()
        conn = db.connection(self.get_connection_name())

        conn.begin_transaction()
        try:
            super(Edicao, self).save()
            detalhes = cursos_data or []
            for i, cd in enumerate(detalhes):
                if not self._validate_detalhe(i, cd):
                    conn.rollback()
                    return False
                
            EdicaoCurso.where('edicao_id', self.id).delete()
            for cd in detalhes:
                ec = EdicaoCurso()
                ec.fill(cd)
                ec.edicao_id = self.id
                if not ec.save():
                    conn.rollback()
                    return False
            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise QueryException(self, [], e)
