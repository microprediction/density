
from density.univariatedensity import UnivariateDensity

if __name__=='__main__':

    # 1) Create a Normal distribution with mean=0, std=1
    dist1 = UnivariateDensity(dist_name="norm", loc=0, scale=1.0)

    # 2) Evaluate PDF at x=2
    val = dist1.pdf(2.0)
    print(f"PDF at x=2 for N(0,1) is: {val:.6f}")

    # 3) Serialize to dict
    d = dist1.to_dict()
    print("Dict format:", d)
    # e.g. {"dist_name": "norm", "params": {"loc": 0, "scale": 1.0}}

    # 4) Deserialize from dict
    dist2 = UnivariateDensity.from_dict(d)
    print("Same PDF value from dist2:", dist2.pdf(2.0))

    # 5) Create a Weibull distribution
    dist3 = UnivariateDensity(dist_name="weibull_min", c=1.5, scale=10.0)
    print("Weibull PDF at x=2:", dist3.pdf(2.0))


