from controllers.Controller import Controller
from models.Curso import Curso
import cgi

class CursoController(Controller):
    def index(self):
        self.redirectPage('/app/dashboard/index', {'tab': 'curso'})

    def create(self):
        self.redirectPage('/app/dashboard/index', {'tab': 'curso'})

    def store(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        data.pop('id', None)  # evita INSERT com id fixo
        curso = Curso()
        curso.fill(data)
        if not curso.save():
            self.redirectPage('/app/dashboard/index', {
                'tab': 'curso',
                'error': getattr(curso, "error", "Falha ao salvar")
            })
            return
        self.redirectPage('/app/dashboard/index', {'msg': 'cadastrado', 'tab': 'curso'})

    def edit(self):
        cid = int(self.environ['params']['id'])
        self.redirectPage('/app/dashboard/index', {'tab': 'curso', 'id': cid})

    def update(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        cid = int(data.get("id", 0))
        curso = Curso.find(cid)
        curso.nome = data.get("nome", "")
        if not curso.save():
            self.redirectPage('/app/dashboard/index', {
                'tab': 'curso',
                'id': cid,
                'error': getattr(curso, "error", "Falha ao salvar")
            })
            return
        self.redirectPage('/app/dashboard/index', {'msg': 'editado', 'tab': 'curso'})

    def delete(self):
        cid = int(self.environ['params']['id'])
        curso = Curso.find(cid)
        if curso:
            curso.delete()
        self.redirectPage('/app/dashboard/index', {'msg': 'excluido', 'tab': 'curso'})
