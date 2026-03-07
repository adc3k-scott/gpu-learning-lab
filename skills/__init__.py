"""
Skills package — plugin system for Mission Control agents.

Import the registry to discover and access skills:
    from skills.registry import registry
    skill = registry.get("file_manager")
    result = await skill.execute(ctx, params)
"""

from skills.registry import SkillRegistry

__all__ = ["SkillRegistry"]
