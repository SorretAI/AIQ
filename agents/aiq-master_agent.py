#!/usr/bin/env python3
# aiq_master_agent.py
# Master skeleton for AIQueue-style multi-agent orchestrator with backward planning.

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Callable
import uuid
import time

# ==========================
# === BEGIN: ENUMS & TYPES
# ==========================

class TaskTrack(Enum):
    ON_TARGET = "on_target"            # To be worked ASAP
    DELEGATION_STATION = "delegation"  # To other agents or humans-in-loop
    BACK_BURNER = "back_burner"        # Future / blocked / pending resources

class TaskStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    BLOCKED = auto()
    DONE = auto()
    FAILED = auto()

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    track: TaskTrack = TaskTrack.BACK_BURNER
    status: TaskStatus = TaskStatus.PENDING
    depends_on: List[str] = field(default_factory=list)    # other task IDs
    assignee: Optional[str] = None                         # agent/human
    metadata: Dict = field(default_factory=dict)

# ========================
# === END: ENUMS & TYPES
# ========================


# ======================================
# === BEGIN: SIMPLE EVENT / LOGGING BUS
# ======================================

def log(msg: str):
    print(f"[AIQ] {time.strftime('%H:%M:%S')}  {msg}")

# ====================================
# === END: SIMPLE EVENT / LOGGING BUS
# ====================================


# =========================================================
# === BEGIN: AGENT INTERFACES (Base + Example Sub-Agents)
# =========================================================

class BaseAgent:
    """All agents should subclass this. Keep it tiny and predictable."""
    def __init__(self, name: str):
        self.name = name

    def can_handle(self, task: Task) -> bool:
        """Override: basic capability filter."""
        return False

    def handle(self, task: Task) -> TaskStatus:
        """Override: do work and return TaskStatus."""
        raise NotImplementedError

# --- Example agent #1
class ResearchAgent(BaseAgent):
    def can_handle(self, task: Task) -> bool:
        return "research" in task.title.lower() or task.metadata.get("type") == "research"

    def handle(self, task: Task) -> TaskStatus:
        log(f"{self.name} researching: {task.title}")
        # pretend to do stuff...
        time.sleep(0.1)
        task.metadata["brief"] = "short background brief generated"
        return TaskStatus.DONE

# --- Example agent #2
class ContentAgent(BaseAgent):
    def can_handle(self, task: Task) -> bool:
        return "content" in task.title.lower() or task.metadata.get("type") == "content"

    def handle(self, task: Task) -> TaskStatus:
        log(f"{self.name} creating content: {task.title}")
        time.sleep(0.1)
        task.metadata["asset_url"] = "s3://bucket/asset.mp4"
        return TaskStatus.DONE

# =======================================================
# === END: AGENT INTERFACES (Base + Example Sub-Agents)
# =======================================================


# =====================================
# === BEGIN: AGENT FACTORY (SPAWNING)
# =====================================

class AgentFactory:
    """
    Spawns agents on-demand. Extend the registry below.
    """

    # ---- EDIT HERE LATER -----------------------------------------
    # === BEGIN EDIT BLOCK: AGENT REGISTRY
    _registry: Dict[str, Callable[[str], BaseAgent]] = {
        "research": lambda n: ResearchAgent(n),
        "content":  lambda n: ContentAgent(n),
        # Add more like: "video_edit": lambda n: VideoEditAgent(n),
    }
    # === END EDIT BLOCK: AGENT REGISTRY
    # --------------------------------------------------------------

    @classmethod
    def spawn(cls, capability: str, name_suffix: str = "") -> BaseAgent:
        maker = cls._registry.get(capability)
        if not maker:
            raise ValueError(f"No agent registered for capability: {capability}")
        name = f"{capability}_agent{name_suffix and '_' + name_suffix}"
        log(f"Spawning agent: {name}")
        return maker(name)

# ===================================
# === END: AGENT FACTORY (SPAWNING)
# ===================================


# ======================================
# === BEGIN: BACKWARD PLANNING ENGINE
# ======================================

