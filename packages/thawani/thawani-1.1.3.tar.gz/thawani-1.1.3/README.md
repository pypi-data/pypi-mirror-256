# Thawani Python Client


Python bindings for interacting with the thawani API

This is primarily meant for merchants who wish to perform interactions with the thawani API programatically.

## Installation

```sh
$ pip install thawani
```

## Usage

You need to setup your key and secret using the following:
You can find your API keys at <https://thawani.om//#/app/keys>.

```py
import thawani
client = thawani.Client(secret_key="<Secret_KEY>",publishable_key="<Publishable_KEY>")
```



## Supported Resources


- [Customer](documents/customer.md)

- [Payments](documents/payment.md)

- [Refunds](documents/refund.md)

- [Invoice](documents/invoice.md)









---

## Bugs? Feature requests? Pull requests?

All of those are welcome. You can [file issues][issues] or [submit pull requests][pulls] in this repository.

[issues]: https://github.com/muradlansa/thawani-python/issues
[pulls]: https://github.com/muradlansa/thawani-python/pulls
