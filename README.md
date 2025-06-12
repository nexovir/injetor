# Injector

**Injector** is a smart parameter injection tool designed to generate and manipulate query strings in URLs for testing or automation purposes.

---

## Features

- Supports different modes of query parameter generation.
- Appends or replaces parameter values intelligently.
- Handles large wordlists with chunked processing.
- Supports root path-only injection.

---

## Installation

```bash
git clone https://github.com/nexovir/Injector.git
cd Injector
python3 injector.py -h
```

---

## Usage Example

### Basic Usage

```bash
python3 injector.py -l urls.txt -w wordlist.txt -p nexovir -gm all
```

### Example Input

**URL:**

```
https://example.com/path1/path2/?query_param1=value1&query_param2=value2
```

**Mode: `-gm all`**

Will generate:

```
https://example.com/path1/path2/?query_param1=value1nexovir&query_param2=value2
https://example.com/path1/path2/?query_param1=value1&query_param2=value2nexovir
https://example.com/path1/path2/?param1=nexovir&param2=nexovir
https://example.com/path1/path2/?query_param1=value1&query_param2=value2&param1=nexovir&param2=nexovir
```

---

## Modes

- `--generatemode all`: Combines all techniques (`combine`, `root`, `ignore`).
- `--generatemode combine`: Only injects into existing parameters.
- `--generatemode root`: Appends new parameters to root path.
- `--generatemode ignore`: Ignores existing queries and appends new ones.

- `--valuemode append`: Adds payload to end of existing value.
- `--valuemode replace`: Replaces the original value.

---

## Example Wordlist

```
param1
param2
```

With `-p nexovir` and chunk = 2, generates:

```
?param1=nexovir&param2=nexovir
```

---

## Output

Use `-o output.txt` to save results.

---

## Silent Mode

Use `-s` to suppress terminal output.
