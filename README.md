# MyPy Hackery


:warning::warning::warning:

> **This repository is deprecated.**
> 
> The purpose of this repo was to conduct experiments for building a frontend for xDSL. 
> Some results of these experiments will eventually be integrated to a frontend generator in [xDSL](https://github.com/xdslproject/xdsl).

:warning::warning::warning:

A collection of tests with MyPy plugins that slightly abuse the Python type system to extend the syntax and add verifiers.

Examples:

| Name      | Short Description                                                             | Link                          |
| --------- | ----------------------------------------------------------------------------- | ----------------------------- |
| MyList    | Strongly typed list which can only be concatenated to lists of the same type. | [code](./examples/MyList/)    |
| Vector    | Custom vector class annotated with entry type and dimension.                  | [code](./examples/Vector/)    |
| Advanced  | Various more complex examples.                                                | [code](./examples/Advanced/)  |

## Tests

Tests for the plugins will be added [here](./tests/).