

# Manually evaluate

if __name__ == "__main__":

    try:
        import scipy.stats as st
    except ImportError:
        print("Please install scipy to run this example")
        raise

    # suppose we have a scipy spec:
    spec = {
        "type": "scipy",
        "name": "norm",
        "params": {"loc": 0, "scale": 1}
    }

    dist_class = getattr(st, spec['name'])
    dist = dist_class(**spec['params'])
    pdf_value = dist.pdf(0)
