import simulator

class Node:
    value_list = []
    change_list = []
    counter = 0
    def __init__(self, data):
        self.left = None
        self.right = None
        self.center = None
        self.root = None
        self.data = data

    def insert_left(self, new_node):
        self.left = new_node

    def insert_right(self, new_node):
        self.right = new_node

    def insert_center(self, new_node, ):
        self.center = new_node

    @classmethod
    def tree_construction(cls, root, depth):
        if depth == 0:
            data = []
            for i in range(len(cls.value_list)):
                data.append(float(cls.value_list[i]) * ((100 + cls.change_list[i][cls.counter]) / 100))
            root.data = data
            cls.counter += 1
        else:
            root.insert_left(Node(None))
            root.insert_right(Node(None))
            root.insert_center(Node(None))
            cls.tree_construction(root.left, depth - 1)
            cls.tree_construction(root.center, depth - 1)
            cls.tree_construction(root.right, depth - 1)

    def find_maximum_value(self, index):
        if Node.calculate_profit(self.left.data, index) > Node.calculate_profit(self.center.data, index):
            maximum = self.left.data
        else:
            maximum = self.center.data

        if Node.calculate_profit(self.right.data, index) > Node.calculate_profit(maximum, index):
            maximum = self.right.data
        return maximum

    @classmethod
    def calculate_profit(cls, data, index):
        sum = 0
        for i in data:
            sum += i
        return data[index] * (sum - data[index]) * cls.customer_level_coefficient(data, index) / (2 * sum)

    @classmethod
    def arrange_value_list(cls, value):
        cls.counter = 0
        cls.value_list = value
        branch = 3
        count = len(cls.value_list)
        elements = [-3, 0, 3]
        needed_element_count = pow(branch, count)

        for i in range(count):
            cls.change_list.append(cls.create_change_element_list(needed_element_count/pow(branch, i), branch, i, elements))

    @classmethod
    def create_change_element_list(cls, x, y, z, elements):
        result = []
        for i in range(int(x)):
            for j in range(pow(y, z)):
                result.append(elements[i % 3])
        return result

    def maximize(self, index, value_index):
        # Index == 2
        if index == 2:
            temp = self.left
            temp.left.data = temp.left.find_maximum_value(value_index)
            temp.center.data = temp.center.find_maximum_value(value_index)
            temp.right.data = temp.right.find_maximum_value(value_index)

            temp = self.center
            temp.left.data = temp.left.find_maximum_value(value_index)
            temp.center.data = temp.center.find_maximum_value(value_index)
            temp.right.data = temp.right.find_maximum_value(value_index)

            temp = self.right
            temp.left.data = temp.left.find_maximum_value(value_index)
            temp.center.data = temp.center.find_maximum_value(value_index)
            temp.right.data = temp.right.find_maximum_value(value_index)
        # Index == 1
        if index == 1:
            temp = self.left
            temp.data = temp.find_maximum_value(value_index)

            temp = self.center
            temp.data = temp.find_maximum_value(value_index)

            temp = self.right
            temp.data = temp.find_maximum_value(value_index)
        # Index == 0
        if index == 0:
            self.data = self.find_maximum_value(value_index)

    @classmethod
    def calculate_best_move(cls, list):
        prog = Node
        prog.arrange_value_list(list)
        lenght = len(list)
        root = Node(None)
        prog.tree_construction(root, lenght)
        for i in range(lenght-1, -1, -1):
            root.maximize(i, lenght-1-i)
        return root.data

    @classmethod
    def customer_level_coefficient(cls, value_list, index):
        sum = 0
        prices = simulator.Simulator.get_starting_fundamental_prices()
        for i in prices:
            sum += i[1]
        sum /= 3

        if value_list[index] > sum:
            if value_list[index] < sum * 2:
                return 1 - ((value_list[index] - sum) / (sum ))
            else:
                return 0
        else:
            return 1