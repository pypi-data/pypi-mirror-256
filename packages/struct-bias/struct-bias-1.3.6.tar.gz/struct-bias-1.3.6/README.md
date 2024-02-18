# Deep-BIAS: Bias In Algorithms, Structural
## A toolbox for detecting structural bias in continuous optimization heuristics.
## With a deep-learning extension to better evaluate the type of bias and gain insights using explainable AI

## Setup

This package requires an R-installation to be present.

The package is tested with R 4.1.2 (install from source https://cran.r-project.org/src/base/R-4/R-4.1.2.tar.gz)

The R packages will be installed automatically upon first importing BIAS.

Install the BIAS toolbox using pip:

    pip install struct-bias

This installs the following R packages:

- PoweR
- AutoSEARCH
- nortest
- data.table
- goftest
- ddst


### Detailed setup using virtual env

1. Download and install R from https://cran.r-project.org/ use version 4.1.2  
   Example for Ubuntu based system:
    ```sh
    sudo wget https://cran.rstudio.com/src/base/R-4/R-4.1.2.tar.gz  
    tar zxvf R-4.1.2.tar.gz  
    cd R-4.1.2  
    ./configure --enable-R-shlib  
    make  
    sudo make install  
    ```
    
2. Download this repository (clone or as zip)
3. Create a python virtual env `python -m venv env`
4. Activate the env (in powershell for example: `env/Scripts/Activate.ps1 `)
5. Install dependencies `pip install -r requirements.txt`
6. Checkout the `example.py` to start using the BIAS toolbox.


## Example

```py
#example of using the BIAS toolbox to test a DE algorithm

from scipy.optimize import differential_evolution
import numpy as np
from BIAS import BIAS, f0

bounds = [(0,1), (0, 1), (0, 1), (0, 1), (0, 1)]

#do 30 independent runs (5 dimensions)
samples = []
print("Performing optimization method 30 times of f0.")
for i in np.arange(30):
    result = differential_evolution(f0, bounds, maxiter=100)
    samples.append(result.x)

samples = np.array(samples)

test = BIAS()
print(test.predict(samples, show_figure=True))

y, preds = test.predict_deep(samples)
test.explain(samples, preds, filename="explanation.png")
```

## Additional files

Note: The code for generating the RF used to predict the type of bias is included, but the full RF is not. These can be found on zenodo: https://doi.org/10.6084/m9.figshare.16546041.
The RF models will be downloaded automatically the first time the predict function requires them.

### Citation

If you use the BIAS toolbox in a scientific publication, we would appreciate using the following citations:

```
@ARTICLE{9828803,
  author={Vermetten, Diederick and van Stein, Bas and Caraffini, Fabio and Minku, Leandro L. and Kononova, Anna V.},
  journal={IEEE Transactions on Evolutionary Computation}, 
  title={BIAS: A Toolbox for Benchmarking Structural Bias in the Continuous Domain}, 
  year={2022},
  volume={26},
  number={6},
  pages={1380-1393},
  doi={10.1109/TEVC.2022.3189848}
}

@software{niki_van_stein_2023_7803623,
  author       = {Niki van Stein and
                  Diederick Vermetten},
  title        = {Basvanstein/BIAS: v1.1 Deep-BIAS Toolbox},
  month        = apr,
  year         = 2023,
  publisher    = {Zenodo},
  version      = {v1.1},
  doi          = {10.5281/zenodo.7803623},
  url          = {https://doi.org/10.5281/zenodo.7803623}
}
```
