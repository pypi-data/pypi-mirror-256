# dvrd_imap

Object oriented wrapper for the built-in imaplib.

Documentation is work in progress.

## Example

```
from dvrd_imap import IMAPServer, IMAPFilter, IMAPMessage

host = imap.example.server
port = 993
username = example@server.com
password = examplePass123

with IMAPServer(host=host, port=port, username=username, password=password) as imap_server:
    filters = IMAPFilter(subject='Example subject')
    messages: list[IMAPMessage] = server.fetch(filters=filters, limit=10)
```

## IMAPServer

Instantiate this object to connect to the IMAP server and use the server for further actions. It is recommended to
use `IMAPServer` as a context manager to ensure the connection is closed properly.

### Properties

| **Prop**                | **Type** | **Required** | **Description**                                                                                                                            |
|-------------------------|----------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `host`                  | str      | yes          | IMAP server host                                                                                                                           |
| `port`                  | int      | yes          | IMAP server port                                                                                                                           |
| `username`              | str      | yes          | Used to login to the IMAP server                                                                                                           |
| `password`              | str      | yes          | Used to login to the IMAP server                                                                                                           |
| `ssl`                   | bool     | no           | If True (default), uses IMAP4_SSL. If False, uses IMAP4                                                                                    |
| `read_only`             | bool     | no           | If True, operate in readonly mode.  Mails are not marked as 'seen' in readonly mode.  Defaults to False.                                   |
| `mailbox`               | str      | no           | Initial mailbox to connect to, defaults to 'INBOX'                                                                                         |
| `default_message_parts` | str      | no           | Parts of the email that are retrieved. Defaults to ('UID RFC822')                                                                          |
| `auto_connect`          | bool     | no           | If False, IMAPServer does not automatically login. For further actions, the 'connect()' function must be called to establish a connection. |

### Functions

| **Function**     | **Parameters**                                                                                                                 | **Returns**       | **Description**                                                                                                                                                                                                               |
|------------------|--------------------------------------------------------------------------------------------------------------------------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `connect`        | mailbox: str (optional)                                                                                                        | IMAPServer        | Login to the IMAPServer and connect to the specified mailbox (default 'INBOX'). Use this function only with property `auto_connect=False`.                                                                                    |
| `select_mailbox` | mailbox: str read_only: bool (optional)                                                                                        | IMAPServer        | Connect to the specified mailbox.  Use the `read_only` parameter to optionally override the class' default.                                                                                                                   |
| `fetch_uids`     | limit: int (optional) filters: str \| IMAPFilter (optional)                                                                    | list[bytes]       | Fetches UID's from the server using the specified filters. Returns up to `limit` UID's. If `filters` is None, uses filter `(ALL)`.                                                                                            |
| `fetch`          | limit: int (optional) filters: str \| IMAPFilter (optional) include_raw_message: bool (optional) message_parts: str (optional) | list[IMAPMessage] | Fetches the specified message parts (see the `default_message_parts` prop) of up to `limit` mails that match the specified filters. Use `include_raw_message=True` to include the original IMAP data in the returned objects. |
| `fetch_mail`     | uid: bytes include_raw_message: bool (optional) message_parts: str (optional)                                                  | IMAPMessage       | Fetch a specific email from the server. Raises an IMAPException if the email does not exist.                                                                                                                                  |
| `close`          | -                                                                                                                              | -                 | Closes the IMAP connection.                                                                                                                                                                                                   |