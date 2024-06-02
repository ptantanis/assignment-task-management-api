from typing import List

TOTAL_ONE_DAY_SLOT = 48 # 30 minutes per slot

def merge_ranges_solution_1(meetings: List[tuple]):
    meetings = sorted(meetings)
    busy_ranges = []
    busy_slot = meetings[0]
    for pointer in range(1, len(meetings)): 
        next_meeting = meetings[pointer]
        if next_meeting[0] <= busy_slot[1]:
            busy_slot = (busy_slot[0], next_meeting[1]) if next_meeting[1] > busy_slot[1] else busy_slot
        else:
            busy_ranges.append(busy_slot)
            busy_slot = next_meeting
    busy_ranges.append(busy_slot)
        
    return busy_ranges

def merge_ranges_solution_2(meetings: List[tuple]):
    one_day_slots = ['available'] * TOTAL_ONE_DAY_SLOT

    for meeting in meetings:
        one_day_slots[meeting[0]: meeting[1]] = ['busy'] * (meeting[1] - meeting[0])
    
    busy_ranges = []
    for slot_index, slot_status in enumerate(one_day_slots):
        if slot_status != 'busy':
            continue
        
        if len(busy_ranges) > 0 and busy_ranges[-1][1] == slot_index:
            busy_ranges[-1] = (busy_ranges[-1][0], slot_index + 1)
        else:
            busy_ranges.append((slot_index, slot_index + 1))
            
    return busy_ranges

print(merge_ranges_solution_2([(1, 2), (2, 3)])) # [(1, 3)]
print(merge_ranges_solution_2([(0, 1), (3, 5), (4, 8), (10, 12), (9, 10)])) # [(0, 1),(3, 8),(9, 12)]
print(merge_ranges_solution_2([(1, 5), (2, 3), (6, 7)])) # [(1, 5), (6, 7)]
print(merge_ranges_solution_2([(1, 5), (2, 3), (6, 10), (5, 8)])) # [(1, 10)]