import scipy.stats as st

# A mapping of "dist_name" strings to the corresponding scipy.stats class.
# You can expand this dictionary to include more distributions (Gamma, Beta, etc.)
SCIPY_DISTS = {
    "norm": st.norm,  # Normal(loc=..., scale=...)
    "t": st.t,  # Student's t(df=..., loc=..., scale=...)
    "weibull_min": st.weibull_min,  # Weibull(c=..., loc=..., scale=...)
    "lognorm": st.lognorm,
    "expon": st.expon,
    # Add more as you wish
}


class UnivariateDensity:
    """
    A simple container for a univariate distribution from scipy.stats.

    Attributes
    ----------
    dist_name : str
        The name of the distribution (must be a key in SCIPY_DISTS).
    params : dict
        The parameters needed by the scipy.stats distribution (e.g., 'loc', 'scale', 'df', 'c', etc.).

    Examples
    --------
    # Create a normal distribution with mean=0, std=1
    dist = Distribution(dist_name="norm", loc=0, scale=1)

    # Evaluate PDF at x=2.0
    val = dist.pdf(2.0)

    # Serialize to dict
    d = dist.to_dict()
    # d -> { "dist_name": "norm", "params": {"loc": 0, "scale": 1} }

    # Deserialize back
    dist2 = Distribution.from_dict(d)
    dist2.pdf(2.0)  # same as val
    """

    def __init__(self, dist_name: str, **params):
        if dist_name not in SCIPY_DISTS:
            raise ValueError(
                f"Unknown distribution name '{dist_name}'. "
                f"Available: {list(SCIPY_DISTS.keys())}"
            )

        self.dist_name = dist_name
        self.params = params

        # Create the underlying scipy.stats distribution object
        dist_class = SCIPY_DISTS[self.dist_name]
        self._scipy_dist = dist_class(**self.params)

    def pdf(self, x):
        """Compute the probability density function at x."""
        return self._scipy_dist.pdf(x)

    def cdf(self, x):
        """Optionally, you can also provide CDF or other methods."""
        return self._scipy_dist.cdf(x)

    def to_dict(self) -> dict:
        """
        Convert distribution into a dictionary representation.
        This can be easily converted to JSON or stored in a DB.
        """
        return {
            "dist_name": self.dist_name,
            "params": self.params
        }

    @staticmethod
    def from_dict(d: dict) -> "UnivariateDensity":
        """
        Create a Distribution from a dictionary with the format:
        {
            "dist_name": <str>,
            "params": <dict>
        }
        """
        dist_name = d["dist_name"]
        params = d["params"]
        return UnivariateDensity(dist_name, **params)
