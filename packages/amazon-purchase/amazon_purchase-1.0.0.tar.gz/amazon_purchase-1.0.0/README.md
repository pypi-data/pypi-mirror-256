# amazon_purchase
![PyPI - Version](https://img.shields.io/pypi/v/amazon_purchase) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/amazon_purchase)
![PyPI - License](https://img.shields.io/pypi/l/amazon_purchase)

### Install
```python
pip install amazon_purchase --upgrade
```

### Make A Purchase
```python
from amazon_purchase import AMAZON

amazon = AMAZON(username, password)
link = "amazon link to the item you wish to purchase"
amazon.purchase(link)
```
