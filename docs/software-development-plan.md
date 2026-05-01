# Software Development Plan

## Project Overview

**Project:** Touch & Go — Biometric Attendance System
**Course:** CSC354 — Software Engineering
**Institution:** Kutztown University of Pennsylvania
**Semester:** Spring 2023 → Fall 2023

---

## Team

| Member | Role |
|---|---|
| Nathan Shutter | Systems architecture, configuration management, delivery |
| Joe | Software process model, validation plan, sequence diagrams |
| Chris | Hardware research, prototype construction, budget |

---

## Process Model

The project followed an **Agile/Scrum** process with two-week sprints. Weekly team meetings were held with a Discord channel for async communication and a GitHub Kanban board for issue tracking.

---

## Project Phases & Gantt Summary

| Phase | Description | Duration | Owner |
|---|---|---|---|
| 1 — Scope | Product description, context diagram, personas, use cases | 6 weeks | Team |
| 2 — Planning | Project organization, feasibility, budget, wireframes | 5 weeks | Team |
| 3 — Requirements | Team description, process model, validation plan | 3 weeks | Team |
| 4 — Architecture | Version control, dev environment, software/hardware stack | 1 week | Nate / Chris |
| 5 — Prototype | Test plan, hardware research, build, delivery | 4 weeks | Chris / Nate |
| 6 — High-Level Design | Class diagram, detailed design specification | 4 weeks | Nate / Joe |
| 7 — Sprints | Seven 2-week implementation sprints | 8 weeks | Team |
| 8 — Acceptance Testing | End-to-end validation | 2 weeks | Team |
| 9 — Final Delivery | Polish, documentation, handoff | 1 week | Team |

---

## Sprint Retrospectives

### Sprint 2

| | Continue | Stop | Start |
|---|---|---|---|
| Nate | Reach out when help is needed; break requirements into smaller tasks | Procrastination | Plan tasks per sprint more efficiently; communicate more effectively |
| Joe | Communicating and coming to meetings ready to work | Meeting without a specific agenda | Meet in person for team tasks |
| Chris | Working together, planning ahead, asking for help | Thinking inside the box | Finish must-haves first |

### Sprint 3

| | Continue | Stop | Start |
|---|---|---|---|
| Nate | Knowing what we're working on; collaborating over calls | Pushing off higher-priority items | Define work before starting meetings; update Kanban before retrospectives |
| Joe | Communicating and working together to hit sprint goals | Working in large chunks instead of consistently | Post meeting agendas in Discord ahead of time |
| Chris | Meeting consistently with an agenda | Not communicating problems | Finish must-haves |

### Sprint 4

| | Continue | Stop | Start |
|---|---|---|---|
| Nate | Integrating work together; communication and updates | Not asking for help; unclear allocation of responsibility | More agenda meetings; keep GitHub Kanban board current |
| Joe | Completing tasks and communicating questions/concerns | Not prioritizing must-haves | Keep documentation up to date |
| Chris | Communicating effectively | Doubting ourselves | Manage feature creep |

### Sprint 5

| | Continue | Stop | Start |
|---|---|---|---|
| Joe | Completing group work in a timely manner | Pushing off documentation while implementing features | Shift focus toward UI look and feel, not just functionality |

---

## Budget

| Item | Cost |
|---|---|
| Raspberry Pi 4 | $100.00 |
| LCD Display | $15.00 |
| GPIO-to-UART USB Board | $15.00 |
| Fingerprint Scanner (AS608) | $20.00 |
| **Hardware Total** | **$150.00** |

**Labor (estimated for academic exercise):**

| Role | Rate |
|---|---|
| Junior Systems Engineer | $30/hr |
| Junior Software Developer | $36/hr |
| IT Project Manager | $58/hr |

- Hours per week: 3
- Multiplier: 2×
- **Estimated total project cost (hardware + labor): ~$38,838**

---

## Configuration Management

- **Version control:** Git / GitHub
- **Branching:** Feature branches merged to `main` via pull request
- **Issue tracking:** GitHub Projects Kanban board
- **Environment:** Credentials stored in `.env`, never committed
- **Dependencies:** Pinned in `requirements.txt`
