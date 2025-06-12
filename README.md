## Version

**v1.0.0**

# Injector

**Injector** is a smart and flexible parameter injection tool designed to automate and test query string manipulation in URLs. It supports multiple generation modes and is ideal for reconnaissance or debugging during web application testing.

## 🛠 Installation

Clone the repository and install it using `pip`:

```bash
git clone https://github.com/nexovir/Injector.git
cd Injector
pip install .
```

Once installed, use `injector` directly from the terminal:

```bash
injector -l urls.txt -w params.txt -gm all
```

## 🔥 Example

Given a URL like:

```
https://example.com/path1/path2/?query_param1=value1&query_param2=value2
```

Running with `-gm all -vm append -p nexovir -w wordlist.txt` may generate:

```
https://example.com/path1/path2/?query_param1=value1nexovir&query_param2=value2
https://example.com/path1/path2/?query_param1=value1&query_param2=value2nexovir
https://example.com/path1/path2/?param1=nexovir&param2=nexovir
https://example.com/path1/path2/?query_param1=value1&query_param2=value2&param1=nexovir&param2=nexovir
```

These represent:

- `combine` mode with `append`: injects into existing query param values.
- `root` mode: creates new parameters on base URL.
- `ignore` mode: adds parameters without considering existing query string.
- `all`: includes all of the above combined.

## 💡 Usage

```bash
injector -l <urls.txt> [-w <params.txt>] [-p <parameter>] [-vm append|replace] [-gm root|ignore|combine|all] [-c 25] [-s] [-o <output.txt>]
```


## Output

Use `-o output.txt` to save results.

---

## Silent Mode

Use `-s` to suppress terminal output.
