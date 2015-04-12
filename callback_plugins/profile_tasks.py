import prettytable
import time


class CallbackModule(object):
    """
    A plugin for timing tasks
    """
    def __init__(self):
        self.stats = {
            "Total time": 0
        }
        self.current = None

    def playbook_on_task_start(self, name, is_conditional):
        """
        Logs the start of each task
        """
        if self.current is not None:
            # Record the running time of the last executed task
            spent = time.time() - self.stats[self.current]
            self.stats[self.current] = spent
            self.stats["Total time"] += spent

        # Record the start time of the current task
        self.current = name
        self.stats[self.current] = time.time()

    def playbook_on_stats(self, stats):
        """
        Prints the timings
        """
        # Record the timing of the very last task
        if self.current is not None:
            self.stats[self.current] = time.time() - self.stats[self.current]

        # Sort the tasks by their running time
        results = sorted(
            self.stats.items(),
            key=lambda value: value[1],
            reverse=True,
        )

        # Just keep the top 10
        results = results[:30]
        t = prettytable.PrettyTable(["Role", "Task", "Elapsed"])
        t.header_style = "upper"
        t.align["Role"] = "l"
        t.align["Task"] = "l"
        t.align["Elapsed"] = "r"
        # Print the timings
        for name, elapsed in results:
            s = name.split("|", 1)
            if len(s) == 1:
                role = ""
                task = s[0]
            else:
                role = s[0]
                task = s[1].strip()
            t.add_row((role, task, '{0:.02f}s'.format(elapsed)))
        print(t)