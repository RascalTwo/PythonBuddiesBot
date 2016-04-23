import threading
import time

class Loop():
    """Run a function mutiple times.

    May have a delay, and may listen to the function
    being executed to stop the thread.

    Methods:
        `__init__` - Create this thread with provided arguments.
        `toggle`   - Switches the current running state to
                     opposite of whatever it currently is.
        `start`    - Start this thread.
        `stop`     - Stop this thread.
        `_run`     - Method with function execution within.
    """

    def __init__(self, function, delay, start_now=True, listen=False):
        """Create a loop thread that executes a function.

        Function will be executed with a delay each time.
        If `listen_to_function` is true, then if the function
        being executed returns `True`, this thread is stopped.

        Arguments:
            `function` (function) - Function to be executed.
            `delay` (int)         - Delay in seconds between
                                    executions of function.
            `start_now` (bool)    - Start now, otherwise must be
                                    started later manually.
            `listen` (bool)       - Determines if this thread stops
                                    when the `function` returns true.
        """
        self.function = function
        self.listen = listen
        self.running = False
        self.delay = delay
        if start_now:
            self.start()

    def toggle(self):
        """Switch the running state to opposite of itself."""
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        """Start the thread."""
        self.running = True
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def stop(self):
        """Stop the thread."""
        self.running = False

    def _run(self):
        while self.running:
            if self.function() is True and self.listen:
                self.stop()
            time.sleep(self.delay)
