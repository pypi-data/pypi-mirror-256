import optuna

def objective(trial):
    x = trial.suggest_float("x", 0, 5)
    y = trial.suggest_float("y", 0, 3)
    v0 = 5 * x ** 2 + 3 * y ** 2
    v1 = (x - 10) ** 2 + (y - 10) ** 2
    v2 = x + y

    return v0, v1, v2

study = optuna.create_study(directions=["minimize", "minimize", "minimize"])

study.optimize(objective, n_trials=100)

fig = optuna.visualization.plot_pareto_front(study, targets=lambda t: (t.values[0], t.values[1]), target_names=["Objective 0", "Objective 1"])
fig.show()


