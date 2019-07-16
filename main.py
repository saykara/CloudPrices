import simulator
import time
import results


def run(cust_start, cust_end, exp_start, exp_end, range, out):
    print("Simulation starting for " + str(range) + " customer.")
    sim = simulator.Simulator()
    sim.initialize_parameters(cust_start, cust_end, exp_start, exp_end)
    sim.simulation(range, out)
    print("Simulation ended.")
    return sim


if __name__ == "__main__":
    while True:
        print("Choose an operation.")
        print("(1)Simulation with non-cooperated game.")
        print("(2)Simulation without outsource.")
        print("(3)Compare revenue.")
        choose = input()
        if choose == '1':
            length = input("Enter simulator range: ")
            if length.isdigit() and int(length) > 0:
                file_name = input("Enter output file name: ")
                sim = run(0, 1, 15, 60, int(length), True)
                results.Plot.plot_result(int(length), file_name, sim)
            else:
                print("Invalid input!")
        elif choose == '2':
            length = input("Enter simulator range: ")
            if length.isdigit() and int(length) > 0:
                file_name = input("Enter output file name: ")

                sim = run(0, 1, 15, 60, int(length), False)
                results.Plot.plot_result(int(length), file_name, sim)
            else:
                print("Invalid input!")
        elif choose == '3':
            length = input("Enter simulator range: ")
            if length.isdigit() and int(length) > 0:
                file_name = input("Enter output file name: ")

                sim_1 = run(0, 1, 15, 60, int(length), True)
                results.Plot.plot_result(int(length), file_name, sim_1)

                sim_2 = run(0, 1, 15, 60, int(length), False)
                results.Plot.plot_revenue_difference(sim_1.results.brand_profits, sim_2.results.brand_profits, "T")
            else:
                print("Invalid input!")
        else:
            print("Invalid input!")
# start = time.time()
# sim = run(0, 1, 15, 60, int(2000), True)
# results.Plot.plot_result(int(2000), "G", sim)
# print(time.time()-start)