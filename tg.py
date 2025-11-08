import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import FloodWaitError

api_id = your_api_id          # 换成你的 api id
api_hash = "your_api_hash"    # api hash
channel = "your_channel"      # 频道用户名

client = TelegramClient("user_session", api_id, api_hash)

# === 限速配置 ===
BATCH_SIZE = 200   # 每处理多少条消息后暂停一次
SLEEP_SEC = 1.5    # 暂停多久（秒）


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

    print("开始统计频道数据中，请稍等...")

    try:
        async for msg in client.iter_messages(channel, limit=None):
            total_msgs += 1

            # 浏览量
            v = getattr(msg, "views", None)
            if v is not None:
                total_views += int(v)
                if int(v) > most_viewed_views:
                    most_viewed_views = int(v)
                    most_viewed = msg

            # 转发
            fwd = getattr(msg, "forwards", None)
            if fwd is not None:
                total_forwards += int(fwd)

            # 评论
            if getattr(msg, "replies", None) is not None:
                rep = msg.replies.replies
                if rep is not None and rep > most_replied_count:
                    most_replied_count = rep
                    most_replied = msg

            # 媒体贴
            if msg.media is not None:
                total_with_media += 1

            # 最近30天发文数
            if msg.date and msg.date.replace(tzinfo=None) >= last_30:
                last_30_count += 1

            # 限速模块
            if total_msgs % BATCH_SIZE == 0:
                print(f"已处理 {total_msgs} 条消息，暂停 {SLEEP_SEC} 秒防止触发限速…")
                await asyncio.sleep(SLEEP_SEC)

    except FloodWaitError as e:
        print(f"检测到 Telegram FloodWait，暂停 {e.seconds} 秒...")
        await asyncio.sleep(e.seconds)

    # === 输出总结 ===
    print("\n=== 频道总结 ===")
    print(f"总消息数: {total_msgs}")
    print(f"总浏览量: {total_views}")
    if total_msgs > 0:
        print(f"平均每条浏览量: {total_views // total_msgs}")
    print(f"最近30天发文数: {last_30_count}")
    print(f"带媒体的帖子: {total_with_media} 条，占 {total_with_media * 100 // total_msgs if total_msgs else 0}%")
    print(f"总转发数: {total_forwards}")

    if most_viewed is not None:
        text_preview = (most_viewed.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(f"浏览量最高: id={most_viewed.id}, 浏览量={most_viewed_views}, 时间={most_viewed.date}, 内容={text_preview}")

    if most_replied is not None:
        text_preview = (most_replied.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(f"评论最多: id={most_replied.id}, 评论数={most_replied_count}, 时间={most_replied.date}, 内容={text_preview}")


if __name__ == "__main__":
    asyncio.run(main())
