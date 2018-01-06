# hpsearch

Hyperparameter tuning for the average Joe.

## Why hpsearch?

* Lightweight. Adds minimal dependencies to your project.
* Same config structure used by Google Cloud ML Engine.

## Usage

Config is meant to be compatible with HyperparameterSpec from Google Cloud ML Engine.

```textproto
# config.textproto

name: "my_project"
goal: MINIMIZE
max_trials: 10
max_parallel_trials: 1
params {
  parameter_name: "learning_rate"
  type: FLOAT
  min_value: 1e-4
  max_value: 1e-1
  scale_type: UNIT_LOG_SCALE
}
params {
  parameter_name: "cell_type"
  type: CATEGORICAL
  categorical_values: "BasicLSTMCell"
  categorical_values: "GRUCell"
}
```

```bash
>> hpsearch config.textproto
```
