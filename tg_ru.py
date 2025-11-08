import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import FloodWaitError

api_id = your_api_id          # Замените на свой api_id
api_hash = "your_api_hash"    # Замените на свой api_hash
channel = "your_channel"      # Имя пользователя или ссылка на канал

client = TelegramClient("user_session", api_id, api_hash)

# === Настройки ограничения скорости ===
BATCH_SIZE = 200   # Пауза после обработки такого количества сообщений
SLEEP_SEC = 1.5    # Длительность паузы в секундах


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

    print("Собираем статистику канала, пожалуйста подождите...")

    try:
        async for msg in client.iter_messages(channel, limit=None):
            total_msgs += 1

            # Просмотры
            v = getattr(msg, "views", None)
            if v is not None:
                total_views += int(v)
                if int(v) > most_viewed_views:
                    most_viewed_views = int(v)
                    most_viewed = msg

            # Пересылки
            fwd = getattr(msg, "forwards", None)
            if fwd is not None:
                total_forwards += int(fwd)

            # Ответы
            if getattr(msg, "replies", None) is not None:
                rep = msg.replies.replies
                if rep is not None and rep > most_replied_count:
                    most_replied_count = rep
                    most_replied = msg

            # Сообщения с медиа
            if msg.media is not None:
                total_with_media += 1

            # Публикации за последние 30 дней
            if msg.date and msg.date.replace(tzinfo=None) >= last_30:
                last_30_count += 1

            # Контроль частоты запросов
            if total_msgs % BATCH_SIZE == 0:
                print(f"Обработано {total_msgs} сообщений, пауза {SLEEP_SEC} сек. чтобы избежать ограничений...")
                await asyncio.sleep(SLEEP_SEC)

    except FloodWaitError as e:
        print(f"Обнаружен FloodWait Telegram, пауза {e.seconds} секунд...")
        await asyncio.sleep(e.seconds)

    # === Итоговая сводка ===
    print("\n=== Сводка по каналу ===")
    print(f"Всего сообщений: {total_msgs}")
    print(f"Всего просмотров: {total_views}")
    if total_msgs > 0:
        print(f"Среднее число просмотров: {total_views // total_msgs}")
    print(f"Публикаций за последние 30 дней: {last_30_count}")
    print(
        f"Сообщений с медиа: {total_with_media} "
        f"({total_with_media * 100 // total_msgs if total_msgs else 0}% от общего числа)"
    )
    print(f"Всего пересылок: {total_forwards}")

    if most_viewed is not None:
        text_preview = (most_viewed.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(
            "Самое просматриваемое: "
            f"id={most_viewed.id}, просмотров={most_viewed_views}, время={most_viewed.date}, содержание={text_preview}"
        )

    if most_replied is not None:
        text_preview = (most_replied.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(
            "Больше всего ответов: "
            f"id={most_replied.id}, ответов={most_replied_count}, время={most_replied.date}, содержание={text_preview}"
        )


if __name__ == "__main__":
    asyncio.run(main())
