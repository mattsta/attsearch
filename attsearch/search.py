import httpx
from loguru import logger
import pprint as pp

from typing import Any


def attsearch(addr1: str, addr2: str, zipcode: str) -> dict[str, Any]:
    """Use att service lookup API to find highest internet service available at an address."""
    addr2 = str(addr2).upper()

    addr2type = ""
    unit = ""
    if addr2:
        # addr2 is the apartment/unit line like: "APT 544"
        addr2type, unit = addr2.split()

    # API Input
    doc = {
        "lobs": ["broadband"],
        "addressLine1": addr1,
        "addressLine2": addr2,
        "mode": "fullAddress",
        "city": "",
        "state": "",
        "zip": str(zipcode),
        "unitType1": addr2type,
        "unitNumber1": unit,
        "customerType": "consumer",
        "relocation_flag": True,
    }

    headers = {
        # API fails without a user agent
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0",
        "Referer": "https://www.att.com/buy/broadband/availability.html",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
    }

    logger.info("Requesting with: {}", doc)

    r = httpx.post(
        "https://www.att.com/msapi/onlinesalesorchestration/att-wireline-sales-eapi/v1/baseoffers",
        headers=headers,
        json=doc,
        timeout=90,  # the API is slow
    )

    got = r.json()
    return got


@logger.catch
def search(addr1: str, addr2: str, zipcode: str) -> None:
    """Easy CLI interface to the ATT Internet@Address API lookup logic."""
    got = attsearch(addr1, addr2, zipcode)

    if content := got.get("content"):
        try:
            logger.info(
                "Highest service level reported: {}",
                content["serviceAvailability"]["availableServices"][
                    "maxInternetDisplayText"
                ],
            )
        except:
            logger.error(
                "Failed to find service key in result? Make sure to include 'APT XXX' if multiple units are at the same address."
            )
            logger.warning("Failed result returned:\n{}", pp.pformat(got))
    else:
        logger.error("Request failed!\n{}", pp.pformat(got))


def cmd():
    import fire

    fire.Fire(search)


if __name__ == "__main__":
    cmd()
