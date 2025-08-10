from controllers.Controller import Controller
from models.Edicao import Edicao
from models.Curso import Curso

class EdicaoController(Controller):
    def index(self):
        self.redirectPage('/app/dashboard/index', {'tab': 'edicao'})

    def create(self):
        self.redirectPage('/app/dashboard/index', {'tab': 'edicao'})

    def store(self):
        data = self.loadNestedForm()
        data.pop('id', None)
        cursos_data = data.pop("cursos", [])
        ed = Edicao()
        ed.nome = data.get("nome")
        if not ed.save_many(cursos_data):
            self.redirectPage('/app/dashboard/index', {
                'tab': 'edicao',
                'error': getattr(ed, "error", "Falha ao salvar")
            })
            return
        self.redirectPage('/app/dashboard/index', {'msg': 'cadastrado', 'tab': 'edicao'})

    def edit(self):
        eid = int(self.environ['params']['id'])
        self.redirectPage('/app/dashboard/index', {'tab': 'edicao', 'id': eid})

    def update(self):
        data = self.loadNestedForm()
        cursos_data = data.pop("cursos", [])
        eid = int(data.get("id", 0)) #aqui guarda o id, pra poder alterar sem duplicar id´s fixos ao editar
        ed = Edicao.find(eid)
        ed.nome = data.get("nome", ed.nome)
        if not ed.save_many(cursos_data):
            self.redirectPage('/app/dashboard/index', {
                'tab': 'edicao',
                'id': eid,
                'error': getattr(ed, "error", "Falha ao salvar")
            })
            return
        self.redirectPage('/app/dashboard/index', {'msg': 'editado', 'tab': 'edicao'})

    def delete(self):
        eid = int(self.environ['params']['id'])
        ed = Edicao.find(eid)
        if ed:
            ed.delete()
        self.redirectPage('/app/dashboard/index', {'msg': 'excluido', 'tab': 'edicao'})
