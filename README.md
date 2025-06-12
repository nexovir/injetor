# Injector

**Injector** is a smart parameter injection tool designed to inject specified parameters into URLs by appending or replacing query parameters. It supports batch processing, multiple injection modes, and flexible configuration options.

---

## Features

- Inject parameters into URLs using a wordlist or single parameter  
- Supports modes to append or replace parameter values  
- Multiple generation modes: root, ignore, combine, all  
- Batch processing with chunk size control  
- Silent mode to suppress terminal output  
- Save results to output file  

---

## Installation

```bash
git clone <your-repo-url>
cd injector
pip install -r requirements.txt
```

---

## Usage

```bash
python injector.py -l urls.txt -w params.txt -p nexovir -vm append -gm all -c 25 -o output.txt
```

---

## Examples

### Example for `-gm all` and `-vm append`

Suppose you have the following:

- URL: `https://example.com`
- Wordlist parameters: `param1, param2, param3`
- Parameter value to inject: `nexovir`

Running:

```bash
python injector.py -l urls.txt -w wordlist.txt -p nexovir -vm append -gm all
```

Where:

- `urls.txt` contains:  
  ```
  https://example.com
  ```
- `wordlist.txt` contains:  
  ```
  param1
  param2
  param3
  ```

---

**What happens?**

- The tool will generate URLs by appending each parameter with the value `nexovir`.
- Since `-gm all` includes all modes (`combine`, `root`, `ignore`), the tool will:
  - Append parameters to the root URL (without existing queries).
  - Append parameters even if the URL has queries (not in this case).
  - Append parameters ignoring existing query parameters.

---

**Generated URLs:**

1. **Root mode:**  
```
https://example.com?param1=nexovir&param2=nexovir&param3=nexovir
```

2. **Ignore mode:**  
```
https://example.com?param1=nexovir&param2=nexovir&param3=nexovir
```

3. **Combine mode:** (no existing queries here, so no output)

---

## Notes

- Use the `-s` or `--silent` flag to suppress output to the terminal.  
- Use the `-o` or `--output` option to save generated URLs to a file.  
- Adjust chunk size (`-c`) to control batch processing size.

---
