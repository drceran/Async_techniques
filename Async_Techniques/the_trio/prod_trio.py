import datetime
import colorama
import random
import trio


async def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)

    # Create a bounded channel (like a queue)
    send_channel, receive_channel = trio.open_memory_channel(10)

    with trio.move_on_after(5):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(generate_data, 20, "Prod1", send_channel.clone())
            nursery.start_soon(generate_data, 20, "Prod2", send_channel.clone())
            nursery.start_soon(process_data, 40, receive_channel)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE +
          f"App exiting, total time: {dt.total_seconds():,.2f} sec.",
          flush=True)


async def generate_data(num: int, name: str, send_channel: trio.MemorySendChannel):
    async with send_channel:
        for idx in range(1, num + 1):
            item = (idx * idx, datetime.datetime.now())
            await send_channel.send(item)

            print(colorama.Fore.YELLOW + f" -- {name} generated item {idx}", flush=True)
            await trio.sleep(random.random() + 0.5)


async def process_data(num: int, receive_channel: trio.MemoryReceiveChannel):
    processed = 0
    async with receive_channel:
        while processed < num:
            item = await receive_channel.receive() 
            processed += 1

            value, t = item
            dt = datetime.datetime.now() - t

            print(colorama.Fore.CYAN +
                  f" +++ Processed value {value} after {dt.total_seconds():,.2f} sec.",
                  flush=True)
            await trio.sleep(0.5)


if __name__ == '__main__':
    trio.run(main)
