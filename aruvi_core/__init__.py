"""aruvi_core — the lifted Aruvi generation engine (UI-free, vendor-neutral).

Public surface:
- view model:   ViewModel, LessonPlanView, AssessmentView, Group, Period,
                AssessmentGroup, AssessmentItem, VisualStimulus, StimulusType
- subjects:     register / get / available  (the plugin registry)
- ports:        LLMClient, OutputCache, Storage, Repository, JobQueue,
                AuthProvider, BillingProvider, Prompt, LLMResponse
- engine:       generate(...)
"""
from __future__ import annotations

from . import engine, ports, subjects
from .view_model import (
    AssessmentGroup,
    AssessmentItem,
    AssessmentView,
    Group,
    LessonPlanView,
    Period,
    StimulusType,
    ViewModel,
    VisualStimulus,
)

__all__ = [
    "engine", "ports", "subjects",
    "ViewModel", "LessonPlanView", "AssessmentView", "Group", "Period",
    "AssessmentGroup", "AssessmentItem", "VisualStimulus", "StimulusType",
]
