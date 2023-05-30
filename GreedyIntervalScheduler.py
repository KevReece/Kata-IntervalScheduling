from collections import namedtuple

Request = namedtuple('Request', ['id', 'start_time', 'end_time'])

class GreedyIntervalScheduler:
    
    def __init__(self, raw_requests):
        requests = sorted(raw_requests, key=lambda request: (request.end_time, request.start_time, request.id))
        self.scheduled_requests = [requests[0]]
        last_end_time = requests[0].end_time
        for index in range(1, len(requests)):
            request = requests[index]
            if request.start_time >= last_end_time:
                self.scheduled_requests.append(requests[index])
                last_end_time = request.end_time
