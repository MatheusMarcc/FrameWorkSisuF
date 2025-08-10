from controllers.Controller import Controller
from models.Candidato import Candidato
import cgi

class CandidatoController(Controller):
    def index(self):
        self.redirectPage('/app/dashboard/index', {'tab': 'candidato'})

    def create(self):
        self.redirectPage('/app/dashboard/index', {'tab': 'candidato'})

    def store(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        candidato = Candidato()
        candidato.fill(data)
        if not candidato.save():
            self.redirectPage('/app/dashboard/index', {
                'tab': 'candidato',
                'error': getattr(candidato, "error", "Falha ao salvar")
            })
            return
        self.redirectPage('/app/dashboard/index', {'msg': 'cadastrado', 'tab': 'candidato'})

    def edit(self):
        cid = int(self.environ['params']['id'])
        self.redirectPage('/app/dashboard/index', {'tab': 'candidato', 'id': cid})

    def update(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        id = int(data.get("id", 0))
        candidato = Candidato.find(id)
        candidato.nome = data.get("nome", "")
        candidato.cpf = data.get("cpf", "")
        candidato.data_nascimento = data.get("data_nascimento", "")
        candidato.categoria = data.get("categoria", "")
        candidato.curso_id = int(data.get("curso_id", 0)) if str(data.get("curso_id", 0)).isdigit() else 0
        candidato.nota = data.get("nota", 0)
        if not candidato.save():
            self.redirectPage('/app/dashboard/index', {
                'tab': 'candidato',
                'id': id,
                'error': getattr(candidato, "error", "Falha ao salvar")
            })
            return
        self.redirectPage('/app/dashboard/index', {'msg': 'editado', 'tab': 'candidato'})

    def delete(self):
        cid = int(self.environ['params']['id'])
        candidato = Candidato.find(cid)
        if candidato:
            candidato.delete()
        self.redirectPage('/app/dashboard/index', {'msg': 'excluido', 'tab': 'candidato'})
