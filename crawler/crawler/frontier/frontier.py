
#
# 1. need url filter and queue
# 2. manage url access period of agent
# 3. support dynamic configuration
# 4. avoid infinite loop of url access
#


def _filter_robots(url: str) -> list:
    """check robots.txt

    :param url:
    :return accessible_urls:
    """
    accessible_urls = []
    return accessible_urls


accessible_urls = _filter_robots("url")  # frontier 로 이동
