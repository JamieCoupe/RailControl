# Infrastructure Layer

The infrastructure layer provides **technical details** for persistence and external data loading.

It contains code the domain and application layers must not depend on.

---

## Responsibilities

- JSON/YAML loading  
- Database persistence  
- Repository implementations  
- Configuration  
- Low-level adapters  

---

## Repositories

Located in:

```
infrastructure/repositories/
```

Example files:

- SqlRoadRepository  
- JsonStationRepository  
- YamlIndustryLoader  

These classes:

- Implement domain repository interfaces  
- Convert raw data into domain objects  
- Handle joins (e.g., station → roads)  
- Instantiate correct subclasses (PlatformRoad, IndustryRoad)

---

## Loaders

Located in:

```
infrastructure/loaders/
```

These read:

- layout files  
- industry definitions  
- wagon type lists  
- speed restrictions  

And produce domain objects via builders or repositories.

---

## Database Folder

```
infrastructure/database/
```

Contains:

- schema.sql  
- migration scripts  
- connection logic  

(Only if SQL is used later.)

---

## Rules

- This layer can depend on the domain  
- Domain may **not** depend on infrastructure  
- Infrastructure must remain replaceable (JSON ↔ SQL ↔ API)

