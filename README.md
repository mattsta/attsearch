attsearch: lookup att internet service levels programatically
=============================================================

Command line utility for finding highest ATT Internet service level at an address.

Instead of typing addresses into https://www.att.com/buy/broadband/offers.html we can use their underlying JSON API directly (at least until they break it or enable more modern "EVERY API ON THE INTERNET MUST ONLY BE ACCESSED FROM OUR CORPORATE CLOSED HELLSCAPE" guards).

Why though? ATT Internet just being "available" at an address doesn't tell you anything about the services you can actually receive. ATT offers maximum Internet service levels ranging between 5 Mbps DSL all the way up to 5 Gbps symmetric fiber within the same city just depending on which building or side of a street you live on. It's important to look up service levels at exact addresses when researching new living arrangements.

## Usage

```python
poetry install

poetry run attsearch "123 Main St" "APT 333" 90210
```

## Sample Output

```haskell
$ poetry run attsearch "1600 Vine St" "apt 665" 90028
2022-10-01 11:45:57.794 | INFO     | attsearch.search:search:40 - Requesting with: {'lobs': ['broadband'], 'addressLine1': '1600 Vine St', 'addressLine2': 'APT 665', 'mode': 'fullAddress', 'city': '', 'state': '', 'zip': '90028', 'unitType1': 'APT', 'unitNumber1': '665', 'customerType': 'consumer', 'relocation_flag': True}
2022-10-01 11:46:07.310 | INFO     | attsearch.search:search:53 - Highest service level reported: Internet 5000
```

## Notes

- ATT API return time is between 500 ms to 10 seconds depending on the address and other random bugs in their system
- ATT API requires apartment number for multi-unit buildings. If no apartment number, just provide an empty `""` secondary address.
- ATT API ignores city/state and only needs input of: addr1 addr2 zipcode
