import asyncio
import logging

import pytest
import pytest_asyncio

pytest_plugins = ("pytest_asyncio",)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio


async def test_show_quiz_handler(client):
    url = "/v1/show-quiz"
    input_data = {
        "active": 1,
        "limit": 50,
        "offset": 0,
        "order": "updated_dt",
        "text": "question",
    }
    response = client.post(url, json=input_data)
    assert response.status_code == 200


async def test_get_questions_handler(client):
    url = "/v1/questions"
    input_data = {
        "active": 1,
        "limit": 50,
        "offset": 0,
        "order": "updated_dt",
        "text": "question",
    }
    response = client.post(url, json=input_data)
    assert response.status_code == 200


def add_question(client, url="/v1/add-question"):
    input_data = {
        "text": "question1",
        "active": 1,
    }
    response = client.post(url, json=input_data)
    assert response.status_code == 201
    id_ = response.json()["created"]
    return id_


def add_answer(client, q_id, url="/v1/add-answer"):
    input_data = {"text": "answer", "correct": True, "question_id": q_id}
    response = client.post(url, json=input_data)
    assert response.status_code == 201
    id_ = response.json()["created"]
    return id_


async def test_add_question_handler(client):
    q_id = add_question(client, "/v1/add-question")
    assert q_id


async def test_edit_question_handler(client):
    url = "/v1/edit-question"
    query = "?id=1&active=1"
    response = client.put(url + query)
    assert response.status_code == 200


async def test_delete_question_handler(client):
    url = "/v1/delete-question?id=1"
    response = client.delete(url)
    assert response.status_code == 200


async def test_add_answer_handler(client):
    q_id = add_question(client, "/v1/add-question")
    assert q_id
    id_ = add_answer(client, q_id, "/v1/add-answer")
    assert id_


async def test_submit_answer_handler(client):
    q_id = add_question(client, "/v1/add-question")
    assert q_id
    id_ = add_answer(client, q_id, "/v1/add-answer")
    assert id_

    url = "/v1/submit-answer?question_id=" + str(q_id)
    response = client.post(url, json=[id_])
    assert response.status_code == 200
    assert "correct" in response.json()


async def test_delete_answer_handler(client):
    url = "/v1/delete-answer?id=1"
    response = client.delete(url)
    assert response.status_code == 200
