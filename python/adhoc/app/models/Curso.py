from orator import Model

class Curso(Model):
    __table__ = 'curso'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False

    def validate(self):
        if not self.nome or self.nome.strip() == "":
            return False
        if len(self.nome) > 120:
            return False
        return True

    def save(self, **kwargs):
        if self.validate():
            return super().save(**kwargs)
        return False