class BackwardPlanner:
    """
    Very small backward planner:
    - Start from a high-level goal.
    - Decompose into milestones (user-extensible).
    - Expand milestones into atomic tasks (user-extensible).
    """

    # ---- EDIT HERE LATER -----------------------------------------
    # === BEGIN EDIT BLOCK: DECOMPOSITION RULES
    @staticmethod
    def decompose_goal(goal: str) -> List[str]:
        """
        Return ordered milestones from end-state backwards.
        """
        # Example for content pipeline—customize per project:
        # 3 -> 2 -> 1 (backward), but we will schedule forward after creation.
        return [
            "Publish asset",
            "Produce final asset",
            "Research & outline",
        ]

    @staticmethod
    def expand_milestone(milestone: str, goal: str) -> List[Task]:
        """
        Translate a milestone into atomic tasks with metadata.
        """
        if milestone == "Publish asset":
            return [
                Task(id=str(uuid.uuid4()), title="Content: Write title/description",
                     track=TaskTrack.ON_TARGET, metadata={"type": "content"}),
                Task(id=str(uuid.uuid4()), title="Content: Schedule publishing",
                     track=TaskTrack.DELEGATION_STATION, metadata={"type": "content"}),
            ]
        if milestone == "Produce final asset":
            return [
                Task(id=str(uuid.uuid4()), title="Content: Edit draft into final",
                     track=TaskTrack.ON_TARGET, metadata={"type": "content"}),
            ]
        if milestone == "Research & outline":
            return [
                Task(id=str(uuid.uuid4()), title="Research: Background brief",
                     track=TaskTrack.ON_TARGET, metadata={"type": "research"}),
                Task(id=str(uuid.uuid4()), title="Content: Create outline",
                     track=TaskTrack.DELEGATION_STATION, metadata={"type": "content"}),
            ]
        # Default fallback goes to BackBurner so nothing is lost.
        return [Task(id=str(uuid.uuid4()), title=f"Unmapped milestone: {milestone}",
                     track=TaskTrack.BACK_BURNER)]
    # === END EDIT BLOCK: DECOMPOSITION RULES
    # --------------------------------------------------------------

    def plan(self, goal: str) -> List[Task]:
        """
        Produce a forward-executable task list by:
          1) decomposing backward
          2) expanding to tasks
          3) stitching dependencies so earlier milestones unblock later ones
        """
        milestones = self.decompose_goal(goal)        # backward list
        all_tasks: List[Task] = []
        last_batch_ids: List[str] = []

        for milestone in reversed(milestones):  # switch to forward creation
            batch = self.expand_milestone(milestone, goal)
            # chain dependencies: everything in this batch depends on last batch completion
            for t in batch:
                t.depends_on.extend(last_batch_ids)
            all_tasks.extend(batch)
            last_batch_ids = [t.id for t in batch]

        return all_tasks

# ====================================
# === END: BACKWARD PLANNING ENGINE
# ====================================


# =================================
# === BEGIN: TASK MANAGER (3-TRACK)
# =================================

class TaskManager:
    """
    Holds and routes tasks among the three stations.
    """

    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    # CRUD
    def add_tasks(self, tasks: List[Task]):
        for t in tasks:
            self.tasks[t.id] = t
            log(f"Task added [{t.track.name}]: {t.title} ({t.id[:8]})")

    # Moves
    def move(self, task_id: str, new_track: TaskTrack):
        t = self.tasks[task_id]
        log(f"Move task {t.id[:8]} -> {new_track.name}")
        t.track = new_track

    def set_status(self, task_id: str, status: TaskStatus):
        t = self.tasks[task_id]
        t.status = status

    # Queries
    def ready_for_execution(self) -> List[Task]:
        """
        Return ON_TARGET tasks with dependencies satisfied and pending.
        """
        def deps_done(task: Task) -> bool:
            return all(self.tasks[d].status == TaskStatus.DONE for d in task.depends_on)

        return [
            t for t in self.tasks.values()
            if t.track == TaskTrack.ON_TARGET and t.status == TaskStatus.PENDING and deps_done(t)
        ]

    def needs_delegation(self) -> List[Task]:
        return [
            t for t in self.tasks.values()
            if t.track == TaskTrack.DELEGATION_STATION and t.status == TaskStatus.PENDING
        ]

    def backlog(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.track == TaskTrack.BACK_BURNER]

# ===============================
# === END: TASK MANAGER (3-TRACK)
# ===============================


# ======================================
# === BEGIN: MASTER ORCHESTRATOR (AIQ)
# ======================================

