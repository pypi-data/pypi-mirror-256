import threading
import traceback
from datetime import datetime

class LocalArena:
    def __init__(self, num_rounds, players, timeout, handin, save_path):
        self.num_rounds = num_rounds
        self.players = players
        self.timeout = timeout
        self.handin_mode = handin
        self.timeout_tolerance = 5
        self.game_reports = {}
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.save_path = f"{save_path}/{timestamp}.txt"

    def run_func_w_time(self, func, timeout, name, alt_ret=None):
        def target_wrapper():
            nonlocal ret
            try:
                ret = func()
            except Exception as e:
                stack_trace = traceback.format_exc()
                print(f"Exception in thread running {name}: {e}\nStack Trace:\n{stack_trace}")
                if self.handin_mode: 
                    self.game_reports[name]['disconnected'] = True

        ret = alt_ret
        thread = threading.Thread(target=target_wrapper)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            thread.join()
            if not self.handin_mode:
                print(f"{name} Timed Out")
            print(f"{name} Timed Out")
            if name in self.game_reports:
                if 'timeout_count' in self.game_reports[name]:
                    self.game_reports[name]['timeout_count'] += 1
                if 'global_timeout_count' in self.game_reports[name]:
                    self.game_reports[name]['global_timeout_count'] += 1
        
        return ret

    def run_game(self):
        raise NotImplementedError
