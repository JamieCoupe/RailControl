# Railway Operations Simulator
### Timetable + Freight + Routing Engine

This project is a modular, domain-driven system for generating timetables, waybills, freight flows, and routing for a model railway.  
It supports industries, stations, track topology, wagon types, and operational constraints.

The architecture follows **Domain-Driven Design (DDD)** with clean separation into layers:

- Domain Layer — core railway concepts and business rules  
- Application Layer — workflow orchestration (routing, timetables, waybills)  
- Infrastructure Layer — JSON/YAML loading, DB persistence  
- Presentation Layer — CLI or UI frontend

---

## Project Structure

```
project_root/
    domain/
    domain/repositories/
    application/
        services/
        dto/
    infrastructure/
        repositories/
        loaders/
        database/
    presentation/
        cli/
```

---

## Domain Layer
Contains *real railway concepts*:

- Road, PlatformRoad, IndustryRoad  
- TrackSection, Junction, Turnout  
- Station, Platform  
- Industry, IndustryInput, IndustryOutput  
- Wagon, WagonType  
- TrainService, Timetable  
- Waybill

No persistence or UI logic appears in this layer.

---

## Application Layer
Implements system workflows:

- Routing trains  
- Generating timetables  
- Creating freight waybills  
- Simulating industries  
- Conflict checking  

Returns DTOs, not domain objects.

---

## Infrastructure Layer
Provides:

- JSON/YAML file loaders  
- Repository implementations  
- Optional SQL adapters  
- Database schemas

Domain never depends on infrastructure.

---

## Presentation Layer
Provides UI (CLI or otherwise) consuming DTOs.

---

## Features Supported

- Passenger timetable generation  
- Freight schedules  
- Industry demand simulation  
- Waybill creation  
- Routing across topology  
- Conflict checks (track, platform, turnout)  
- Train length vs platform/siding validation  

---

## Status
Currently implementing scaffolding: domain, repositories, services, folder structure.