class MasterAgent:
    """
    The conductor:
    - Accepts a goal
    - Builds a backward plan
    - Fills three stations
    - Spawns sub-agents to execute ON_TARGET/DELEGATION tasks
    - Escalates to humans as needed (placeholder hook)
    """

    def __init__(self):
        self.tm = TaskManager()
        self.planner = BackwardPlanner()
        # Keep a tiny pool of spawned agents by capability
        self.agent_pool: Dict[str, List[BaseAgent]] = {}

    # ---- EDIT HERE LATER -----------------------------------------
    # === BEGIN EDIT BLOCK: CAPABILITY RESOLUTION
    def resolve_capability(self, task: Task) -> Optional[str]:
        """
        Map a task to a capability string used by AgentFactory.
        Extend this as you add agents/types.
        """
        return task.metadata.get("type")  # e.g., "research", "content"
    # === END EDIT BLOCK: CAPABILITY RESOLUTION
    # --------------------------------------------------------------

    def ensure_agent(self, capability: str) -> BaseAgent:
        pool = self.agent_pool.setdefault(capability, [])
        if pool:
            return pool[0]  # reuse first for simplicity
        agent = AgentFactory.spawn(capability, name_suffix="pool0")
        pool.append(agent)
        return agent

    def ingest_goal(self, goal: str):
        log(f"Received GOAL: {goal}")
        tasks = self.planner.plan(goal)
        self.tm.add_tasks(tasks)

    def step(self):
        """
        One orchestration 'tick'. Call repeatedly from a loop / scheduler.
        """
        # 1) Execute ON_TARGET tasks with satisfied deps
        for t in self.tm.ready_for_execution():
            cap = self.resolve_capability(t)
            if not cap:
                log(f"No capability for task {t.title} → parking to Delegation Station")
                t.track = TaskTrack.DELEGATION_STATION
                continue

            agent = self.ensure_agent(cap)
            log(f"Dispatching to {agent.name}: {t.title}")
            self.tm.set_status(t.id, TaskStatus.IN_PROGRESS)
            try:
                status = agent.handle(t)
                self.tm.set_status(t.id, status)
                log(f"Task {t.id[:8]} → {status.name}")
            except Exception as e:
                log(f"ERROR in agent {agent.name}: {e}")
                self.tm.set_status(t.id, TaskStatus.FAILED)
                # On failure, you might move it to DelegationStation or BackBurner:
                self.tm.move(t.id, TaskTrack.DELEGATION_STATION)

        # 2) Route DELEGATION_STATION tasks
        for t in self.tm.needs_delegation():
            # --- Human-in-the-loop hook (replace with notifier) ---
            log(f"Delegation needed: {t.title} ({t.id[:8]}) → notify human or spawn specialized agent")
            # Example: attempt another capability guess or leave for human:
            cap = self.resolve_capability(t)
            if cap:
                agent = self.ensure_agent(cap)
                log(f"Re-dispatching delegated task to {agent.name}: {t.title}")
                self.tm.set_status(t.id, TaskStatus.IN_PROGRESS)
                try:
                    status = agent.handle(t)
                    self.tm.set_status(t.id, status)
                except Exception as e:
                    log(f"ERROR (delegation) {agent.name}: {e}")
                    self.tm.set_status(t.id, TaskStatus.FAILED)

        # 3) Backlog stays as is (BackBurner); you can surface periodically.

    # Utility
    def summary(self) -> Dict[str, int]:
        counts = {"on_target": 0, "delegation": 0, "back_burner": 0,
                  "pending": 0, "in_progress": 0, "done": 0, "failed": 0}
        for t in self.tm.tasks.values():
            counts[t.track.value] += 1
            if t.status == TaskStatus.PENDING: counts["pending"] += 1
            if t.status == TaskStatus.IN_PROGRESS: counts["in_progress"] += 1
            if t.status == TaskStatus.DONE: counts["done"] += 1
            if t.status == TaskStatus.FAILED: counts["failed"] += 1
        return counts

# ====================================
# === END: MASTER ORCHESTRATOR (AIQ)
# ====================================


# =====================================
# === BEGIN: DEMO MAIN (SAFE TO KEEP)
# =====================================

if __name__ == "__main__":
    """
    Quick smoke test:
    - Define a goal
    - Build plan (backward -> forward)
    - Tick the orchestrator a few times
    - Print summary
    """
    goal_text = "Publish a branded short-form video explaining AIQueue"
    master = MasterAgent()
    master.ingest_goal(goal_text)

    for _ in range(5):
        master.step()

    log(f"Summary: {master.summary()}")
# ===================================
# === END: DEMO MAIN (SAFE TO KEEP)
# ===================================

