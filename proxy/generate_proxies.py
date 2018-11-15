"""Find working HTTP(S) proxies and save them to a file."""

import asyncio
from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        count = 0
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            if proto:
                print('Generating proxies to use...{} - proto {}'.format(proxy.host, proto))
                count += 1
                print(count)
                #row = '%s://%s\n' % (proto, proxy.host)
                row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)


def gen_proxies():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=500),
                           save(proxies, filename='proxy/proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()