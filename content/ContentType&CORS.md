
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
4. multipart/form-data

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

# ContentType: x-www-form-urlencoded

1. default ContentType of form submission
2. space will be replaced by "+"
3. non-printable ascii charaters will be converted to "%HH"
4. then, will waste too much when transferring binary file

---

# ContentType: form-data

```
Content-Type: multipart/form-data; boundary=AaB03x

--AaB03x
Content-Disposition: form-data; name="submit-name"

Larry
--AaB03x
Content-Disposition: form-data; name="files"; filename="file1.txt"
Content-Type: text/plain

... contents of file1.txt ...
--AaB03x--
```

---

# Server side parser - tornado

```
if content_type.startswith("application/x-www-form-urlencoded"):
		try:
				uri_arguments = parse_qs_bytes(native_str(body), keep_blank_values=True)
		except Exception as e:
				gen_log.warning('Invalid x-www-form-urlencoded body: %s', e)
				uri_arguments = {}
		for name, values in uri_arguments.items():
				if values:
						arguments.setdefault(name, []).extend(values)
elif content_type.startswith("multipart/form-data"):
		try:
				fields = content_type.split(";")
				for field in fields:
						k, sep, v = field.strip().partition("=")
						if k == "boundary" and v:
								parse_multipart_form_data(utf8(v), body, arguments, files)
								break
				else:
						raise ValueError("multipart boundary not found")
		except Exception as e:
				gen_log.warning("Invalid multipart/form-data: %s", e)
```

---

# Servr side parse - body-parse (express & koa)

```
  function* parseBody(ctx) {
    if (enableJson && ((detectJSON && detectJSON(ctx)) || ctx.request.is(jsonTypes))) {
      return yield parse.json(ctx, jsonOpts);
    }
    if (enableForm && ctx.request.is(formTypes)) {
      return yield parse.form(ctx, formOpts);
    }
    if (enableText && ctx.request.is(textTypes)) {
      return yield parse.text(ctx, textOpts) || '';
    }
    return {};
  }
```
---

class: center, middle
# CORS

---

# Simple request

1. GET HEAD POST
2. headers: Accept, Accept-Language, Content-Language, Content-Type
3. Content-Type: two kinds of form data and text/plain
---

# Non-simple request

1. will send preflighted request (OPTIONS)
2. header "Access-Control-Max-Age": cached preflighted response

```
if (this.method === 'OPTIONS') {
	this.status = 204
	return
}
```
---

# Deal with cross site origin header

1. `this.set('Access-Control-Allow-Origin', '*')`
2. nginx
3. backend server

NEVER set this header twice.

---

# References:

1. [rfc1341 ContentType](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html)
2. [rfc-2616 http headers](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)
3. [html form](https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4)
4. [mozilla MDN cors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS)
5. [fetch spec](https://fetch.spec.whatwg.org/#cors-preflight-fetch)
6. [my jsfiddle](http://jsfiddle.net/zxdvd/4uy9fhyt/6/)
