import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import FloodWaitError

api_id = your_api_id          # Sustituye con tu api_id
api_hash = "your_api_hash"    # Sustituye con tu api_hash
channel = "your_channel"      # Nombre de usuario o enlace del canal

client = TelegramClient("user_session", api_id, api_hash)

# === Configuración de limitación de velocidad ===
BATCH_SIZE = 200   # Pausar después de procesar esta cantidad de mensajes
SLEEP_SEC = 1.5    # Duración de la pausa en segundos


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

    print("Recopilando estadísticas del canal, espera por favor...")

    try:
        async for msg in client.iter_messages(channel, limit=None):
            total_msgs += 1

            # Visualizaciones
            v = getattr(msg, "views", None)
            if v is not None:
                total_views += int(v)
                if int(v) > most_viewed_views:
                    most_viewed_views = int(v)
                    most_viewed = msg

            # Reenvíos
            fwd = getattr(msg, "forwards", None)
            if fwd is not None:
                total_forwards += int(fwd)

            # Respuestas
            if getattr(msg, "replies", None) is not None:
                rep = msg.replies.replies
                if rep is not None and rep > most_replied_count:
                    most_replied_count = rep
                    most_replied = msg

            # Mensajes con medios
            if msg.media is not None:
                total_with_media += 1

            # Publicaciones en los últimos 30 días
            if msg.date and msg.date.replace(tzinfo=None) >= last_30:
                last_30_count += 1

            # Control de velocidad
            if total_msgs % BATCH_SIZE == 0:
                print(f"Procesadas {total_msgs} mensajes, descansando {SLEEP_SEC} segundos para evitar limitaciones...")
                await asyncio.sleep(SLEEP_SEC)

    except FloodWaitError as e:
        print(f"Se detectó un FloodWait de Telegram, descansando {e.seconds} segundos...")
        await asyncio.sleep(e.seconds)

    # === Resumen ===
    print("\n=== Resumen del canal ===")
    print(f"Mensajes totales: {total_msgs}")
    print(f"Visualizaciones totales: {total_views}")
    if total_msgs > 0:
        print(f"Promedio de visualizaciones por mensaje: {total_views // total_msgs}")
    print(f"Publicaciones en los últimos 30 días: {last_30_count}")
    print(f"Mensajes con medios: {total_with_media} ({total_with_media * 100 // total_msgs if total_msgs else 0}% del total)")
    print(f"Reenvíos totales: {total_forwards}")

    if most_viewed is not None:
        text_preview = (most_viewed.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(
            "Más visto: "
            f"id={most_viewed.id}, visualizaciones={most_viewed_views}, hora={most_viewed.date}, contenido={text_preview}"
        )

    if most_replied is not None:
        text_preview = (most_replied.message or "").replace("\n", " ")
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(
            "Más respondido: "
            f"id={most_replied.id}, respuestas={most_replied_count}, hora={most_replied.date}, contenido={text_preview}"
        )


if __name__ == "__main__":
    asyncio.run(main())
