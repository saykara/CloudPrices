import matplotlib.pyplot as plt
import parameters as par


class Plot:
    @classmethod
    def plot_gantt(cls, sim, doc_name):
        result = sim.gantt_list
        outsource = sim.out_list
        reject = sim.reject_list

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

        plt.savefig('outputs/' + doc_name + '/gantt.png')
        plt.savefig('outputs/' + doc_name + '/gantt.svg')

    @classmethod
    def plot_customer_distribution(cls, sim, doc_name):
        plt.clf()
        plt.figure(figsize=(8, 8))
        brand_list = par.CloudParameters.brand
        customer_list = []
        for i in brand_list:
            customer_list.append(sim.customer_list.count(i))

        y_pos = []
        for i in range(len(brand_list)):
            y_pos.append(i * 0.5)

        plt.bar(y_pos, customer_list, width=0.3, align='center', alpha=0.5, color=("red", "green", "blue"))
        plt.xticks(y_pos, brand_list)
        plt.ylabel('Usage')
        plt.xlabel('Brands')
        plt.title('Customer by Brand')
        plt.savefig('outputs/' + doc_name + '/customer.png')

    @classmethod
    def plot_outsource_difference(cls, sim, range, doc_name):
        plt.clf()
        plt.figure(figsize=(6, 6))
        plt.bar(0.5 - 0.1, sim.state['successful'], width=0.2, align='center', alpha=0.75, color="green")
        plt.bar(0.5 + 0.1, range - sim.state['successful'], width=0.2, align='center', alpha=0.75, color="red")
        plt.bar(1 - 0.1, range - sim.state['fail'], width=0.2, align='center', alpha=0.75, color="blue")
        plt.bar(1 + 0.1, sim.state['fail'], width=0.2, align='center', alpha=0.75, color="red")
        plt.xticks([0.5, 1], ["No Outsource", "Outsource"])
        plt.ylabel('Count')
        plt.xlabel('State')
        plt.title('With Outsource - Without Outsource')
        plt.savefig('outputs/' + doc_name + '/success.png')

    @classmethod
    def plot_rate_change(cls, sim, doc_name):
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
        plt.xlabel('Time')
        plt.legend(loc='upper right')
        plt.title('Rate Changes')
        plt.savefig('outputs/' + doc_name + '/rate.png')

    @classmethod
    def plot_price_change(cls, sim, doc_name):
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
        plt.xlabel('Time')
        plt.legend(loc='upper right')
        plt.title('Price Changes')
        # plt.show()
        plt.savefig('outputs/' + doc_name + '/price.png')


