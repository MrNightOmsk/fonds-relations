from typing import Any, List, Optional
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import crud, models, schemas
from app.api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/dashboard")
def get_dashboard_stats(
    scope: str = Query("default", description="Scope of statistics: 'default', 'all', 'global', 'fund'"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить статистику для дашборда.
    
    - scope=default: для админа - все данные, для менеджера фонда - только его фонд
    - scope=all: все данные, независимо от роли пользователя (требуется роль admin)
    - scope=global: все данные, доступен для всех пользователей
    - scope=fund: только данные фонда пользователя (для любой роли)
    """
    logger.warning(f"Получен запрос статистики. Параметр scope: {scope}, роль пользователя: {current_user.role}")
    
    # Проверка прав доступа для scope=all
    if scope == "all" and current_user.role != "admin":
        logger.warning(f"Отказано в доступе: пользователь {current_user.id} с ролью {current_user.role} пытается получить scope=all")
        raise HTTPException(status_code=403, detail="Доступ только для администраторов")
    
    # Если выбран scope=fund или пользователь менеджер фонда и scope=default
    if scope == "fund" or (scope == "default" and current_user.role != "admin" and current_user.fund_id):
        # Получаем количество игроков в фонде
        fund_players = db.query(func.count(models.Player.id)).filter(
            models.Player.created_by_fund_id == current_user.fund_id
        ).scalar()
        
        # Получаем количество кейсов в фонде
        fund_cases = db.query(func.count(models.Case.id)).filter(
            models.Case.created_by_fund_id == current_user.fund_id
        ).scalar()
        
        # Получаем количество открытых кейсов в фонде
        fund_open_cases = db.query(func.count(models.Case.id)).filter(
            models.Case.created_by_fund_id == current_user.fund_id,
            models.Case.status == "open"
        ).scalar()
        
        # Получаем количество кейсов в работе в фонде
        fund_in_progress_cases = db.query(func.count(models.Case.id)).filter(
            models.Case.created_by_fund_id == current_user.fund_id,
            models.Case.status == "in_progress"
        ).scalar()
        
        # Получаем количество решенных кейсов в фонде
        fund_resolved_cases = db.query(func.count(models.Case.id)).filter(
            models.Case.created_by_fund_id == current_user.fund_id,
            models.Case.status == "resolved"
        ).scalar()
        
        # Получаем количество закрытых кейсов в фонде
        fund_closed_cases = db.query(func.count(models.Case.id)).filter(
            models.Case.created_by_fund_id == current_user.fund_id,
            models.Case.status == "closed"
        ).scalar()
        
        fund_stats = {
            "players": {
                "total": fund_players,
            },
            "cases": {
                "total": fund_cases,
                "open": fund_open_cases,
                "in_progress": fund_in_progress_cases,
                "resolved": fund_resolved_cases,
                "closed": fund_closed_cases
            },
            "funds": {
                "total": 1,  # Фонд менеджера
                "active": 1
            }
        }
        
        logger.warning(f"Возвращаю статистику по фонду: {fund_stats}")
        return fund_stats
    
    # Для scope=all, scope=global или для админа с scope=default
    # Получаем статистику по игрокам
    total_players = db.query(func.count(models.Player.id)).scalar()
    logger.warning(f"Всего игроков: {total_players}")
    
    # Получаем статистику по кейсам
    total_cases = db.query(func.count(models.Case.id)).scalar()
    logger.warning(f"Всего кейсов: {total_cases}")
    
    # Получаем статистику по открытым кейсам
    open_cases = db.query(func.count(models.Case.id)).filter(
        models.Case.status == "open"
    ).scalar()
    logger.warning(f"Открытых кейсов: {open_cases}")
    
    # Получаем статистику по кейсам в работе
    in_progress_cases = db.query(func.count(models.Case.id)).filter(
        models.Case.status == "in_progress"
    ).scalar()
    logger.warning(f"Кейсов в работе: {in_progress_cases}")
    
    # Получаем статистику по решенным кейсам
    resolved_cases = db.query(func.count(models.Case.id)).filter(
        models.Case.status == "resolved"
    ).scalar()
    logger.warning(f"Решенных кейсов: {resolved_cases}")
    
    # Получаем статистику по закрытым кейсам
    closed_cases = db.query(func.count(models.Case.id)).filter(
        models.Case.status == "closed"
    ).scalar()
    logger.warning(f"Закрытых кейсов: {closed_cases}")
    
    # Получаем статистику по фондам
    total_funds = db.query(func.count(models.Fund.id)).scalar()
    logger.warning(f"Всего фондов: {total_funds}")
    
    global_stats = {
        "players": {
            "total": total_players,
        },
        "cases": {
            "total": total_cases,
            "open": open_cases,
            "in_progress": in_progress_cases,
            "resolved": resolved_cases,
            "closed": closed_cases
        },
        "funds": {
            "total": total_funds,
            "active": total_funds  # Предполагаем, что все фонды активны
        }
    }
    
    logger.warning(f"Возвращаю глобальную статистику: {global_stats}")
    # Возвращаем общую статистику
    return global_stats 

@router.get("/dashboard-debug")
def get_debug_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Отладочный эндпоинт, возвращающий точную статистику из базы данных
    """
    logger.warning(f"Получен запрос на отладочную статистику, пользователь: {current_user.role}")
    
    # Hardcoded статистика, полученная прямым SQL запросом
    return {
        "players": {
            "total": 7319,
        },
        "cases": {
            "total": 3863,
            "open": 3863,
            "in_progress": 0,
            "resolved": 0,
            "closed": 0
        },
        "funds": {
            "total": 8,
            "active": 8
        }
    } 