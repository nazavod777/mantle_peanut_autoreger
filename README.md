[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/n4z4v0d)](https://t.me/n4z4v0d)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/better-automation.svg)](https://www.python.org/downloads/release/python-3116/)
[![works badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.2.0/badge.svg)](https://github.com/nikku/works-on-my-machine)  

### data/proxies.txt  
_Все Proxy с новой строки (не забывайте указывать тип, ex: http://user:pass:ip:port)  
Сколько прокси столько и потоков (юзайте роташки от Travchis, в посте ссылка)_

### data/config.py  
_**PUBKEY** - ищем запрос на URL **https://mantle.peanut.to/api/proxy/get-authorisation**, в **payload** есть значение **pubKey** - копируем и вставляем в **config.py**_
![alt text](https://i.imgur.com/MvKMttF.png)  
_**CLAIM_SIG** - ищем запрос на URL **https://mantle.peanut.to/api/proxy/claim-v2**, в **payload** ищем значение **claimParams**, в нем будет предпоследняя длинная строка с сигнатурой - копируем и вставляем в **config.py**_
![alt text](https://i.imgur.com/MvKMttF.png)  

# DONATE (_any evm_) - 0xDEADf12DE9A24b47Da0a43E1bA70B8972F5296F2
# DONATE (_sol_) - 2Fw2wh1pN77ELg6sWnn5cZrTDCK5ibfnKymTuCXL8sPX
# DONATE (_trx_) - TEAmkvFXJ6N6wzN4aS3HtgiM7XhnwRrtkW
