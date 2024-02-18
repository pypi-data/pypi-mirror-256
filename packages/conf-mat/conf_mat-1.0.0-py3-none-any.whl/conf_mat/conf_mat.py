from tabulate import tabulate
from pandas import DataFrame
from seaborn import heatmap
from matplotlib.pyplot import title, tick_params, yticks, show


def confusion_matrix(y_or_predicted_y: list, predicted_y_or_y: list) -> list:
    y_or_predicted_y = list(y_or_predicted_y)
    predicted_y_or_y = list(predicted_y_or_y)
    cm = [[0, 0], [0, 0]]
    if len(y_or_predicted_y) == len(predicted_y_or_y):
        for i in range(len(y_or_predicted_y)):
            if y_or_predicted_y[i] == predicted_y_or_y[i] == 1:
                cm[0][0] += 1
            elif y_or_predicted_y[i] == predicted_y_or_y[i] == 0:
                cm[1][1] += 1
            elif y_or_predicted_y[i] == 1 and predicted_y_or_y[i] == 0:
                cm[0][1] += 1
            elif y_or_predicted_y[i] == 0 and predicted_y_or_y[i] == 1:
                cm[1][0] += 1
        return cm
    else:
        return [[0, 0], [0, 0]]


def conf_mat_disp(y_or_predicted_y: list, predicted_y_or_y: list) -> None:
    cm = DataFrame(confusion_matrix(y_or_predicted_y, predicted_y_or_y), index=[
                   "Positive", "Negative"], columns=["", ""])
    if len(cm) == 2:
        print("\nConfusion Matrix Display : \n" + "_" *
              len("Confusion Matrix Display") + "\n")
        confusion_matrix_annot = [[f"True Positive (TP) : {cm.iloc[0,0]}", f"False Negative (FN) : {cm.iloc[0,1]}\nType II Error (Missed)"], [
            f"False Positive (FP) : {cm.iloc[1,0]}\nType I Error (Wrong)", f"True Negative (TN) : {cm.iloc[1,1]}"]]
        show()
        title("Predicted Positive                 Predicted Negative", fontsize=10)
        tick_params(axis='x', which='both', bottom=False, top=True)
        heatmap(cm, annot=confusion_matrix_annot,
                fmt='', cmap='Blues', cbar=True)
        yticks(rotation=0)
        show()
    else:
        print("Sorry, it has not been added yet. It will be added in version 1.1")


