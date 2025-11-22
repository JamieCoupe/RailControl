# Application Layer

The application layer orchestrates **use cases** by coordinating domain entities and repositories.

It contains **workflow logic**, not business logic.

---

## Services

Located in:

```
application/services/
```

Services include:

- RoutingService  
- TimetableService  
- IndustrySimulationService  
- WaybillGenerator  
- ConflictChecker  
- TopologyBuilder  

Each service:

- Depends on domain repositories  
- Manipulates domain entities  
- Returns DTOs  
- Contains no persistence logic

---

## DTOs

Located in:

```
application/dto/
```

DTOs are:

- Simple data carriers  
- Returned to the UI  
- Not domain objects  
- Safe for serialization  

Examples:

- TimetableEntryDTO  
- RouteDTO  
- WaybillDTO  

---

## Commands & Queries

### Commands:
- Generate timetable  
- Generate waybills  
- Run industry simulation  

### Queries:
- List stations  
- Get road details  
- Fetch industry requirements  

Application services expose these via clearly defined interfaces.

---

## Workflow Example

```
CLI → TimetableService → Domain (Road, Station, Junction)
                         → RoutingService
                         → ConflictChecker
                         → TimetableEntryDTO → CLI
```

---

## Notes

- Application layer does not know *how* data is stored (JSON, SQL, etc.)  
- Application layer must remain pure logic  
- DTOs isolate the domain from UI concerns  

