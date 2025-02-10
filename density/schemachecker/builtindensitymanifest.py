# density/schemachecker/builtindensitymanifest.py


BUILTIN_DENSITY_MANIFEST = {
    "norm": {"loc", "scale"},  # For scipy.stats.norm convention replication
    "lognorm": {"s", "loc", "scale"},
    "expon": {"loc", "scale"},
    "t": {"df", "loc", "scale"},
    "weibull_min": {"c", "loc", "scale"},
    "gamma": {"a", "loc", "scale"},
    "weibull_max": {"c", "loc", "scale"},
    "beta": {"a", "b", "loc", "scale"},
    "chi": {"df", "loc", "scale"},
    "chi2": {"df", "loc", "scale"},
    "rayleigh": {"loc", "scale"},
    "pareto": {"b", "loc", "scale"},
    "cauchy": {"loc", "scale"},
    "laplace": {"loc", "scale"},
    "f": {"dfn", "dfd", "loc", "scale"},
}
