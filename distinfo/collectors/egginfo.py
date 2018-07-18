from .collector import Collector


class EggInfo(Collector):

    MULTI_KEYS = (
        "classifier",
        "obsoletes",
        "obsoletes_dist",
        "platform",
        "project_url",
        "provides",
        "provides_dist",
        "provides_extra",
        "requires",
        "requires_dist",
        "requires_external",
        "supported_platform",
    )

    def _collect(self):
        source_dir = self.req.source_dir
        self.req.source_dir = "."
        self.req.run_egg_info()
        for key, value in self.req.pkg_info().items():
            value = value.strip()
            if not value or value == "UNKNOWN":
                continue
            key = key.lower().replace("-", "_")
            if key == "keywords":
                value = sorted(value.split())
            if key in self.MULTI_KEYS:
                self.dist.setdefault(key, set()).add(value)
            else:
                self.dist[key] = value
        self.req.source_dir = source_dir
