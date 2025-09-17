from bayes_classifier.utils.datalab import *


def calculate_prior_probs(data, target_index=-1):
    probs_dict = {}
    target = target_column(data, target_index)
    target_values = extract_unique_values(target)
    general_probs = target_values_share(target)
    columns = data.columns
    for column in columns:
        column_values = extract_unique_values(data[column])
        probs_dict[column] = equivalent_target_values(
            column_values, data[column], target
        )
        for c in probs_dict[column]:
            for key in target_values:
                if key in probs_dict[column][c]:
                    # print(probs_dict[column][c][key],"/",general_probs[key])
                    probs_dict[column][c][key] = (
                        probs_dict[column][c][key] / general_probs[key]
                    )
                else:
                    probs_dict[column][c][key] = 1 / (
                        general_probs[key] + len(probs_dict[column])
                    )  # smoothing, I was assiging to 0 but chatGPT reviewed the code and suggested me to edit this line.
    return probs_dict


def target_values_share(target_column):
    dict = {}
    target_values = extract_unique_values(target_column)
    for val in target_values:
        dict[val] = 0
    for i in range(len(target_column)):
        dict[target_column[i]] += 1
    return dict


def calculate_probs(instance, data, target_index=-1):
    is_instance_valid = validate_instance(instance, data)
    final_probs = {}
    if not is_instance_valid:
        print("Instance is not valid.")
        return None

    target = target_column(data, target_index)
    target_values = extract_unique_values(target)
    target_values_distribution = target_values_share(target)
    prior_probabilities = calculate_prior_probs(data)

    for target_value in target_values:
        current_prob = target_values_distribution[target_value] / len(target)
        print("root current prob:", current_prob)
        for key in instance:
            current_prob *= prior_probabilities[key][instance[key]][target_value]
        final_probs[target_value] = current_prob
    return final_probs


def classify(probs):
    max_prob = max(probs, key=probs.get)
    return max_prob


def calculate_prior_probs(data, target_index=-1):
    probs_dict = {}
    target = target_column(data, target_index)
    target_values = extract_unique_values(target)
    general_probs = target_values_share(target)
    columns = data.columns

    for column in columns:
        column_values = extract_unique_values(data[column])
        probs_dict[column] = equivalent_target_values(
            column_values, data[column], target
        )

        for c in probs_dict[column]:
            for key in target_values:
                if key in probs_dict[column][c]:
                    # Calculate P(feature|class) = count(feature,class) / count(class)
                    probs_dict[column][c][key] = (
                        probs_dict[column][c][key] / general_probs[key]
                    )
                else:
                    # Laplace smoothing: add 1 to numerator and vocabulary size to denominator
                    probs_dict[column][c][key] = 1 / (
                        general_probs[key] + len(column_values)
                    )

    return probs_dict


def calculate_probs(instance, data, target_index=-1):
    is_instance_valid = validate_instance(instance, data)
    final_probs = {}
    if not is_instance_valid:
        print("Instance is not valid.")
        return None

    target = target_column(data, target_index)
    target_values = extract_unique_values(target)
    target_values_distribution = target_values_share(target)
    prior_probabilities = calculate_prior_probs(
        data, target_index
    )  # Pass target_index here

    for target_value in target_values:
        current_prob = target_values_distribution[target_value] / len(target)
        print("root current prob:", current_prob)
        for key in instance:
            if key in prior_probabilities and instance[key] in prior_probabilities[key]:
                current_prob *= prior_probabilities[key][instance[key]][target_value]
            else:
                print(f"Warning: {key}={instance[key]} not found in training data")
                # Use a small probability for unseen features
                current_prob *= 1e-6
        final_probs[target_value] = current_prob

    # Normalize probabilities so they sum to 1
    total_prob = sum(final_probs.values())
    if total_prob > 0:
        for key in final_probs:
            final_probs[key] = round(final_probs[key] / total_prob, 3)
            

    return final_probs


def classify(probs):
    max_prob = max(probs, key=probs.get)
    return max_prob
