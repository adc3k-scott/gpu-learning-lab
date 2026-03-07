"""
Skill registry — discovers, validates, and manages skill plugins.

Auto-discovery searches:
  • skills/builtin/   — built-in skills shipped with Mission Control
  • skills/custom/    — user-defined skills (gitignored templates provided)

Usage:
    from skills.registry import registry

    # List available skills
    for meta in registry.list_all():
        print(meta["name"], meta["description"])

    # Execute a skill
    skill = registry.get("file_manager")
    result = await skill.execute(ctx, {"path": "/tmp/test.txt"})
"""

from __future__ import annotations

import importlib
import inspect
import logging
import pkgutil
from typing import Any

from skills.base import BaseSkill

logger = logging.getLogger(__name__)


class SkillRegistry:
    """
    Central registry for all Mission Control skills.

    Skills are discovered automatically from `skills.builtin` and
    `skills.custom` packages when `discover()` is called.  Individual
    skills can also be registered manually via `register()`.
    """

    def __init__(self) -> None:
        self._skills: dict[str, BaseSkill] = {}

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(self) -> None:
        """
        Scan builtin and custom skill packages and register every valid skill.
        Safe to call multiple times — already-registered skills are skipped.
        """
        for package_name in ("skills.builtin", "skills.custom"):
            self._discover_package(package_name)

    def _discover_package(self, package_name: str) -> None:
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            logger.debug("Skill package %r not found — skipping", package_name)
            return

        package_path = getattr(package, "__path__", [])
        for module_info in pkgutil.iter_modules(package_path):
            if module_info.name.startswith("_"):
                continue  # skip __init__, _template, etc.
            module_fqn = f"{package_name}.{module_info.name}"
            try:
                module = importlib.import_module(module_fqn)
                self._register_from_module(module)
            except Exception as exc:
                logger.warning("Failed to import skill module %r: %s", module_fqn, exc)

    def _register_from_module(self, module: Any) -> None:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BaseSkill)
                and obj is not BaseSkill
                and not inspect.isabstract(obj)
            ):
                try:
                    instance = obj()
                    self.register(instance)
                except Exception as exc:
                    logger.warning("Failed to instantiate skill %r: %s", obj, exc)

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, skill: BaseSkill, *, overwrite: bool = False) -> None:
        """
        Register a skill instance.

        Args:
            skill:     An instantiated BaseSkill subclass
            overwrite: Allow replacing an existing skill with the same name
        """
        if not self._validate(skill):
            return
        if skill.name in self._skills and not overwrite:
            logger.debug("Skill %r already registered — skipping", skill.name)
            return
        self._skills[skill.name] = skill
        logger.info("Registered skill: %s v%s", skill.name, skill.version)

    def unregister(self, name: str) -> None:
        skill = self._skills.pop(name, None)
        if skill:
            logger.info("Unregistered skill: %s", name)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> BaseSkill:
        """
        Return the skill with the given *name*.
        Raises KeyError if not found.
        """
        try:
            return self._skills[name]
        except KeyError:
            available = ", ".join(self._skills) or "(none)"
            raise KeyError(
                f"Skill {name!r} not found. Available: {available}"
            ) from None

    def list_all(self) -> list[dict[str, Any]]:
        """Return metadata dicts for every registered skill, sorted by name."""
        return sorted(
            [
                {
                    "name": s.name,
                    "description": s.description,
                    "version": s.version,
                    "required_secrets": s.required_secrets,
                }
                for s in self._skills.values()
            ],
            key=lambda d: d["name"],
        )

    def __len__(self) -> int:
        return len(self._skills)

    def __contains__(self, name: str) -> bool:
        return name in self._skills

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate(self, skill: BaseSkill) -> bool:
        if not skill.name:
            logger.warning("Skill %r has no name — skipping", type(skill).__name__)
            return False
        if not skill.description:
            logger.warning("Skill %r has no description — skipping", skill.name)
            return False
        return True


# ---------------------------------------------------------------------------
# Module-level singleton — import and use directly
# ---------------------------------------------------------------------------

registry = SkillRegistry()
registry.discover()
