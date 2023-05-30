from datetime import datetime
import unittest
# from PivotIntervalScheduler import PivotIntervalScheduler as IntervalScheduler, Request 
from GreedyIntervalScheduler import GreedyIntervalScheduler as IntervalScheduler, Request 

class TestIntervalScheduler(unittest.TestCase):

    def test_SingleRequest(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 2))
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        self.assertEqual(scheduled_requests, requests)
        
    def test_TwoExclusive(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 2)),
                Request(2, datetime(2000, 1, 2), datetime(2000, 1, 3)),
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        self.assertEqual(scheduled_requests, requests)
        
    def test_PreferEarlyEnd(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 1), datetime(2000, 1, 2))
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(2, datetime(2000, 1, 1), datetime(2000, 1, 2))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_PreferLowerId(self):
        requests = [
                Request(2, datetime(2000, 1, 1), datetime(2000, 1, 2)),
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 2))
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 2))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_TwoOverlapping(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 2), datetime(2000, 1, 4)),
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_TwoOverlappingReversed(self):
        requests = [
                Request(1, datetime(2000, 1, 2), datetime(2000, 1, 4)),
                Request(2, datetime(2000, 1, 1), datetime(2000, 1, 3)),
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(2, datetime(2000, 1, 1), datetime(2000, 1, 3))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_TwoOverlappingAndAnExclusive(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 2), datetime(2000, 1, 4)),
                Request(3, datetime(2000, 1, 4), datetime(2000, 1, 5)),
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(3, datetime(2000, 1, 4), datetime(2000, 1, 5))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_TwoOverlappingAndAnExclusiveReversed(self):
        requests = [
                Request(1, datetime(2000, 1, 4), datetime(2000, 1, 5)),
                Request(2, datetime(2000, 1, 2), datetime(2000, 1, 4)),
                Request(3, datetime(2000, 1, 1), datetime(2000, 1, 3))
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(3, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(1, datetime(2000, 1, 4), datetime(2000, 1, 5))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_DoubleExclusiveAndOverlapping(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 3), datetime(2000, 1, 5)),
                Request(3, datetime(2000, 1, 2), datetime(2000, 1, 3)),
                Request(4, datetime(2000, 1, 4), datetime(2000, 1, 5)),
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 3), datetime(2000, 1, 5))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_DoubleExclusiveAndOverlappingReversed(self):
        requests = [
                Request(1, datetime(2000, 1, 4), datetime(2000, 1, 5)),
                Request(2, datetime(2000, 1, 2), datetime(2000, 1, 3)),
                Request(3, datetime(2000, 1, 3), datetime(2000, 1, 5)),
                Request(4, datetime(2000, 1, 1), datetime(2000, 1, 3)),
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(4, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(3, datetime(2000, 1, 3), datetime(2000, 1, 5))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)
        
    def test_DoubleExclusiveAndOverlappingTripleExclusive(self):
        requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 3), datetime(2000, 1, 5)),
                Request(3, datetime(2000, 1, 6), datetime(2000, 1, 7)),
                Request(4, datetime(2000, 1, 2), datetime(2000, 1, 4)),
                Request(5, datetime(2000, 1, 4), datetime(2000, 1, 7))
            ]

        scheduled_requests = IntervalScheduler(requests).scheduled_requests
        
        expected_scheduled_requests = [
                Request(1, datetime(2000, 1, 1), datetime(2000, 1, 3)),
                Request(2, datetime(2000, 1, 3), datetime(2000, 1, 5)),
                Request(3, datetime(2000, 1, 6), datetime(2000, 1, 7))
            ]
        self.assertEqual(scheduled_requests, expected_scheduled_requests)