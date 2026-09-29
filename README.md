# genpark-autonomous-calendar-deconfliction-scheduler-skill

> Autonomous Calendar Deconfliction Scheduler with Buffer Guarantees. 100% Python Standard Library.

Distilled from **Shuffle**, providing autonomous multi-party scheduling negotiation directly inside messaging channels without requiring external calendly links.

## Architecture

```mermaid
flowchart LR
    Request["Request: 'Find 30m with Alex on Tuesday'"] --> Scheduler["Calendar Deconfliction Scheduler"]
    Scheduler --> ConflictDetector["Scan Booked Blocks + Buffer Windows"]
    ConflictDetector --> SlotFilter["Filter Slots within Working Hours (09:00 - 18:00)"]
    SlotFilter --> Candidates["Formatted Candidate Timeslots"]
    Candidates --> MsgOutput["Formatted iMessage / WhatsApp Suggestion"]
```

## Features
- **Buffer Invariant**: Guarantees recovery time between consecutive meetings.
- **Lightweight & Standalone**: Zero third-party calendar client lock-in.
