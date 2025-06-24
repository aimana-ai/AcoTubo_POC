from pydantic import BaseModel
from typing import List


#regressor model inputs type
class RegressorInput(BaseModel):
    limite: float
    Year: int
    day_of_year: int
    FaixaPeso: object
    ProdutoFamilia: object
    ProdutoDescricao: object
    ProdutoGrupoSOP: object
    Canal: object
    EmpresaNome: object
    ClienteCNPJCPF: object
    nuPrecoGerenciaTotal: float

