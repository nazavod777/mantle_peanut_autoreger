import asyncio
from traceback import format_exc

import curl_cffi.requests.session
from curl_cffi.requests import AsyncSession
from eth_account import Account
from eth_account.account import LocalAccount
from loguru import logger
from pyuseragents import random as random_useragent

from data import config
from utils import append_file, loader


class Reger:
    def __init__(self) -> None:
        self.account: LocalAccount = Account.create()

    async def get_authorization(self,
                                client: curl_cffi.requests.session.AsyncSession) -> tuple[int, str] | None:
        response_text: None = None

        try:
            r = await client.post(url='https://mantle.peanut.to/api/proxy/get-authorisation',
                                  json={
                                      'pubKey': config.PUBKEY,
                                      'link': 'https://mantle.peanut.to/packet?c=5000&v=v4.3&t=mantle',
                                      'recipientAddress': self.account.address,
                                      'recipientName': '',
                                      'apiKey': 'doesnt-matter'
                                  })

            response_text: str = r.text

            return r.json()['depositIdx'], r.json()['authorisation']

        except Exception as error:
            if response_text:
                logger.error(f'{self.account.address} | Unexpected Error When Get Authorization: {error}, response: {response_text}')

            else:
                logger.error(f'{self.account.address} | Unexpected Error When Get Authorization: {error}')

            return None

    async def do_claim(self,
                       client: curl_cffi.requests.session.AsyncSession,
                       deposit_idx: int,
                       authorization: str) -> bool:
        response_text: None = None

        try:
            r = await client.post(url='https://mantle.peanut.to/api/proxy/claim-v2',
                                  json={
                                      'claimParams':
                                          [
                                              deposit_idx,
                                              self.account.address,
                                              config.CLAIM_SIG,
                                              authorization
                                          ],
                                      'chainId': '5000',
                                      'version': 'v4.3',
                                      'withMFA': True,
                                      'apiKey': 'doesnt-matter'
                                  })

            response_text: str = r.text

            if not r.json():
                logger.success(f'{self.account.address} | Successfully Claimed')
                return True

            logger.error(f'{self.account.address} | Bad Claim Response: {r.text}')
            return False

        except Exception as error:
            if response_text:
                logger.error(f'{self.account.address} | Unexpected Error When Get Authorization: {error}, response: {response_text}')

            else:
                logger.error(f'{self.account.address} | Unexpected Error When Get Authorization: {error}')

            return False

    async def get_reward(self,
                         client: curl_cffi.requests.session.AsyncSession) -> tuple[float, str, float] | None:
        response_text: None = None

        for _ in range(10):
            try:
                r = await client.post(url='https://mantle.peanut.to/api/proxy/user-raffle-status',
                                      json={
                                          'pubKey': config.PUBKEY,
                                          'userAddress': self.account.address,
                                          'apiKey': 'doesnt-matter'
                                      })

                response_text: str = r.text

                if r.json().get('userResults'):
                    user_amount: float | None = r.json()['userResults']['amount']
                    token_symbol: str | None = r.json()['userResults']['tokenSymbol']
                    usd_value: str | None = r.json()['userResults']['usdValue']

                    if not user_amount:
                        user_amount: float = 0

                    else:
                        user_amount: float = float(user_amount)

                    if not usd_value:
                        usd_value: float = 0

                    else:
                        usd_value: float = float(usd_value)

                    if not token_symbol:
                        token_symbol: str = 'None'

                    return user_amount, token_symbol, usd_value

                logger.info(f'{self.account.address} | {r.text}')

                await asyncio.sleep(1)

            except Exception as error:
                if response_text:
                    logger.error(f'{self.account.address} | Unexpected Error When Get Authorization: {error}, response: {response_text}')

                else:
                    logger.error(f'{self.account.address} | Unexpected Error When Get Authorization: {error}')

        return None

    async def start_reger(self,
                          proxy: str | None = None) -> None:
        client: curl_cffi.requests.session.AsyncSession = AsyncSession(
            impersonate='chrome110',
            headers={
                'accept': '*/*',
                'accept-language': 'ru,en;q=0.9',
                'content-type': 'application/json',
                'origin': 'https://mantle.peanut.to',
                'referer': 'https://mantle.peanut.to/packet?c=5000&v=v4.3&t=mantle',
                'user-agent': random_useragent()
            },
            proxies={
                'http': proxy,
                'https': proxy
            } if proxy else None,
            verify=False
        )

        auth_data: tuple[int, str] | None = await self.get_authorization(client=client)

        if not auth_data:
            return

        logger.success(f'{self.account.address} | Successfully Authorized')

        do_claim_result: bool = await self.do_claim(client=client,
                                                    deposit_idx=auth_data[0],
                                                    authorization=auth_data[1])

        if not do_claim_result:
            return

        reward_data: tuple[float, str, float] = await self.get_reward(client=client)

        if not reward_data:
            await append_file(file_folder='result/no_rewards.txt',
                              file_text=f'{self.account.key.hex()}\n')
            return

        async with loader.lock:
            await append_file(file_folder='result/accounts.txt',
                              file_text=f'{self.account.key.hex()} | {reward_data[1]} {reward_data[0]} | {reward_data[2]}\n')

        logger.success(f'{self.account.address} | Successfully Claimed {reward_data[1]} {reward_data[0]}')


async def start_reger(proxy: str | None = None) -> None:
    while True:
        try:
            await Reger().start_reger(proxy=proxy)

        except Exception as error:
            logger.error(f'{format_exc()}')
            logger.error(f'Unexpected Error: {error}')