def conf_mat(y_or_predicted_y: list, predicted_y_or_y: list) -> None:
    cm = confusion_matrix(y_or_predicted_y, predicted_y_or_y)
    if len(cm) == 2:
        accuracy = ((cm[0][0] + cm[1][1]) / (
            cm[0][0] + cm[1][1] +
            cm[0][1] + cm[1][0]))
        error = round(1-accuracy, 2)
        precision = (cm[0][0] /
                     (cm[0][0] + cm[1][0]))
        negative_precision = (cm[1][1]/(cm[0][1]+cm[1][1]))
        recall = (cm[0][0] /
                  (cm[0][0] + cm[0][1]))
        specificity = (cm[1][1]/(cm[1][1]+cm[1][0]))
        data1 = [
            [
                "Classes",
                "Predicted Positive (PP)",
                "Predicted Negative (PN)",
                "",
            ],
            [
                "Actual Positive (P)",
                f"True Positive (TP) : {cm[0][0]}",
                f"False Negative (FN) : {cm[0][1]}\nType II Error (Missed)",
            ],
            [
                "Actual Negative (N)",
                f"False Positive (FP) : {cm[1][0]}\nType I Error (Wrong)",
                f"True Negative (TN) : {cm[1][1]}",
            ],
        ]
        data2 = [
            [
                "",
                "Rate (Score)",
            ],
            [
                "Accuracy",
                "Correct        TP + TN\n" + "_" * len("Correct") + " : " + "_" *
                len("TP + FP + FN + TN") + "  OR  1 - Error " + " =  " +
                f"{round(accuracy, 2)}" + "\n\n Total    TP + FP + FN + TN",
            ],
            [
                "Error",
                "Wrong        FP + FN\n" + "_" * len("Wrong") + " : " + "_" *
                len("TP + FP + FN + TN") + "  OR  1 - Accuracy " +
                " =  " + f"{error}" + "\n\nTotal   TP + FP + FN + TN",
            ],
        ]
        support_1 = cm[0][1] + cm[0][0]
        support_0 = cm[1][0] + cm[1][1]
        f_score_1 = (2 * precision * recall) / (precision + recall)
        f_score_0 = ((2 * negative_precision * specificity) /
                     (negative_precision + specificity))
        data3 = [
            [
                "Precision (P)",
                "Recall (R)",
                "F1-Score (F)",
                "Support (S)",
            ],
            [
                "Positive (1)",
                "P1 (PPV): \n\n  TP\n" + "_" *
                len("TP + FP") + "  = " +
                f"{round(precision, 2)}" + "\n\nTP + FP",
                f"R1 (Sensitivity):\n\n  TP\n" + "_" * len("TP + FN") +
                "  = " + f"{round(recall, 2)}" + "\n\nTP + FN",
                "F1 : \n\n" + "2 x P1 x R1\n" + "_" * len("2 x P1 x R1") +
                "  = " + f"{round(f_score_1, 2)}" + "\n\n  P1 + R1",
                f"S1 : \n\n\n TP + FN = {support_1}",
            ],
            [
                "Negative (0)",
                f"P0 (NPV): \n\n  TN\n" + "_" *
                len("TN + FN") + "  = " +
                f"{round(negative_precision, 2)}" + "\n\nTN + FN",
                f"R0 (Specificity): \n\n  TN\n" + "_" * len("TN + FP") +
                "  = " + f"{round(specificity, 2)}" + "\n\nTN + FP",
                "F0 : \n\n" + "2 x P0 x R0\n" + "_" * len("2 x P0 x R0") +
                "  = " + f"{round(f_score_0, 2)}" + "\n\n  P0 + R0",
                f"S0 : \n\n\n FP + TN = {support_0}",
            ],
            [
                "Macro Avg",
                "P1 + P0\n" + "_" *
                len("P1 + P0") + "  = " +
                f"{round((round(precision, 2)+round(negative_precision, 2))/2, 2)}" + "\n\n   2",
                "R1 + R0\n" + "_" *
                len("R1 + R0") + "  = " +
                f"{round((round(recall, 2)+round(specificity, 2))/2, 2)}" + "\n\n   2",
                "F1 + F0\n" + "_" * len("F1 + F0") + "  = " +
                f"{round((round(f_score_1, 2)+round(f_score_0, 2))/2, 2)}" + "\n\n   2",
                f"TS = {support_0+support_1}",
            ],
            [
                "Weighted Avg",
                "W1\n" + "_" * len("TS") + "  = " +
                f"{round(((round(precision, 2)*support_1)+(round(negative_precision, 2)*support_0))/(support_0+support_1), 2)}" + "\n\nTS",
                "W2\n" + "_" * len("TS") + "  = " +
                f"{round(((round(recall, 2)*support_1)+(round(specificity, 2)*support_0))/(support_0+support_1), 2)}" + "\n\nTS",
                "W3\n" + "_" * len("TS") + "  = " +
                f"{round(((round(f_score_1, 2)*support_1)+(round(f_score_0, 2)*support_0))/(support_1+support_0),2)}" + "\n\nTS",
                f"TS = {support_0+support_1}",
            ],
        ]
        print("\nConfusion Matrix : \n" + "_" * len("Confusion Matrix") + "\n")
        print(tabulate(data1, headers="firstrow", tablefmt="fancy_grid") + "\n")
        print(tabulate(data2, headers="firstrow", tablefmt="fancy_grid") + "\n")
        print("\nClassification Report : \n" + "_" *
              len("Classification Report") + "\n")
        print(tabulate(data3, headers="firstrow", tablefmt="fancy_grid"))
        print("\nPPV : Positive Predictive Value")
        print("\nNPV : Negative Predictive Value")
        print("\nW1 = (P1 x S1) + (P0 x S0)")
        print("\nW2 = (R1 x S1) + (R0 x S0)")
        print("\nW3 = (F1 x S1) + (F0 x S0)")
        print("\nTS : Total Support = S1 + S0\n")
    else:
        print("Sorry, it has not been added yet. It will be added in version 1.0.1")
