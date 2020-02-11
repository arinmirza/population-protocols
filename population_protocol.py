import random
import matplotlib.pyplot as plt
from agent import Agent


def run_experiment(num_agents=100, no_change_limit=200):

    def rand_config():
        return random.randint(0, 1)

    def random_interaction(agents):
        i, j = random.sample(range(0, len(agents)-1), 2)
        interact = agents[i].interact(agents[j])
        # print(interact)

    def count_states(agents):
        count = [0, 0, 0]
        for agent in agents:
            count[agent.state] += 1
        return count

    # Generate agents with random initial configurations
    all_agents = [Agent(rand_config()) for _ in range(num_agents)]

    # Store initial conditions
    initial_count = count_states(all_agents)
    initial_diff = initial_count[1] - initial_count[0]
    initial_majority = initial_count[1] > initial_count[0]

    # Prepare x, y lists for plotting
    x_step, y_diff = [], []

    # Main experiment loop
    step = 0
    last_count = (0, 0, 0)
    last_change = 0
    while True:
        random_interaction(all_agents)
        cur_count = count_states(all_agents)
        step += 1

        last_change = (last_change + 1) if (last_count == cur_count) else 0
        last_count = cur_count
        if last_change > no_change_limit:
            break

        diff = cur_count[1] - cur_count[0]

        x_step.append(step)
        y_diff.append(diff)

    final_count = count_states(all_agents)
    final_diff = final_count[1] - final_count[0]
    final_majority = final_count[1] > final_count[0]
    total_steps = step

    plots = {
        'diff': (x_step, y_diff)
    }

    return {
        'num_agents': num_agents,
        'initial_majority': initial_majority,
        'initial_diff': initial_diff,
        'final_diff': final_diff,
        'total_steps': total_steps,
        'success': initial_majority == final_majority,
        'plots': plots,
    }


def visualize(results):
    fig, ax = plt.subplots()

    for result in results:
        x, y = result['plots']['diff']
        plt.plot(x, y)

    ax.grid()
    plt.show()


def main():
    num_experiments = 10
    results = []

    num_exp_success = 0

    for i in range(num_experiments):
        exp = run_experiment(num_agents=500, no_change_limit=1000)
        results.append(exp)
        if exp['success']:
            num_exp_success += 1
        print(f"Exp {i}/{num_experiments} " + str(exp))

    print(f'Success raw: {num_exp_success} / {num_experiments}\nSuccess: {100 * num_exp_success/num_experiments}%')

    visualize(results)

if __name__ == '__main__':
    main()
