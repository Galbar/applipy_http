# Logging

There's two loggers that can be configured for a given http server. You can
find bellow an example with the default values:

```
http.servers:
- name: demo
  host: 0.0.0.0
  port: 8080
  logging:
    access:
      level: WARNING
      format: '%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
    server:
      level: WARNING
```

The `access.format` field must follow the format specified
[here](https://docs.aiohttp.org/en/stable/logging.html#access-logs)
