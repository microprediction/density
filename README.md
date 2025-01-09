# Density ![tests_312](https://github.com/microprediction/density/workflows/tests_312/badge.svg)
A simple `dict` specification of an algebra of continuous univariate density function mixtures using `pydantic`. 

## Install

   pip install density 
   
## Specifying densities or mixtures of the same
See [examples](https://github.com/microprediction/density/tree/main/examples) of specifying densities. 

See the [Scipy manifest](https://github.com/microprediction/density/blob/main/density/schemachecker/scipydensitymanifest.py) for a list of densities. 

## Evaluating densities 
The current use case involves evaluation of a single data point at a time. For this we recommend using the `builtin` option rather than `scipy`, and using [https://github.com/microprediction/density](https://github.com/microprediction/densitypdf) package. 


      from densitypdf import density_pdf
      
      mixture_spec = {
          "type": "mixture",
          "components": [
              {
                  "density": {
                      "type": "scipy",
                      "name": "norm",
                      "params": {"loc": 0, "scale": 1}
                  },
                  "weight": 0.6
              },
              {
                  "density": {
                      "type": "builtin",
                      "name": "norm",
                      "params": {"loc": 2.0, "scale": 1.0}
                  },
                  "weight": 0.4
              }
          ]
      }
      
      val = density_pdf(mixture_spec, x=0.0)


You can also evaluate manually of course, per examples [here](https://github.com/microprediction/density/tree/main/examples/evaluation). 


