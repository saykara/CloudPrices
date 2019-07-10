import matplotlib.pyplot as plt
import simulator
import parameters as par
import numpy as np
import time


def plot_result(cust_start, cust_end, exp_start, exp_end):
    sim = simulator.Simulator()
    sim.initialize_parameters(cust_start, cust_end, exp_start, exp_end)
    sim.simulation(20000)

    plot_gantt(sim)
    plot_customer_distribution(sim)
    plot_rate_change(sim)
    plot_price_change(sim)


def plot_gantt(sim):
    result = sim.gantt_list
    outsource = sim.out_list
    reject = sim.reject_list

    plt.figure(figsize=(20, 10))
    # plt.add_subplot(111)
    for i in range(round(len(result) / 4)):
        plt.barh((i * 0.5) + 0.5, result[i * 4][1] - result[i * 4][0], left=result[i * 4][0], height=0.25,
                 align='center', color='green')

    x_out = []
    y_out = []

    for i in outsource:
        x_out.append(i[1])
        y_out.append(i[0] * 0.5 * 0.25)

    plt.plot(x_out, y_out, 'bo')

    x_rej = []
    y_rej = []

    for i in reject:
        x_rej.append(i[1])
        y_rej.append(i[0] * 0.5 * 0.25)

    plt.plot(x_rej, y_rej, 'ro')

    plt.savefig('outputs/gantt.png')
    plt.savefig('outputs/gantt.svg')

def plot_customer_distribution(sim):
    plt.clf()
    plt.figure(figsize=(20, 8))
    brand_list = par.CloudParameters.brand
    print(brand_list)
    customer_list = []
    for i in brand_list:
        customer_list.append(sim.customer_list.count(i))
    y_pos = np.arange(len(brand_list))
    print(customer_list)
    plt.bar(y_pos, customer_list, align='center', alpha=0.5)
    plt.xticks(y_pos, brand_list)
    plt.ylabel('Usage')
    plt.title('Customer by Brand')
    plt.savefig('outputs/customer.png')


def plot_rate_change(sim):
    plt.clf()
    plt.figure(figsize=(20, 8))
    a = [0]
    b = [0]
    c = [0]
    for i in sim.rate_history:
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])

    plt.plot(a, "r", label="Google")
    plt.plot(b, "g", label="Azure")
    plt.plot(c, "b", label="Amazon")
    plt.ylabel('Rate')
    plt.legend(loc='upper right')
    plt.title('Rate Changes')
    # plt.show()
    plt.savefig('outputs/rate.png')


def plot_price_change(sim):
    plt.clf()
    plt.figure(figsize=(20, 8))
    a = []
    b = []
    c = []
    for j in sim.fundamental_price_list:
        if j[0] == "Google":
            a.append(j[1])
        elif j[0] == "Azure":
            b.append(j[1])
        elif j[0] == "Amazon":
            c.append(j[1])


    for i in sim.rate_history:
        for j in sim.fundamental_price_list:
            if j[0] == "Google":
                a.append(j[1] + (j[1]*i[0]) / 100)
            elif j[0] == "Azure":
                b.append(j[1] + (j[1]*i[1]) / 100)
            elif j[0] == "Amazon":
                c.append(j[1] + (j[1]*i[2]) / 100)

    plt.plot(a, "r", label="Google")
    plt.plot(b, "g", label="Azure")
    plt.plot(c, "b", label="Amazon")
    plt.ylabel('Price')
    plt.legend(loc='upper right')
    plt.title('Price Changes')
    # plt.show()
    plt.savefig('outputs/price.png')

plot_result(0,1,15,90)