<h1 align="center">
  <br>
  <a href="http://www.github.com/vulzap/vulzap"><img src="https://avatars.githubusercontent.com/u/148681518?s=200&v=4" alt="vulzap" width="200"></a>
  <br>
  vulzap
  <br>
</h1>

<h4 align="center">Web-based 0/1-Day Semi-Automation Analysis Tool</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#build">Build</a> •
  <a href="#license">License</a>
</p>

## Key Features

## Installation

### Manual

```sh
$ python3 setup.py install
```

```sh
$ pip3 install vulzap
```

## How To Use

### Set environments

| Key       | Value (default)         |
| --------- | ----------------------- |
| DB_HOST   | MySQL Host (localhost)  |
| DB_PORT   | MySQL Port (3306)       |
| DB_USER   | MySQL User (root)       |
| DB_PASSWD | MySQL Password ()       |
| DB_NAME   | MySQL DataBase (vulzap) |

**Default**

```yaml
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWD=
DB_NAME=vulzap
```

Under `~/.vzrc` (MacOS), `%UserProfile\.vzrc` (Windows)

You can set environment values with this command:

```php
$ vz setenv <key> <value>
```

Also can print environment values with this command:

```php
$ vz printenv
```

### Crawl

```powershell
$ python vulzap\main.py crawl -u http://localhost:9001 -H "{'Cookie': 'test'}"
```

### Exploit

vulzap supports: XSS(Cross Site Script), SQL Injection

**XSS**

```powershell
$ python vulzap\main.py exploit --mode xss -u http://13.209.98.240/DVWA/vulnerabilities/xss_r/?name=name -m GET
```

```sh
$ python vulzap/main.py exploit --mode xss -u http://13.209.98.240/DVWA/vulnerabilities/xss_r/?name=name -m GET
```

**SQL Injection**

```powershell
$ python vulzap\main.py exploit --mode sqli -d "{'http://testphp.vulnweb.com/listproducts.php': {'GET': ['cat'], 'POST': []}, 'http://example.com/': {'GET': ['search', 'def'], 'POST': []}}"
```

```sh
$ python vulzap/main.py exploit --mode sqli -d "{'http://testphp.vulnweb.com/listproducts.php': {'GET': ['cat'], 'POST': []}, 'http://example.com/': {'GET': ['search', 'def'], 'POST': []}}"
```

### show

```powershell
$ python vulzap\main.py show
```

### proxy

```powershell
$ python vulzap\main.py proxy --host localhost --port 8080
```

### Build

```sh
# test build
$ python setup.py develop

$ python setup.py install
```

### Release

```sh
$ python setup.py sdist bdist_wheel

$ python -m twine upload dist/*
```

## License

MIT
