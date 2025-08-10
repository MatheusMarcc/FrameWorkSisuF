from controllers.Controller import Controller
from models.Curso import Curso
from models.Edicao import Edicao
from models.Candidato import Candidato
from models.EdicaoCurso import EdicaoCurso

class DashboardController(Controller):
    def index(self):
        params = self.environ.get('params', {})
        tab = params.get('tab', '')
        msg = params.get('msg', '')
        error = params.get('error', '')

        cursos = Curso.all()
        edicoes = Edicao.all()
        candidatos = Candidato.all()

        edicao_to_edit = None
        detalhes = []
        curso = None
        candidato_to_edit = None

        if tab == 'edicao' and params.get('id'):
            try:
                eid = int(params.get('id'))
                edicao_to_edit = Edicao.find(eid)
                detalhes = EdicaoCurso.where('edicao_id', eid).get()
            except Exception:
                pass

        if tab == 'curso' and params.get('id'):
            try:
                cid = int(params.get('id'))
                curso = Curso.find(cid)
            except Exception:
                pass

        if tab == 'candidato' and params.get('id'):
            try:
                cand_id = int(params.get('id'))
                candidato_to_edit = Candidato.find(cand_id)
            except Exception:
                pass

        modalidades = [
            "Ampla Concorrência",
            "PPI - Baixa Renda",
            "Pública - Baixa Renda",
            "PPI - Pública",
            "Pública",
            "Deficientes",
        ]

        self.render(
            "index.html",
            cursos=cursos,
            edicoes=edicoes,
            candidatos=candidatos,
            edicao_to_edit=edicao_to_edit,
            detalhes=detalhes,
            curso=curso,
            candidato_to_edit=candidato_to_edit,
            modalidades=modalidades,
            msg=msg,
            error=error,
            tab=tab,
        )
