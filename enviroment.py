import spade
from drone import Drone


async def main():
    
    receiveragent = ReceiverAgent("admin@leandro", "admin")
    await receiveragent.start(auto_register=True)
    print("Receiver started")

    senderagent = SenderAgent("dummy@leandro", "dummy")
    await senderagent.start(auto_register=True)
    print("Sender started")

    await spade.wait_until_finished(receiveragent)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())