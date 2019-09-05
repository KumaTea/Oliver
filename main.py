from init import starting
from taskManager import manager, scheduler


if __name__ == '__main__':
    starting()
    manager()
    scheduler.start()
