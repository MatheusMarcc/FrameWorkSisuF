from orator import Model

class Candidato(Model):
    __table__ = 'candidato'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False

    def validate(self):
        if not self.nome or self.nome.strip() == "":
            self.error = "Nome não pode ser vazio"
            return False

        cpf = str(self.cpf or "").strip().replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit() or not self._cpf_valido(cpf):
            self.error = "CPF inválido"
            return False
        self.cpf = cpf

        existente = (Candidato
                     .where("cpf", self.cpf)
                     .where(self.__primary_key__, '!=', getattr(self, self.__primary_key__, 0) or 0)
                     .first())
        if existente:
            self.error = "CPF já cadastrado"
            return False

        if not self.data_nascimento:
            self.error = "Data de nascimento obrigatória"
            return False

        if not self.categoria:
            self.error = "Categoria obrigatória"
            return False

        try:
            if int(self.curso_id) < 1:
                self.error = "Curso inválido"
                return False
        except:
            self.error = "Curso inválido"
            return False

        try:
            n = float(str(self.nota).replace(',', '.'))
            if n < 0 or n > 1000:
                self.error = "Nota deve estar entre 0 e 1000"
                return False
            self.nota = n
        except:
            self.error = "Nota inválida"
            return False

        return True

    def _cpf_valido(self, cpf: str) -> bool:
        if cpf == cpf[0] * 11:
            return False
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        dv1 = (soma * 10) % 11
        dv1 = 0 if dv1 == 10 else dv1
        if dv1 != int(cpf[9]):
            return False
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        dv2 = (soma * 10) % 11
        dv2 = 0 if dv2 == 10 else dv2
        return dv2 == int(cpf[10])

    def save(self, **kwargs):
        if self.validate():
            return super().save(**kwargs)
        return False
