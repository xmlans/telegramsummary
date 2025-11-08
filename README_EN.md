# Telegram Channel Summary

> Quickly collect key metrics from any Telegram channel using the Telegram Developer API and Telethon.

## Introduction

Telegram Channel Summary is a Python script that leverages Telethon to fetch subscriber counts, message histories, and other essential channel data. The output presents a concise overview that helps you evaluate channel performance at a glance.

## Getting Started

### 1. Install dependencies

Make sure Python is installed, then install Telethon:

```bash
pip install telethon
```

### 2. Configure developer credentials

1. Open the [Telegram developer portal](https://my.telegram.org/apps).
2. Create an application to obtain your `api_id` and `api_hash`.
3. Update the `api_id` and `api_hash` values in `tg.py` with your own credentials.

### 3. Configure channel parameters

- Set the `channel` variable in `tg.py` to the username of the channel you want to analyze.
- Adjust `BATCH_SIZE` as needed; for channels with more than 1,000 messages, increase the value to respect Telegram rate limits.

### 4. Run the script

Launch the script with:

```bash
python tg.py
```

On first run, follow the prompts to enter your phone number (including country code, for example `+13333333333`). Telegram will send a verification code—enter it when requested and wait for the summary to be generated.

## Output example

![Renderings](pic.png)
