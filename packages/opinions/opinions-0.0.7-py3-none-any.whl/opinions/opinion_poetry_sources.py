from opinions import Opinion


class PoetryExplicitSourcesOpinion(Opinion):
    def apply_changes(self):
        sources = self.project.pyproject.content.get("tool", {}).get("poetry", {}).get("source", [])
        if not sources:
            return

        for source in sources:
            if "secondary" in source:
                if source["secondary"]:
                    source["priority"] = "supplemental"
                del source["secondary"]

        if not any([x["name"].lower() == "pypi" for x in sources]) and not any(
            [x.get("priority", "default") == "default" for x in sources]
        ):
            sources.append({"name": "pypi", "priority": "default"})
