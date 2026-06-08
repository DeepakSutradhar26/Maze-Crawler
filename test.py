from kaggle_environments import make

env = make("crawl", configuration={"randomSeed": 42, "episodeSteps": 2}, debug=True)
env.run(["main.py", "random"])

# View result
final = env.steps[-1]
for i, s in enumerate(final):
    print(f"Player {i}: reward={s.reward}, status={s.status}")

# Render in a notebook
env.render(mode="ipython", width=800, height=800)
