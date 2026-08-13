"""Core analysis contracts for Neuro Signal Lab."""

from .analysis import P3Summary, p3_contrast, summarize_contrasts, window_mean
from .metadata import RunAudit, audit_event_file, load_frozen_audit, pz_is_eeg_channel

__all__ = [
    "P3Summary",
    "RunAudit",
    "audit_event_file",
    "load_frozen_audit",
    "p3_contrast",
    "pz_is_eeg_channel",
    "summarize_contrasts",
    "window_mean",
]
