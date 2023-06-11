import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
import requests

from constants import API_HOST, API_PORT
from logger import info_logger, warning_logger



async def get_users():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'{API_HOST}:{API_PORT}/users/'
            ) as response:
                return await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def create_user(user: dict):
    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            async with session.post(
                f'{API_HOST}:{API_PORT}/users/',
                json=user,
                ssl=False
            ) as response:
                await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def exists_user(user_id: dict) -> dict:
    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            async with session.get(
                f'{API_HOST}:{API_PORT}/users/{user_id}/exists/',
            ) as response:
                return await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def get_payments(user_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'{API_HOST}:{API_PORT}/users/{user_id}/payments/'
            ) as response:
                return await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def create_payments(user_id: int, payment: dict):
    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            async with session.post(
                f'{API_HOST}:{API_PORT}/users/{user_id}/payments/',
                json=payment,
                ssl=False
            ) as response:
                await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def update_ballance(user_id: int, ballance: dict):
    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            async with session.patch(
                f'{API_HOST}:{API_PORT}/users/{user_id}/ballance/',
                json=ballance,
                ssl=False
            ) as response:
                await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def get_blacklist():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'{API_HOST}:{API_PORT}/blacklist/'
            ) as response:
                return await response.json()
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


async def create_blacklist_object(user_id: int):
    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            async with session.post(
                f'{API_HOST}:{API_PORT}/users/{user_id}/blacklist/',
                ssl=False
            ) as response:
                result = response
                return result.status
        except ClientConnectorError:
            warning_logger.error('ClientConnectorError')


def get_blacklist_sync():
    response = requests.get(f'{API_HOST}:{API_PORT}/blacklist/')
    print(response.json())
    return response.json()

