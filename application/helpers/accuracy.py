import datetime
import application.helpers.constant as C
import application.helpers.io as io


class Accuracy:
    def __init__(self, method=None):
        self.desc = method + " accuracy"
        self.accuracy = []
        self.logs = []


    def calculate(self, product, rsky, true_rsky_id, customers):
        rsky_id = [obj[C.ID] for obj in rsky]
        customers_id = [obj[C.ID] for obj in customers]
        not_rsky_id = list(set(customers_id) - set(rsky_id))
        not_true_rsky_id = list(set(customers_id) - set(true_rsky_id))

        # check accuracy of RSL in pruning customers
        true_positive = list(set(rsky_id).intersection(true_rsky_id)) 
        true_negative = list(set(not_rsky_id).intersection(not_true_rsky_id))
        false_positive = list(set(rsky_id) - set(true_positive))
        false_negative = list(set(not_rsky_id) - set(true_negative))

        # calculate the accuracy 
        accuracy = ((len(true_positive) + len(true_negative)) / (len(true_positive) + len(true_negative) + len(false_positive) + len(false_negative))) * 100
        self.accuracy.append(accuracy)

        # add to log 
        log = " ".join(["Product " + str(product[C.ID]), "\t", "{:.2f}".format(accuracy), "%"])
        self.logs.append(log)


    def calc_overall(self):
        overall_accuracy = sum(self.accuracy) / len(self.accuracy)
        log = " ".join(["Overall Accuracy", "\t", "{:.2f}".format(overall_accuracy), "%"])
        self.logs.append(log)


    def export(self):
        self.calc_overall()
        filename = C.ACCURACY_PATH + self.desc.replace(" ", "_") + "_" + str(datetime.datetime.now().date()) + ".txt"
        io.export_txt(C.ACCURACY_PATH, filename, self.logs)
    