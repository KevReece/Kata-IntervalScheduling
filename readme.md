Interval Scheduling Kata
===

Given a resource, such as a meeting room, and a number of requests for exclusive use of the resource, specific to start and end times, find the largest set of exclusive usages, where largest is defined by quantity of usages.

Problem analysis
---
### Solvability and Solution Quality
- Can have many valid but non-optimal answers
- Can have multiple correct answer (such as with duplicate requests), so one quality of an algorithm is stability (i.e. it is consistant in the case of duplicates)

### Definition of done
- Verifying validity of an answer is simple based on the problem statement, and consists of checking for overlaps (e.g. order by start times, then iterate, comparing item end to next item start)
- The problem statement doesn't offer any means to verify an answer is optimal, outside of a full search of combinations, which itself would be an algorthmic solution. So verification must be based on a suite of test cases of request sets, covering all identified complexities:
    1. single request
    2. two exclusive requests
    3. two overlapping requests
    4. reversed two overlapping requests (verify stability)
    5. two exclusive requests and a further fully overlapping request
    5+ the same but reverse order input
    6. two exclusive requests and a further double partially overlapping request
    6+ the same but reverse order input
    7. three exclusive requests and two overlapping exclusive requests
- Stability could come in two forms: fully dependent on input ordering; dependant on ordered inputs, then dependant on original ordering for duplicates. However for duplicates some unique input identifer would be needed to refer back to which request was successfully scheduled.

### Brute force
Brute force approach = loop permutations verifiying validity, valid permutation is set as answer, if it's larger than prior answer
    (m = number of requests)
    - time complexity
        - loop permutations efficiency = O(2^n) ordered combinations aren't required (as the exclusive set is naturally ordered by start time), permutations increase exponentially as the number of items increase
        - verify permutation efficiency = O(n) per loop, check each item for overlap with neighbour, assumes a pre-ordered list of requests (ordered by start time)
        - pre-order list efficiency = O(n^2)
        - compare permutation size efficiency = n(1) per loop
        - = total time complexity of O(2^n)
    - space complexity
        - loop permutations: O(1) through enumaration
        - verify permutation: O(1) by verifying neighbours
        - pre-order list: O(n)
        - compare permutation: O(n) by only storing one best permutation of n requests to compare to current permutation
        - = total space complexity of O(n)

Solution analysis
---

### Algorithmic patterns
- Due to the permutations nature of the problem space, and due to the reuse of subsets of permutations within in potetential answers, this problem intuitively lends itself to known algorithmic patterns:
    1. dynamic programming, where a each smaller set of requests can be calculated for validity and then used in supersets. This may either apply as a core algorithm or as an optimisation to improve the average.
    2. greedy algorithm, where we start with least impactful request, i.e. one with minimal overlaps, and build our set of requests progressively from there. As always with greedy, this would often find a local minima, but could be useful in large data sets where other algorithms are too expensive in time complexity
    3. divide and conquer, where requests are clustered, and the clusters don't overlap, each cluster can be divided away and conquered separately. This approach may be a step improvement in the average case, or when particularly well suited to a domain, it could be highly benefical to the average case, such as large but highly clusterd data (such as hotel bookings on seasonal properties).
    4. tree stuctured exploration, where the permutations are explored based on a self organising structure, rather than upfront definition

### Improving on brute force
The brute force approach largest limitation is the permutation loop time complexity, so this should be the target of reduction. Below that is the pre-order time complexity, of O(n^2), so we should look to reduce towards that. The pre-order list step is required to keep the verifiy permutation step from increasing from O(n) to O(o^2) (within the permutation loops), so the pre-order is unlikely to reducable. 
The brute force approach space complexity limitation of O(n) cannot be reduced as the output space complexity is also O(n).

The permutations loop may be reducable to O(n^2), by first ordering the dataset, and then exploring it as an ordered tree structure of permutations. This can be achieved by spliting the input set at each request giving a left subset, a pivot request, and a right subset, for each of the n requests. The left and right set can then be solved recursivly, by finding all the pivots that are valid for the parent available time window, and then going to the left and right of that within the recursive subset (for those left/right subsets that exist). This pivot split continues until the recursive subset is a single request and cannot be broken further. Through dynamic programming each recursive set can be memoised, based on the sub-window and subset. Due to the processing only of unique sequential chains of requests (rather than every permutation), the loop will be for every possible subset size (=n-1), multiplied by every shifted position of that size (<=n), therefore O(n^2).

