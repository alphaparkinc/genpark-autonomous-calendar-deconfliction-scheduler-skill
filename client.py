"""Autonomous Calendar Deconfliction Scheduler.
100% Python Standard Library.
"""

class CalendarDeconflictionScheduler:
    """Finds optimal non-conflicting meeting slots and prevents back-to-back calendar fatigue."""
    def __init__(self, day_start_hour=9, day_end_hour=18, buffer_minutes=15):
        self.day_start_hour = day_start_hour
        self.day_end_hour = day_end_hour
        self.buffer_minutes = buffer_minutes
        self.booked_slots = []

    def book_slot(self, start_hour, start_min, duration_min, title):
        start_total = start_hour * 60 + start_min
        end_total = start_total + duration_min
        self.booked_slots.append((start_total, end_total, title))
        self.booked_slots.sort(key=lambda x: x[0])

    def find_available_slots(self, duration_min):
        day_start = self.day_start_hour * 60
        day_end = self.day_end_hour * 60
        required_span = duration_min + self.buffer_minutes
        
        available = []
        cursor = day_start
        for start, end, title in self.booked_slots:
            if start - cursor >= required_span:
                available.append({
                    "start_hour": cursor // 60,
                    "start_min": cursor % 60,
                    "duration_min": duration_min
                })
            cursor = max(cursor, end + self.buffer_minutes)

        if day_end - cursor >= duration_min:
            available.append({
                "start_hour": cursor // 60,
                "start_min": cursor % 60,
                "duration_min": duration_min
            })
        return available
