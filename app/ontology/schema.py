"""
Ontology schema.

Defines the supported ontology types used by the Enterprise Knowledge
Assistant.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class EntityType:
    """
    Supported entity type.
    """

    name: str

    description: str


@dataclass(frozen=True, slots=True)
class RelationshipType:
    """
    Supported relationship type.
    """

    name: str

    description: str


ENTITY_TYPES: list[EntityType] = [

    EntityType(
        name="Person",
        description="Employee, manager or individual.",
    ),

    EntityType(
        name="Organization",
        description="Company or organization.",
    ),

    EntityType(
        name="Department",
        description="Business department.",
    ),

    EntityType(
        name="Team",
        description="Organizational team.",
    ),

    EntityType(
        name="Project",
        description="Business or technical project.",
    ),

    EntityType(
        name="Product",
        description="Enterprise product.",
    ),

    EntityType(
        name="Technology",
        description="Technology or framework.",
    ),

    EntityType(
        name="Application",
        description="Software application.",
    ),

    EntityType(
        name="Database",
        description="Database system.",
    ),

    EntityType(
        name="Policy",
        description="Enterprise policy.",
    ),

    EntityType(
        name="Document",
        description="Enterprise document.",
    ),

    EntityType(
        name="Location",
        description="Physical location.",
    ),
]


RELATIONSHIP_TYPES: list[RelationshipType] = [

    RelationshipType(
        name="BELONGS_TO",
        description="Entity belongs to another entity.",
    ),

    RelationshipType(
        name="PART_OF",
        description="Part of another entity.",
    ),

    RelationshipType(
        name="WORKS_IN",
        description="Person works in department.",
    ),

    RelationshipType(
        name="REPORTS_TO",
        description="Reporting hierarchy.",
    ),

    RelationshipType(
        name="MANAGES",
        description="Management relationship.",
    ),

    RelationshipType(
        name="USES",
        description="Uses technology or application.",
    ),

    RelationshipType(
        name="DEPENDS_ON",
        description="Dependency relationship.",
    ),

    RelationshipType(
        name="RELATED_TO",
        description="Generic relationship.",
    ),

    RelationshipType(
        name="LOCATED_IN",
        description="Location relationship.",
    ),

    RelationshipType(
        name="OWNS",
        description="Ownership relationship.",
    ),

    RelationshipType(
        name="CREATED_BY",
        description="Creator relationship.",
    ),
]


ENTITY_TYPE_MAP = {
    entity.name.lower(): entity
    for entity in ENTITY_TYPES
}

RELATIONSHIP_TYPE_MAP = {
    relationship.name.lower(): relationship
    for relationship in RELATIONSHIP_TYPES
}