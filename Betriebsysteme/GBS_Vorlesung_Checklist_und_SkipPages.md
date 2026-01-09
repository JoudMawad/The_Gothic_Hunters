# GBS — Exam Checklist (bound to **V_GBS.pdf** pages)

**How to use this file**
- The page numbers below refer to the **PDF page index** of `V_GBS.pdf` (1–939), i.e. the number you see in the PDF viewer.
- For each checklist item: read the referenced pages, then **solve at least 1 old-exam task** on that topic.

---

## 1) Fast navigation map (what lives where)

### Parts / chapters in `V_GBS.pdf`
- **Teil A (Einführung)**: p. **1–252**
  - 1 Einführung und Organisation: p. **5–88** fileciteturn7file0
  - 2 Exkurs: Systemnahe C-Programmierung: p. **89–182** fileciteturn7file0
  - 3 Grundlegende Konzepte: p. **183–251** fileciteturn6file0
- **Teil B (Prozesse und Dateien)**: p. **252–546** fileciteturn5file0
  - 4 Dateien und Dateisysteme: p. **253–328** fileciteturn5file0
  - 5 Prozesse und Fäden: p. **329–398** fileciteturn5file0
  - 6 Unterbrechungen, Ausnahmen, Signale: p. **399–460** fileciteturn7file0
  - 7 Prozessverwaltung: p. **461–546** fileciteturn6file0
- **Teil C (Interaktion und Kommunikation)**: p. **546–784** fileciteturn5file0
  - 8 Speicherbasierte Interaktionen: p. **548–628** fileciteturn6file0
  - 9 Synchronisation und Verklemmung: p. **629–725** fileciteturn5file0
  - 10 Interprozesskommunikation (IPC): p. **726–784** fileciteturn5file0
- **Teil D (Speicher und Zugriffsschutz)**: p. **784–934** fileciteturn4file0
  - 11 Speicherorganisation: p. **786–863** fileciteturn6file0
  - 12 Speichervirtualisierung: p. **864–934** fileciteturn6file0
- **Anhang / Referenzen**: p. **935–939** fileciteturn6file0

---

## 2) Pages you can skip (or only skim)

### A) “Safe skip” (almost never exam-critical)
- **p. 1–3**: cover/metadata.
- **p. 61–84**: literature lists + course organization/semester plan/workload (administrative). fileciteturn6file0
- **p. 935–939**: references/appendix. fileciteturn6file0

### B) “Skim only” (skip if time is tight)
- **Motivation / quotes slides**: **p. 47–53, 57–60** (context, not needed for problem solving).
- **Literature quotes about “what is an OS”**: **p. 36–37**.
- **Discussion / comparison slides** (helpful but low ROI for points):  
  - **p. 376–379** (fork/exec discussion),  
  - **p. 559–560, 577–578, 580–581, 594–596** (design discussions around sync/threads).

### C) “Conditional skip”
- **Chapter 2 (C programming), p. 89–182**:  
  Skip *only if* you can already read/trace C with pointers, arrays/strings, structs, function pointers, bit ops, and understand typical `errno`/return value patterns.  
  Otherwise, do it (it’s needed for interpreting exam code snippets).

---

## 3) Exam-oriented checklist (with pages)

### 4 Dateien und Dateisysteme (p. 253–328)
**Goal:** be able to reason about file descriptors, open file tables, directory traversal, and typical file syscalls.

- [ ] Understand **file descriptors** (per-process) vs **open-file objects** (system-wide) and why `dup/dup2` matter.  
  Read: **p. 311–313** (fd-table / open file table / vnode diagram). fileciteturn8file0
- [ ] Know the lifecycle: `open/creat → read/write → close` (return values, what happens on error).  
  Read: **p. 307–311**.
- [ ] Be able to do simple **I/O redirection reasoning** (what happens to stdin/stdout after `dup2`).  
  Read: **p. 309–311**.
- [ ] Directory traversal basics (`opendir`, `readdir`, `closedir`) and what a directory entry contains.  
  Read: **p. 305**.  
  (Old exams often include the `readdir` struct and file types.)

**Typical exam skills**
- trace which fd points where after a sequence of `open/close/dup2`;
- decide which files are shared after `fork` and which not.

---

### 5 Prozesse und Fäden (p. 329–398)
**Goal:** be able to trace process creation and the fork/exec/wait pattern (this appears repeatedly in old exams).

- [ ] **Process primitives**: `fork`, `exit`, `kill`, `wait` — semantics and return values; zombies/orphans.  
  Read: **p. 371–372** (overview + fork/wait example). fileciteturn8file10
- [ ] **exec family**: what changes (program image) vs what stays (PID, open fds unless close-on-exec).  
  Read: **p. 373–376** (exec + mini-shell example). fileciteturn8file6
- [ ] Be able to **trace a fork/exec program**: which lines run in parent vs child; when/why parent blocks in `wait`.  
  Read: **p. 371–379**.

**Typical exam skills**
- fill missing lines in a fork/exec/pipe program;
- reason about which output is printed by parent/child.

---

