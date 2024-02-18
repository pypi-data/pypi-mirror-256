import requests
from requests import Session

from .adapters import HTTPAdapterWithProxyKerberosAuth


def get_session(proxies=None) -> type(Session):
    session: Session = requests.Session()
    if proxies:
        session.proxies = proxies

        # kerberos authentication
        http_adapter_with_proxy_kerberos_auth = HTTPAdapterWithProxyKerberosAuth()
        session.mount('https://', http_adapter_with_proxy_kerberos_auth)
    return session