
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

## Command-line Arguments

| Short | Long           | Type    | Required | Default    | Choices                       | Description                                                      |
|-------|----------------|---------|----------|------------|------------------------------|------------------------------------------------------------------|
| -l    | --urlspath     | str     | Yes      |            |                              | Path to file containing list of target URLs for Injection.      |
| -w    | --wordlist     | str     | No       |            |                              | Path to a file containing parameters to fuzz for reflection.    |
| -p    | --parameter    | str     | No       | "nexovir"  |                              | Comma-separated parameter to test for reflection.                |
| -vm   | --valuemode    | str     | No       | "append"   | append, replace               | How to apply valuemode: append or replace.                       |
| -gm   | --generatemode | str     | No       | "all"      | root, ignore, combine, all   | Control how parameters are generated.                            |
| -c    | --chunk        | int     | No       | 25         |                              | Number of URLs to process per batch.                             |
| -s    | --silent       | flag    | No       | False      |                              | Disable printing output to the command line.                     |
| -o    | --output       | str     | No       |            |                              | Path to file where discovered URLs should be saved.             |

---

## Examples

Inject parameter "nexovir" into URLs from `urls.txt` using parameters from `params.txt`, appending values, processing 25 URLs per batch, and saving output:

```bash
python injector.py -l urls.txt -w params.txt -p nexovir -vm append -gm all -c 25 -o output.txt
```

Run silently without printing to terminal:

```bash
python injector.py -l urls.txt -p nexovir -s
```
