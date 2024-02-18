

import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 5)
    y = trial.suggest_float("y", 0, 3)

    v0 = 4 * x ** 2 + 4 * y ** 2
    v1 = (x - 5) ** 2 + (y - 5) ** 2
    if 0 < x < 1:
        return float('nan'), float('nan')
    else:
        return v0, v1


study = optuna.create_study(study_name='trial_optuna', directions=["minimize", "minimize"],
                            load_if_exists=True,
                            storage="sqlite:///trial_optuna.sqlite3",)
study.optimize(objective, n_trials=50)

print(f"{len(study.trials)}")


#fig = optuna.visualization.plot_pareto_front(study)
#fig.show()