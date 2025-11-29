# Domain Layer

The domain layer models the **business concepts** of a railway.  
It contains pure domain logic without:

- JSON parsing  
- SQL code  
- UI references  
- External dependencies

This is the core of the system.

---

## Structure

```
domain/
    track/
    station/
    industry/
    rolling_stock/
    timetable/
    freight/
    repositories/
```

---

## Track & Topology

Entities include:

- Road (abstract block)
- PlatformRoad (specialisation)
- IndustryRoad (specialisation)
- TrackSection (atomic track piece)
- Junction (node)
- Turnout (specialised branching junction)
- SpeedRestriction

These form the layout topology.

---

## Industries

- Industry represents a customer  
- IndustryInput & IndustryOutput define demand and production  
- IndustryRoad links industries to track for loading/unloading  
- Industries aggregate their loading roads

---

## Stations

- Station includes name, area  
- Station references Roads that are platforms  
- PlatformRoad is a subclass of Road

---

## Rolling Stock

- Wagon  
- WagonType  
- Locomotive (optional for later)

---

## Timetable & Freight

- TrainService and Timetable represent passenger operations  
- Waybill and FreightFlow represent freight tasks

---

## Repository Interfaces

Located in `domain/repositories/`.

Examples:

- RoadRepository
- StationRepository
- IndustryRepository
- JunctionRepository

These are abstract interfaces with no implementation.

---

## Key Rules

- The domain does **not** include join-table objects  
- Domain relationships use lists (e.g., `Station.roads`)  
- Only aggregate roots have repositories  
- Domain must be persistence-agnostic

