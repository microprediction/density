# density/schemachecker/builtindensitymanifest.py

BUILTIN_DENSITY_MANIFEST = {
    # We only allow "normal"
    "normal": {"mu", "sigma"}, # For statistics.NormalDist convention replication
    "norm": {"loc", "scale"},  # For scipy.stats.norm convention replication
}

