import logging
from queue import Empty, Queue

from nicegui import app

from ezlab.parameters import TASK_FINISHED


def process_messages(queue: Queue, number_of_tasks: int = 1):
    while True:
        try:
            message = queue.get_nowait()
            if message is not None:
                if TASK_FINISHED in message:
                    app.storage.general["ui"]["finished_tasks"] += 1
                    logging.info(
                        f"Completed jobs: {app.storage.general['ui']['finished_tasks']}"
                    )
                    if app.storage.general["ui"]["finished_tasks"] == number_of_tasks:
                        logging.info("All tasks completed")
                        app.storage.general["ui"]["finished_tasks"] = 0
                        queue.task_done()
                        return True
                else:
                    if "error" in message or "failed" in message:
                        logging.error(message)
                    else:
                        logging.info(message)
                    # less eager for polling the queue
                    # sleep(0.3)
        except Empty:
            pass
        except Exception as error:
            queue.put(TASK_FINISHED)
            queue.task_done()
            print(error)
            return False
