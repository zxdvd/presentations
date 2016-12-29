
class: center, middle
# Blue Green Deployment

---

# Agenda

1. Why
2. How
    - haproxy
    - nginx
3. QA

---

# Why?

1. avoid bad build
2. decrease downtime
3. AB testing / feature testing
4. help debugging problems

---

# How: haproxy

1. maybe the best open source load balancer
2. layer4 and layer7 load lalancer (ssh, smtp, mysql, mongo, http)

---

# How: haproxy

```
frontend in
      bind *:20000
      acl testing_url path_beg /abtesting
      use_backend backend-blue if { req.cook(ABTESTING) -m beg blue }
      use_backend backend-blue if testing_url
        default_backend backend-green

backend backend-green
      server server1 localhost:20001  maxconn 100

backend backend-blue
      cookie ABTESTING insert indirect nocache maxlife 48h
      server server1 localhost:20002  cookie blue= maxconn 100
```

---

# How: haproxy

```
frontend www-in
        bind *:20000
        default_backend www-out

backend www-out
        cookie ABTESTING insert indirect nocache maxlife 48h
        use-server www-server2 if { path_beg /abtesting }
        # use-server www-server2 if { req.cook(ABTESTING) -m reg ^www.* }
        # acl abtesting_found req.cook(abtesting) -m found
        # use-server www-server1 if !abtesting_found
        server www-server1 localhost:20001  cookie www-server1 maxconn 100
        server www-server2 localhost:20002  cookie www-server2 maxconn 100 backup
```


---

# Haproxy

```
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
acl host_www    hdr_beg(host) -i www
acl host_static hdr_beg(host) -i img. video. download. ftp.

use_backend static if host_static or host_www url_static
use_backend www    if host_www
```

---

# How: nginx

```
upstream green {
  server localhost:20001;
}

upstream blue {
  server localhost:20002;
}

map $cookie_abtesting $backend {
  default green;
  green green;
  blue blue;
}

server {
  listen 80;
  location / {
    proxy_pass http://$backend;
  }

  location /testing {
    add_header Set-Cookie abtesting=blue always;
    proxy_pass http://$backend;
  }
}
```

---

# How: nginx

nginx sticky (work like haproxy cookie persistence)
```
upstream backend {
  server localhost:20001;
  server localhost:20002;
  sticky cookie server_id expires=48h;
}

```
---

# References:

1. [haproxy doc](http://www.haproxy.org/download/1.6/doc/configuration.txt)
2. [haproxy a/b testing](http://blog.rudylee.com/2016/04/13/haproxy-and-a-slash-b-testing/)
3. [nginx a/b testing](http://qzaidi.github.io/2012/03/11/nginx-ab/)
4. [nginx sticky](http://nginx.org/en/docs/http/ngx_http_upstream_module.html?&_ga=1.189051176.2090890265.1437394769#sticky_cookie)
