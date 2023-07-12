# HTTP 1.1 101 Switching

Background Research and References:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/101
* https://christian-schneider.net/CrossSiteWebSocketHijacking.html
* https://www.rfc-editor.org/rfc/rfc2616#section-14.42

## IAM Policy

The pseudo-policy - [cazt_scen4_implicit-deny.json](../../../trainee/iam_policies/cazt_scen4_implicit-deny.json) should be used for testing. Your goal is to get around the deny authorization via abuse of the switching protocol.

## Exercise

1. Document the result of calling each API endpoint including why you received the response you did.
1. Explain what the IAM policy stated in comparison with the result you received.
   * Why was the API endpoint vulnerable or not vulnerable?

You will need to use Burp Suite (or another HTTP MitM proxy) for this exercise. **Ensure that you set the mode to HTTP/1.1** and not HTTP/2 for the requests.

Some malicious HTTP headers to try:
```
Connection: Upgrade
Upgrade: http/2


Upgrade: h2c
HTTP2-Settings: YEL8U6YI2gRiwXAGTdmnUeMs
Connection: Upgrade, HTTP2-Settings


Connection: Upgrade
Upgrade: WebSocket, foo/2, h2c, h2, http/2
Sec-WebSocket-Key: Y29hbGZpcmU=
```

## API Endpoints (in-scope for testing)

* Create Moggy
* List Moggies
* Get Moggy
* Delete Moggy
* Run Moggy Activity
* Pet Sitter


## Next

Proceed to [scenario ten - HTTP Smuggling](10-http_smuggling.md)
