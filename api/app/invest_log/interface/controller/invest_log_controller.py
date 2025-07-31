from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.invest_log.application.invest_log_service import InvestLogService
from app.invest_log.domain.invest_log import CreateInvestLogBody, DeleteInvestLogBody, UpdateInvestLogBody, InvestLog
from app.utils.id_utils import verify_access_token, verify_refresh_token

router = APIRouter(prefix="/invest_log", tags=["invest_log"])

@router.get("/", status_code=200, response_model=list[InvestLog])
@inject
def get_user_asset(
    access_token:str=Query(None),
    refresh_token:str=Query(None),
    invest_log_service: InvestLogService = Depends(Provide[Container.invest_log_service]),
):
    user = None
    user = verify_access_token(access_token)
    if(user is None):
        user = verify_refresh_token(refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    invest_log = invest_log_service.search_by_user_id(user.id)
    return invest_log

@router.post("/", status_code=201)
@inject
def create_invest_log(
    create_invest_log_body: CreateInvestLogBody,
    invest_log_service: InvestLogService = Depends(Provide[Container.invest_log_service]),
):
    user = None

    user = verify_access_token(create_invest_log_body.access_token)
    if(user is None):
        user = verify_refresh_token(create_invest_log_body.refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    invest_log_service.create(user.id, create_invest_log_body.date, create_invest_log_body.stock_code, create_invest_log_body.stock_name, create_invest_log_body.action, create_invest_log_body.amount, create_invest_log_body.reason, create_invest_log_body.amount_ratio, create_invest_log_body.profit, create_invest_log_body.profit_ratio, create_invest_log_body.price)
    return {"status": "success"}

@router.put("/", status_code=201)
@inject
def update_user_asset(
    update_invest_log_body: UpdateInvestLogBody,
    invest_log_service: InvestLogService = Depends(Provide[Container.invest_log_service]),
):
    user = None

    user = verify_access_token(update_invest_log_body.access_token)
    if(user is None):
        user = verify_refresh_token(update_invest_log_body.refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    invest_log_service.update(update_invest_log_body.invest_log)
    return {"status": "success"}

@router.delete("/", status_code=201)
@inject
def delete_invest_log(
    delete_invest_log_body: DeleteInvestLogBody,
    invest_log_service: InvestLogService = Depends(Provide[Container.invest_log_service]),
):
    user = None

    user = verify_access_token(delete_invest_log_body.access_token)
    if(user is None):
        user = verify_refresh_token(delete_invest_log_body.refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    invest_log_service.delete(delete_invest_log_body.invest_log_id)
    return {"status": "success"}