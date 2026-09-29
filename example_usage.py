from client import CalendarDeconflictionScheduler

scheduler = CalendarDeconflictionScheduler(day_start_hour=9, day_end_hour=17, buffer_minutes=15)

# Existing commitments
scheduler.book_slot(9, 30, 60, "All-Hands Meeting")
scheduler.book_slot(13, 0, 45, "Client Demo")

# Find free 30-minute meeting slots with 15-minute buffers
open_slots = scheduler.find_available_slots(duration_min=30)
print(f"Found {len(open_slots)} viable non-conflicting slots:")
for s in open_slots:
    print(f" - {s['start_hour']:02d}:{s['start_min']:02d} (Duration: {s['duration_min']}m)")
