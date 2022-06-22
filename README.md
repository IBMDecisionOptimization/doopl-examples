# IBM&reg; OPL connector for Python (DOopl)

Welcome to the IBM&reg; OPL connector for Python.
Licensed under the Apache License v2.0.

With this library, you can quickly and easily add the power of optimization to
your Python application. You can model your problems by using the OPL language and IDE, and integrate it in Python via Python/pandas/sql alchemy inputs/outputs.

Solving with CPLEX requires that IBM&reg; ILOG CPLEX Optimization Studio is installed on your machine.
Currently, `doopl` supports CPLEX Optimization Studio versions:
- 12.8
- 12.9
- 12.10

We provide the library for python 3.6 and 3.7.

This library is an example showing how to use data sources in python in OPL.
It is provided "as-is".

We don't plan to provide the library as a standard Python package anymore: the connector source code is now on the IBM public github.
If you need a more recent version of optimization engine and/or if you need a more recent Python version, you can have a look at the [code](https://github.com/IBMDecisionOptimization/doopl) and refer to the README for build instructions.

## Install the library

```
   pip install doopl
```

## Get the examples

* [Examples](https://github.com/IBMDecisionOptimization/doopl-examples)

## Get your IBM&reg; ILOG CPLEX Optimization Studio edition

- You can get a free [Community Edition](http://www-01.ibm.com/software/websphere/products/optimization/cplex-studio-community-edition)
 of CPLEX Optimization Studio, with limited solving capabilities in term of problem size.

- Faculty members, research professionals at accredited institutions can get access to an unlimited version of CPLEX through the
 [IBM&reg; Academic Initiative](https://ibm.onthehub.com/WebStore/ProductSearchOfferingList.aspx?srch=cplex).

## License

This library is delivered under the  Apache License Version 2.0, January 2004 (see [LICENSE](LICENSE.txt)).

## Starting point

The API is very compact and simple.
You must have the OPL binaries in your PATH/LD_LIBRARY_PATH or DYLD_LIBRARY_PATH, depending on your platform.
They are located in <code>&lt;cplex_studio_dir&gt;/opl/bin/&lt;platform&gt;</code> where
   * cplex_studio_dir is the installation directory of CPLEX Optimization Studio
   * platform is your plaform.

Here is small sumup of the capabilities:
   * Inputs can be tuple lists, panda's dataframe, sql alchemy fetch statements.
   * Generate, solve and get output tuplesets as panda's dataframe
   * Get the CPLEX problem statistics and quality metrics for the solution
   * Convert all integer variables to floating point variables and vice-versa.
   * Run the conflict/relaxation mechanism.
   * Call the 'RunSeed' diagnosis for CPLEX/CPO based problems.

Each of these features are demonstrated with simple examples.

Here is a small example to start working with the API:

    from doopl.factory import *

    # Create an OPL model from a .mod file
    with create_opl_model(model="file.mod") as opl:
        # tuple can be a list of tuples, a pandas dataframe...
        opl.set_input("TupleSet1", tuples)

        # Generate the problem and solve it.
        opl.run()

        # Get the names of post processing tables
        print("Table names are: "+ str(opl.output_table_names))

        # Get all the post processing tables as dataframes.
        for name, table in iteritems(opl.report):
            print("Table : " + name)
            for t in table.itertuples(index=False):
                print(t)
