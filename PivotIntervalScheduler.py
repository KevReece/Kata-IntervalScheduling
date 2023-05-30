from collections import namedtuple

Request = namedtuple('Request', ['id', 'start_time', 'end_time'])

class PivotIntervalScheduler:
    
    def __init__(self, raw_requests):
        self.requests = sorted(raw_requests, key=lambda request: (request.start_time, request.end_time, request.id))
        self._memoised_schedule_sets_in_window = {}
        set_start_index = 0
        set_end_index = len(raw_requests)-1
        window_start_time = self.requests[set_start_index].start_time
        window_end_time = self.requests[set_end_index].end_time
        scheduled_indexes = self._memoised_schedule_set_in_window(
                set_start_index, 
                set_end_index, 
                window_start_time, 
                window_end_time)
        
        self.scheduled_requests = []
        for scheduled_indicies_index in range(len(scheduled_indexes)):
            scheduled_index = scheduled_indexes[scheduled_indicies_index]
            self.scheduled_requests.append(self.requests[scheduled_index])

    def _memoised_schedule_set_in_window(self, set_start_index, set_end_index, window_start_time, window_end_time):
        memo_key = (set_start_index, set_end_index, window_start_time, window_end_time)
        
        if memo_key in self._memoised_schedule_sets_in_window:
            return self._memoised_schedule_sets_in_window[memo_key]

        scheduled_indexes = self._schedule_set_in_window(set_start_index, set_end_index, window_start_time, window_end_time)

        self._memoised_schedule_sets_in_window[memo_key] = scheduled_indexes

        return scheduled_indexes
    
    def _schedule_set_in_window(self, set_start_index, set_end_index, window_start_time, window_end_time):
        best_scheduled_indexes = [] 

        for pivot_index in range(set_start_index, set_end_index+1):
            pivot_request = self.requests[pivot_index]
            iteration_scheduled_indexes = []
            if pivot_request.start_time >= window_start_time and pivot_request.end_time <= window_end_time:
                if pivot_index != set_start_index:
                    iteration_scheduled_indexes += self._memoised_schedule_set_in_window(set_start_index, pivot_index-1, window_start_time, pivot_request.start_time)
                iteration_scheduled_indexes.append(pivot_index)
                if pivot_index != set_end_index:
                    iteration_scheduled_indexes += self._memoised_schedule_set_in_window(pivot_index+1, set_end_index, pivot_request.end_time, window_end_time)
            if len(iteration_scheduled_indexes) > len(best_scheduled_indexes):
                best_scheduled_indexes = iteration_scheduled_indexes

        return best_scheduled_indexes
