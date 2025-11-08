import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import FloodWaitError

api_id = your_api_id          # Replace with your api_id
api_hash = "your_api_hash"    # Replace with your api_hash
channel = "your_channel"      # Channel username or link

client = TelegramClient("user_session", api_id, api_hash)

# === Rate limit configuration ===
BATCH_SIZE = 200   # Pause after processing this many messages
SLEEP_SEC = 1.5    # Pause duration in seconds


async def main():
    await client.start()

    total_views = 0
    total_msgs = 0
    total_forwards = 0
    total_with_media = 0
    most_viewed = None
    most_viewed_views = -1
    most_replied = None
    most_replied_count = -1

    now = datetime.utcnow()
    last_30 = now - timedelta(days=30)
    last_30_count = 0

    print("Collecting channel statistics, please wait...")

    try:
        async for msg in client.iter_messages(channel, limit=None):
            total_msgs += 1

            # Views
            v = getattr(msg, "views", None)
            if v is not None:
                total_views += int(v)
                if int(v) > most_viewed_views:
                    most_viewed_views = int(v)
                    most_viewed = msg

            # Forwards
            fwd = getattr(msg, "forwards", None)
            if fwd is not None:
                total_forwards += int(fwd)

            # Replies
            if getattr(msg, "replies", None) is not None:
                rep = msg.replies.replies
                if rep is not None and rep > most_replied_count:
                    most_replied_count = rep
                    most_replied = msg

            # Messages with media
            if msg.media is not None:
                total_with_media += 1

            # Posts in the last 30 days
            if msg.date and msg.date.replace(tzinfo=None) >= last_30:
                last_30_count += 1

            # Rate limiting
            if total_msgs % BATCH_SIZE == 0:
                print(f"Processed {total_msgs} messages, sleeping {SLEEP_SEC} seconds to avoid rate limits...")
                await asyncio.sleep(SLEEP_SEC)

    except FloodWaitError as e:
        print(f"Telegram FloodWait detected, sleeping for {e.seconds} seconds...")
        await asyncio.sleep(e.seconds)

    # === Summary output ===
    print("\n=== Channel summary ===")
    print(f"Total messages: {total_msgs}")
    print(f"Total views: {total_views}")
    if total_msgs > 0:
        print(f"Average views per message: {total_views // total_msgs}")
    print(f"Posts in the last 30 days: {last_30_count}")
    print(f"Messages with media: {total_with_media} ({total_with_media * 100 // total_msgs if total_msgs else 0}% of total)")
    print(f"Total forwards: {total_forwards}")

    if most_viewed is not None:
        text_preview = (most_viewed.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(
            "Most viewed: "
            f"id={most_viewed.id}, views={most_viewed_views}, time={most_viewed.date}, content={text_preview}"
        )

    if most_replied is not None:
        text_preview = (most_replied.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(
            "Most replied: "
            f"id={most_replied.id}, replies={most_replied_count}, time={most_replied.date}, content={text_preview}"
        )


if __name__ == "__main__":
    asyncio.run(main())
