from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from service.db_watchers import GameDb
from service.config import logger
from service.db_setup.db_settings import get_session
from service.schemas import (
    QuestionGetOneRequest,
    QuestionResponse,
    TgPlayerIdRequest,
)
from service.utils import QuestionsManager

api_router = APIRouter(
    prefix="/v1",
    tags=["game"],
)


@api_router.post(
    "/round-question",
    response_model=QuestionResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def get_round_question(
    data: QuestionGetOneRequest, session: AsyncSession = Depends(get_session)
) -> QuestionResponse:
    """Get_question next in round for this user"""
    q_manager = QuestionsManager(session)
    db_game = GameDb(session)
    try:
        await db_game.create_new_rounds(data.tg_id)
    except IntegrityError as err:
        text_err = "error. maybe tg_id is wrong"
        logger.error(text_err)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            text_err,
        ) from err
    question_id = data.question_id or await db_game.get_next_question_id(
        data.tg_id
    )
    question = await q_manager.get_question_by_id(question_id)
    if question is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    return question


@api_router.put(
    "/edit-score",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def edit_player_score(
    params=Depends(TgPlayerIdRequest),
    session: AsyncSession = Depends(get_session),
):
    """Request for edit_score"""
    db_game = GameDb(session)
    await db_game.raise_score(params.tg_id)
    return {"success": "1"}