### 6 Unterbrechungen, Ausnahmen, Signale (p. 399–460)
**Goal:** understand the event model and how signals behave in user-space programs.

- [ ] Distinguish **interrupt vs exception vs system call** (sync/async; who triggers it).  
  Read: **p. 399–410**.
- [ ] Signal basics: delivery, default actions, masks, handler installation.  
  Read: **p. 420–446**.
- [ ] Know `sigaction` at a conceptual level (handler pointer, default/ignore).  
  Read: **p. 438**.

**Typical exam skills**
- explain what happens if a blocking call is interrupted by a signal (EINTR);
- identify safe/unsafe operations in a signal handler (conceptually).

---

### 7 Prozessverwaltung (p. 461–546)
**Goal:** scheduling + process states + context switching reasoning.

- [ ] Process states and transitions; what a context switch saves/restores.  
  Read: **p. 461–480**.
- [ ] Scheduling policies: FCFS, Round Robin, priorities; understand trade-offs and fairness.  
  Read: **p. 488–495** and **p. 531–542** (RR/priority clusters).
- [ ] Be able to compute simple scheduling outcomes if asked (who runs next / waiting time trends).  
  Read: **p. 488–495**.

---

### 8 Speicherbasierte Interaktionen (p. 548–628)
**Goal:** threads + shared memory + critical sections + classical synchronization tools.

- [ ] Thread model: what is shared vs private (stacks/registers vs address space).  
  Read: **p. 548–562**.
- [ ] Mutual exclusion: why we need it; basic primitives (mutex/spinlock/atomic).  
  Read: **p. 562–587**.
- [ ] Higher-level patterns: producer/consumer, condition synchronization.  
  Read: **p. 593–596, 611–622**.

**Typical exam skills**
- complete code that protects a shared variable correctly (mutex + condition or semaphore);
- detect a race condition from a short code snippet.

---

### 9 Betriebsmittelverwaltung, Synchronisation und Verklemmung (p. 629–725)
**Goal:** deadlock reasoning (Coffman conditions), avoidance/prevention ideas, standard examples.

- [ ] Deadlock definition and the **four Coffman conditions**; be able to apply them to a scenario.  
  Read: **p. 640–660** (concept block) and then the examples.
- [ ] Dining philosophers and what changes break deadlock (trade-offs).  
  Read: **p. 684–686**. fileciteturn8file16
- [ ] Understand common mistakes: “fixing” deadlock by serializing too much (bad utilization).  
  Read: **p. 685–686**.

**Typical exam skills**
- decide if deadlock is possible and justify with conditions;
- propose one improvement and state what condition it breaks.

---

### 10 Interprozesskommunikation (IPC) (p. 726–784)
**Goal:** pipes and process composition (very frequent in exams), plus basic IPC variants.

- [ ] Pipes: `pipe → fork → close unused ends → dup2 → exec`.  
  Read: **p. 770–772** (connect example).
- [ ] Be able to reason about pipe deadlocks (both sides waiting) and EOF behavior (closing write end).  
  Read: **p. 770–774**.
- [ ] Know where sockets appear in the script (high level, as needed).  
  Read: **p. 742, 779–781**.

---

### 11 Speicherorganisation (p. 786–863)
**Goal:** memory layout and dynamic allocation reasoning.

- [ ] Process memory layout (code/data/heap/stack) and what grows where.  
  Read: **p. 786–798**.
- [ ] `malloc/free` conceptual model + fragmentation; typical allocator ideas.  
  Read: **p. 798–805**.
- [ ] `mmap` (only conceptually: mapping regions / file-backed memory).  
  Read: **p. 831**.

---

### 12 Speichervirtualisierung (p. 864–934)
**Goal:** address translation computations + page faults + swapping (this is classic exam material).

- [ ] Paging translation: page number + offset, page table lookup, physical address construction.  
  Read: **p. 897–910**.
- [ ] Page faults: what triggers them and the high-level handling path.  
  Read: **p. 897–910** (fault intro) and **p. 908–910**.
- [ ] TLB: why it exists and what it caches.  
  Read: **p. 885–886, 890**.
- [ ] Segmentation vs paging: pros/cons and typical failure modes.  
  Read: **p. 867–879, 889–893, 904–907**.
- [ ] Swapping / backing store: what happens when a page is not in RAM.  
  Read: **p. 919–927**.

**Typical exam skills**
- compute page size, page table size, max virtual address space given bit splits (like older exams);
- describe page-fault handling in bullet points.

---

## 4) Minimal weekly plan (works even with a big script)

Repeat this cycle until the exam:

1) **1 chapter/day** (or half-chapter/day): read only the pages referenced in the checklist.  
2) Do **one old-exam task** on that chapter immediately after.  
3) Write a 1-page “mistakes list” (your personal bug tracker): every wrong assumption goes there.

Priority order (highest → lowest):
1. Ch. **5, 4, 10** (fork/exec/pipe + fds)  
2. Ch. **8, 9** (sync + deadlocks)  
3. Ch. **12** (virtual memory computations)  
4. Ch. **6, 7, 11**  
5. Ch. **1–3** (only what you need to support the above)