Pseudocode
---
```pseudo
GIVEN requests: ARRAY OF Request

TYPE Request = (id: ID, start_time: TIME, end_time: TIME)

ordered_requests := ORDER(requests, key: (request.start_time, request.end_time, request.id))
set_start_index := 1
set_end_index := LENGTH(requests)
window_start_time := ordered_requests[set_start_index].start_time
window_end_time := ordered_requests[set_end_index].end_time
scheduled_indexes := MemoisedScheduleSetInWindow(ordered_requests, set_start_index, set_end_index, window_start_time, window_end_time)
FOR scheduled_index IN scheduled_indexes:
    PRINT(ordered_requests[scheduled_index])
END FOR

FUNCTION MemoisedScheduleSetInWindow
    requests: ARRAY OF Request
    set_start_index: INTEGER
    set_end_index: INTEGER
    window_start_time: TIME
    window_end_time: TIME

    IF IS_MEMOISED((set_start_index, set_end_index, window_start_time, window_end_time))
        RETURN GET_MEMOISED((set_start_index, set_end_index, window_start_time, window_end_time))
    END IF

    scheduled_indexes := ScheduleSetInWindow(requests, set_start_index, set_end_index, window_start_time, window_end_time)

    SET_MEMOISED((set_start_index, set_end_index, window_start_time, window_end_time), scheduled_indexes)

    RETURN scheduled_indexes
END FUNCTION

FUNCTION ScheduleSetInWindow
    requests: ARRAY OF Request
    set_start_index: INTEGER
    set_end_index: INTEGER
    window_start_time: TIME
    window_end_time: TIME

    best_scheduled_indexes := [] 
    FOR pivot_index IN set_start_index TO set_end_index:
        pivot_request := requests[pivot_index]
        iteration_scheduled_indexes := []
        IF pivot_request.start_time >= window_start_time AND pivot_request.end_time <= window_end_time
            IF index NOT set_start_index:
                iteration_scheduled_indexes := iteration_scheduled_indexes + MemoisedScheduleSetInWindow(requests, set_start_index, pivot_index-1, window_start_time, pivot_request.start_time)
            END IF
            iteration_scheduled_indexes := iteration_scheduled_indexes + pivot_index
            IF index NOT set_end_index:
                iteration_scheduled_indexes := iteration_scheduled_indexes + MemoisedScheduleSetInWindow(requests, pivot_index+1, set_end_index, pivot_request.end_time, window_end_time)
            END IF
        END IF
        IF LENGTH(scheduled_indexes) > LENGTH(best_scheduled_indexes)
            best_scheduled_indexes := iteration_scheduled_indexes
        END IF
    END FOR

    RETURN best_scheduled_indexes
END FUNCTION
```

### Analysis

 (n = number of requests)
- Time complexity: 
    - O(n^2), due to recursion of unique sequential chains of requests
    - Theta(n^2), assuming an equal mix of overlapping and non-overlapping requests the order of complexity is unchanged
    - Omega(n), for the case that all requests overlap, the first set of pivots will be found, but all subsequent pivots will be out of window
- Space complexity O(n), the auxiliary memory usage matches the input size due to the ORDER operation
- The solution is stable, and will have a preference for shorter and earlier requests due to the iteration through pivots sequentially and their comparisons at the iteration level.
- An ID was added to the request to as this would be needed to allow handling of duplicate requests. Without a request ID, the question of stablity is not relevent as there is no link back to the originating request.

### Further Optimisations

- Greedy approach of limiting search branches. The FOR loops could be opinionated on which pivots are worth persuing, based on some imperfect presumptions to reduce computation time. An example presumption would be that only requests below a certain size are worth persuing.
- Exit search when current best subset size is unobtainable by other subsets. This optimisation would improve the average complexity by exiting the pivot for loop when a scheduled subset contains all the available requests, therefore no other subset can exceed this size. 
- Divide and conquer clusters of non-overlapping subsets. This opinionated optimisation could significantly reduce average complexity for large clustered input request sets. This would involve an extra O(n) step after ordering requests to iterate the input requests, checking for subsets that have no overlaps. These could then be passed to the main functions separately.

Official solution (Earliest deadline first algorithm)
---

### Greedy solution

There is a more efficient algorithm, which utilises a greedy algorithm of taking the request with the earliest end time, then rejecting those that overlap, then repeating. This algorithm works due to the earliest end time request being a completely safe option to assume, as it can't be worse than any of it's overlapping requests, which can then be safely discarded. 

### Efficiency

- This algorithm time efficieny is then driven by an ordering by request end time, so O(nlogn)), after this sort there is only an O(n) iteration of scheduling requests which don't overlap. 
- The space efficiency is again driven entirely by the sorting algorithm and is therefore O(n), or lower if the input has no restriction on mutation. 
- The solution is also stable based on the ordering of requests used.

### Pseudocode

```pseudo
GIVEN requests: ARRAY OF Request

TYPE Request = (id: ID, start_time: TIME, end_time: TIME)

ordered_requests := ORDER(requests, key: (request.end_time, request.start_time, request.id))
last_end_time := -INFINITY
FOR index IN LENGTH(ordered_requests):
    request := ordered_requests[index]
    IF request.start_time > last_end_time:
        last_end_time := request.end_time
        PRINT(request)
    END IF
END FOR
```
