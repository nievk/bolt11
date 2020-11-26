
# BOLT11 ⚡️

<img src='https://www.flaticon.com/svg/static/icons/svg/3325/3325150.svg' width="250" height="252">

[Buy me a coffee ☕︎](https://zbd.gg/nievk)

This is a [Bolt11](https://github.com/lightningnetwork/lightning-rfc/blob/master/11-payment-encoding.md) ⚡️ implementation with some changes from the [original](https://github.com/lnbits/lnbits/blob/master/lnbits/bolt11.py) made by [Fiatjaf](https://github.com/fiatjaf/bolt11) and [Eillarra](https://github.com/eillarra)

## Instalation

```sh
git clone https://github.com/nievk/bolt11 && cd bolt11 && python3 setup.py install --user
```

## Start

###### Starting the Bolt11 module.

```python
#!/usr/bin/env python3

import bolt11

invoice = 'lnbc100n1p0mkk0lpp5g8pn6um9ezqtuc6xwfrdw5h5wzem0lsg3qna42p23c2z9gdha59qdqqxq9p5hsqrzjqtqkejjy2c44jrwj08y5ygqtmn8af7vscwnflttzpsgw7tuz9r40lrdu24a9pyzkw5qqqqqqqqqqqqqqpysp5qypqxpq9qcrsszg2pvxq6rs0zqg3yyc5z5tpwxqergd3c8g7rusq9qypqsq0jncr5msemdshhhjquzjmtxa4muw3zptgquhfmfahc9ssdu5l7jnxg3j0j7m4694kc49dt9dfxyzz9qd7zpj3jm6r0tkfjujlzz5j0gpkq56cc'

print(bolt11.decode(invoice))

```

###### Run

```bash
{'payment_request': 'lnbc100n1p0mkk0lpp5g8pn6um9ezqtuc6xwfrdw5h5wzem0lsg3qna42p23c2z9gdha59qdqqxq9p5hsqrzjqtqkejjy2c44jrwj08y5ygqtmn8af7vscwnflttzpsgw7tuz9r40lrdu24a9pyzkw5qqqqqqqqqqqqqqpysp5qypqxpq9qcrsszg2pvxq6rs0zqg3yyc5z5tpwxqergd3c8g7rusq9qypqsq0jncr5msemdshhhjquzjmtxa4muw3zptgquhfmfahc9ssdu5l7jnxg3j0j7m4694kc49dt9dfxyzz9qd7zpj3jm6r0tkfjujlzz5j0gpkq56cc', 'amount': 10000, 'date': 1606113791, 'route_hints': [{'short-channel-id': '180588x13255766x11097', 'base-fee-msat': 231897545, 'pubkey': '42200bdccfd4f990c3a69fad620c10ef2f8228eaff8dbc557a5090567500000000', 'cltv': 0}], 'payment-hash': '41c33d7365c880be63467246d752f470b3b7fe088827daa82a8e1422a1b7ed0a', 'description': '', 'expiry': 1728000, 'secret': '0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20', 'payee': '023b6a88c470060962fe533763125ad0cb97efcd49de460751cc9855212aef20cc'}

```
