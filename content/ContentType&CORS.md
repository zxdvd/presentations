
class: center, middle
# ContentType and CORS

---

# Agenda

1. ContentType
2. CORS

---

# ContentType: Why we need to care about it?

1. ajax(jquery) help us wrap the details while fetch does not
2. we need to know what we sent and received
3. better cooperation between frontend and backend

---

# ContentType: frequent used types

1. text/plain
2. application/json
3. application/x-www-form-urlencoded

---

# ContentType: ajax under the hood

1. ajax settings

```
url: location.href,
		type: "GET",
		isLocal: rlocalProtocol.test( location.protocol ),
		global: true,
		processData: true,
		async: true,
		contentType: "application/x-www-form-urlencoded; charset=UTF-8",
```

2. data manipulation

```
// Convert data if not already a string
if ( s.data && s.processData && typeof s.data !== "string" ) {
  s.data = jQuery.param( s.data, s.traditional );
}
```

```
// Serialize an array of form elements or a set of
// key/values into a query string
jQuery.param = function( a, traditional ) {
  ...
  // Return the resulting serialization
	return s.join( "&" );
```

---

# Server side parser - flask

---

# Servr side parse - body-parse (express & koa)

---

class: center, middle
# CORS

---

# Simple request

---

# Non-simple request

---

# Deal with OPTION request

---

# Deal with cross site origin header

1. nginx
2. backend server

---

# References:

1. [rfc1341 ContentType](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html)
2. [rfc-2616 http headers](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)
3. [mozilla MDN cors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS)
