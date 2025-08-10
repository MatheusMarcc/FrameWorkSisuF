from orator import Model

class EdicaoCurso(Model):
    __table__ = 'edicao_curso'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False

    def validate(self):
        try:
            if not int(self.edicao_id) >= 1:
                return False
        except:
            return False
        try:
            if not int(self.curso_id) >= 1:
                return False
        except:
            return False
        campos = [
            'vagas_ac', 'vagas_ppi_br', 'vagas_publica_br',
            'vagas_ppi_publica', 'vagas_publica', 'vagas_deficientes'
        ]
        for c in campos:
            try:
                v = int(getattr(self, c, 0) or 0)
                if v < 0:
                    return False
                setattr(self, c, v)
            except:
                return False
        return True

    def save(self, **kwargs):
        if self.validate():
            return super().save(**kwargs)
        return False
