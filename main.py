import simulator
import os
import results


def run(cust_start, cust_end, exp_start, exp_end, range):
    sim = simulator.Simulator()
    sim.initialize_parameters(cust_start, cust_end, exp_start, exp_end)
    sim.simulation(range)
    return sim


def plot_result(range, doc_name, sim):
    if not os.path.exists('outputs/' + doc_name):
        os.mkdir('outputs/' + doc_name)
    p = results.Plot
    # p.plot_gantt(sim, doc_name)
    p.plot_outsource_difference(sim, range, doc_name)
    p.plot_customer_distribution(sim, doc_name)
    p.plot_rate_change(sim, doc_name)
    p.plot_price_change(sim, doc_name)


k = run(0,1,15,60,20000)
plot_result(20000, "20000", k)