# Pull your routing blueprints and schema validation objects together
from .router import router
from .schema import TriageAssessment, EmailDeliveryPreferences

# Define the public interface for the protocols package
__all__ = [
    "router",
    "TriageAssessment",
    "EmailDeliveryPreferences"
]