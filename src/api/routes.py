import logging
import src.queries as queries
from pydantic  import BaseModel
from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from src.db import insert_data
from src.process import process_csv
from typing import Optional

class Venda(BaseModel):
    id: int
    cliente: str
    produto: str
    valor: float
    data: str

router = APIRouter(prefix="/vendas")

@router.post("/") # POST para inserir uma nova venda
def criar_venda(venda: Venda):

    try:
        result =  queries.insert_data([venda.model_dump()])
        return result
    
    except Exception as e:
        logging.error(f"Erro ao criar venda: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar venda")
    

# @router.get("/") # GET sem filtros, para listar todas as vendas
# def listar_vendas():
    
#     try:
#         return queries.fetch_all()
    
#     except Exception as e:
#         logging.error(f"Erro ao listar vendas: {e}") 
#         raise HTTPException(status_code=500, detail="Erro interno ao buscar vendas")
    
@router.get("") # GET com filtros opcionais
def listar_vendas(
    cliente: Optional[str] = Query(None, description="Filtrar por nome do cliente"),
    valor_min: Optional[float] = Query(None, description="Valor mínimo da venda"),
    valor_max: Optional[float] = Query(None, description="Valor máximo da venda"),
    data: Optional[str] = Query(None, description="Data da venda no formato YYYY-MM-DD"),
    limit: Optional[int] = Query(None, description="Limite de resultados"),
    offset: Optional[int] = Query(None, description="Deslocamento para paginação")
):

    try:
        return {
            "limit": limit,
            "offset": offset,
            "data":queries.fetch_by(
            limit=limit,
            offset=offset,
            cliente=cliente,
            valor_min=valor_min,
            valor_max=valor_max,
            data=data
            )
        }
    except Exception as e:
        logging.error(f"Erro ao listar vendas com filtros: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar vendas com filtros")

@router.get("/{id}") # GET para buscar venda por ID
def buscar_venda(id: int):

    try:
        venda = queries.fetch_by_id(id)

        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        return venda
    
    except HTTPException:
        raise

    except Exception:
        logging.exception(f"Erro ao buscar venda por ID")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar venda por ID")
    
@router.delete("/{id}") # DELETE para remover venda por ID
def deletar_venda(id: int):

    try:
        venda = queries.fetch_by_id(id)

        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        queries.delete_by_id(id)
        return {"message": f"Venda com ID {id} deletada com sucesso"}
    
    except Exception as e:
        logging.error(f"Erro ao deletar venda: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao deletar venda")

@router.get("/relatorios/") # GET para gerar relatório completo de vendas
def relatorio_faturamento():

    try:
        return queries.fetch_report()
    
    except Exception as e:
        logging.error(f"Erro ao gerar relatório de faturamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar relatório de faturamento")
    
@router.post("/upload")
def upload_vendas(file: UploadFile = File(...)):
    
    try:
        content = file.file.read().decode('utf-8')

        data = process_csv(content)

        data_counts = insert_data(data)
        
        return data_counts
    
    except Exception as e:
        logging.exception(f"Erro ao processar arquivo CSV: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar arquivo CSV")