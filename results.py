import matplotlib.pyplot as plt
import parameters as par
import os


class Plot:
    @classmethod
    def plot_gantt(cls, sim, doc_name):
        result = sim.results.gantt_list
        outsource = sim.results.out_list
        reject = sim.results.reject_list

        plt.figure(figsize=(30, 15))
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

        plt.title('Event Time Graph', fontsize=20)

        plt.savefig('outputs/' + doc_name + '/gantt.png')
        plt.savefig('outputs/' + doc_name + '/gantt.svg')
        plt.close()

    @classmethod
    def plot_customer_distribution(cls, sim, doc_name):
        plt.clf()
        plt.figure(figsize=(8, 8))
        brand_list = par.CloudParameters.brand
        customer_list = []
        for i in brand_list:
            customer_list.append(sim.results.customer_list.count(i))

        y_pos = []
        for i in range(len(brand_list)):
            y_pos.append(i * 0.5)

        plt.bar(y_pos, customer_list, width=0.3, align='center', alpha=0.5, color=("red", "green", "blue"))
        plt.xticks(y_pos, brand_list)
        plt.ylabel('Usage', fontsize=16)
        plt.xlabel('Brands', fontsize=16)
        plt.title('Customer by Brand', fontsize=20)
        plt.savefig('outputs/' + doc_name + '/customer.png')
        plt.close()

    @classmethod
    def plot_outsource_difference(cls, sim, range, doc_name):
        plt.clf()
        plt.figure(figsize=(8, 8))
        plt.bar(0.5 - 0.1, sim.state['successful'], width=0.2, align='center', alpha=0.75, color="green")
        plt.bar(0.5 + 0.1, range - sim.state['successful'], width=0.2, align='center', alpha=0.75, color="red")
        plt.bar(1 - 0.1, range - sim.state['fail'], width=0.2, align='center', alpha=0.75, color="blue")
        plt.bar(1 + 0.1, sim.state['fail'], width=0.2, align='center', alpha=0.75, color="red")
        plt.xticks([0.5, 1], ["No Outsource", "Outsource"])
        plt.ylabel('Count', fontsize=16)
        plt.xlabel('State', fontsize=16)
        plt.title('With Outsource - Without Outsource', fontsize=20)
        plt.savefig('outputs/' + doc_name + '/success.png')
        plt.close()

    @classmethod
    def plot_revenue_difference(cls, x, y, doc_name):
        plt.clf()
        plt.figure(figsize=(12, 12))

        plt.bar(0.5 - 0.1, x[0][1], width=0.2, align='center', alpha=0.5, color="green")
        plt.bar(0.5 + 0.1, y[0][1], width=0.2, align='center', alpha=0.5, color="red")
        plt.bar(1 - 0.1, x[1][1], width=0.2, align='center', alpha=0.5, color="blue")
        plt.bar(1 + 0.1, y[1][1], width=0.2, align='center', alpha=0.5, color="red")
        plt.bar(1.5 - 0.1, x[2][1], width=0.2, align='center', alpha=0.5, color="yellow")
        plt.bar(1.5 + 0.1, y[2][1], width=0.2, align='center', alpha=0.5, color="red")

        plt.xticks([0.5, 1, 1.5], [x[0][0], x[1][0], x[2][0]])
        plt.ylabel('Revenue', fontsize=16)
        plt.xlabel('Brands', fontsize=16)
        plt.title('Revenue Difference', fontsize=20)
        plt.savefig('outputs/' + doc_name + '/revenue.png')
        plt.close()

    @classmethod
    def plot_rate_change(cls, sim, doc_name):
        plt.clf()
        plt.figure(figsize=(20, 8))
        a = [0]
        b = [0]
        c = [0]
        for i in sim.results.rate_history:
            a.append(i[0])
            b.append(i[1])
            c.append(i[2])

        plt.plot(a, "r", label="Google")
        plt.plot(b, "g", label="Azure")
        plt.plot(c, "b", label="Amazon")
        plt.ylabel('Rate', fontsize=16)
        plt.xlabel('Time', fontsize=16)
        plt.legend(loc='upper right')
        plt.title('Rate Changes', fontsize=20)
        plt.savefig('outputs/' + doc_name + '/rate.png')
        plt.close()

    @classmethod
    def plot_price_change(cls, sim, doc_name):
        plt.clf()
        plt.figure(figsize=(20, 8))
        a = []
        b = []
        c = []
        for j in sim.results.fundamental_price_list:
            if j[0] == "Google":
                a.append(j[1])
            elif j[0] == "Azure":
                b.append(j[1])
            elif j[0] == "Amazon":
                c.append(j[1])

        for i in sim.results.rate_history:
            for j in sim.results.fundamental_price_list:
                if j[0] == "Google":
                    a.append(j[1] + (j[1]*i[0]) / 100)
                elif j[0] == "Azure":
                    b.append(j[1] + (j[1]*i[1]) / 100)
                elif j[0] == "Amazon":
                    c.append(j[1] + (j[1]*i[2]) / 100)

        plt.plot(a, "r", label="Google")
        plt.plot(b, "g", label="Azure")
        plt.plot(c, "b", label="Amazon")

        plt.ylabel('Price', fontsize=16)
        plt.xlabel('Time', fontsize=16)
        plt.legend(loc='upper right')
        plt.title('Price Changes', fontsize=20)
        # plt.show()
        plt.savefig('outputs/' + doc_name + '/price.png')
        plt.close()

    @classmethod
    def plot_result(cls, range, doc_name, sim):
        if not os.path.exists('outputs/' + doc_name):
            print("Creating file.")
            os.mkdir('outputs/' + doc_name)

        print("Table creation starting.")
        # cls.plot_gantt(sim, doc_name)
        cls.plot_outsource_difference(sim, range, doc_name)
        cls.plot_customer_distribution(sim, doc_name)
        cls.plot_rate_change(sim, doc_name)
        cls.plot_price_change(sim, doc_name)
        print("Table creation ended.")
