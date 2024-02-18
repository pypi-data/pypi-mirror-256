#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geniune AI functions
Related to the IMICS lab research projects

@author: Ernest Namdar  ernest.namdar@utoronto.ca
"""
import torch
import torch.nn as nn


sofmx = nn.Softmax(dim=1)

def logistic_func(x, k=1, L=1, x_zero=0):
    """
    Compute the logistic function, a sigmoid curve, for a given input.

    The logistic function is defined as L / (1 + exp(-k * (x - x_zero))),
    where L is the curve's maximum value, k is the steepness of the curve,
    x is the input, and x_zero is the value of x at the sigmoid's midpoint.

    Parameters:
    - x (torch.Tensor): The input tensor for which to compute the logistic function.
    - k (float): The steepness of the logistic curve. A higher value makes the curve steeper. Defaults to 1.
    - L (float, optional): The curve's maximum value. Defaults to 1, resulting in a range of (0, L).
    - x_zero (float, optional): The midpoint of the sigmoid, where the output is L/2. Defaults to 0.

    Returns:
    - torch.Tensor: The logistic function's output for each element in x, with the same shape as x.
    """
    return L / (1 + torch.exp(-k * (x - x_zero)))


class AUCLoss(nn.Module):
    """
    A custom loss class that approximates the Area Under the Curve (AUC) loss for binary classification.

    This class computes a differentiable approximation of the AUC metric by considering the pairwise differences
    between the positive and negative samples' predictions and applying a logistic function to these differences.
    The mean of the transformed differences is subtracted from 1 to provide a loss value that when minimized,
    increases the AUC metric.
    For more information, refere to our paper: https://arxiv.org/abs/2402.03547
    """
    def __init__(self):
        """
        Initializes the AUCLoss instance by calling the superclass's constructor.
        """
        super(AUCLoss, self).__init__()

    def forward(self, output, target):
        """
        Defines the computation performed at every call.

        Parameters:
        - output (torch.Tensor): The predictions from the model. For binary classification,
                                 it should have a shape [batch_size, 2], where the second dimension
                                 represents "logit scores" for each class.
        - target (torch.Tensor): The ground truth labels with shape [batch_size]. Each element should be
                                 either 0 (negative class) or 1 (positive class).

        Returns:
        - torch.Tensor: The computed AUC loss as a single scalar.
        """
        # Apply softmax to convert logits to probabilities, focusing on the positive class (index 1)
        output = sofmx(output)[:, 1]

        # Separate predictions into positive and negative based on ground truth labels
        pos_pred = output[target == 1]
        neg_pred = output[target == 0]

        # Calculate pairwise differences between positive and negative predictions
        pairwise_matrix = pos_pred.unsqueeze(1) - neg_pred.unsqueeze(0)

        # Apply a logistic function to the pairwise differences
        transform = logistic_func(pairwise_matrix, k=20)

        # Compute the loss as 1 minus the mean of the transformed differences
        # This formulation encourages the model to increase the margin between positive and negative predictions
        return 1 - transform.mean()


class MulticlassAUCLoss(nn.Module):
    """
    A custom loss class designed for multiclass classification tasks that approximates
    the multiclass One vs the rest (OvR) Area Under the Curve (AUC).

    This class computes a differentiable approximation of the AUC metric by considering the pairwise
    differences between the predictions for a given class (treated as "positive") and the predictions
    for all other classes (treated as "negative"), applying a logistic function to these differences,
    and then averaging the results across all classes.
    """
    def __init__(self):
        """
        Initializes the MulticlassAUCLoss instance by calling the superclass's constructor.
        """
        super(MulticlassAUCLoss, self).__init__()

    def forward(self, output, target):
        """
        Defines the computation performed at every call.

        Parameters:
        - output (torch.Tensor): The predictions from the model for each class. It should have a shape
                                 [batch_size, num_classes], where num_classes is the total number of classes.
        - target (torch.Tensor): The ground truth labels with shape [batch_size]. Each element should be
                                 the index of the correct class, ranging from 0 to num_classes-1.

        Returns:
        - torch.Tensor: The computed loss as a single scalar, representing the averaged AUC loss across all classes.
        """
        # Apply softmax to convert logits to probabilities for each class
        output = sofmx(output)

        # Determine the number of classes from the output tensor
        num_classes = output.size(1)

        # Initialize the sum of per-class AUC scores
        sum_per_class_auc = 0.0

        # Iterate over each class to calculate its AUC score
        for class_index in range(num_classes):
            # Select predictions for the current class as "positive" predictions
            pos_pred = output[:, class_index][target == class_index]
            # Select predictions for other classes as "negative" predictions
            neg_pred = output[:, class_index][target != class_index]

            # Calculate pairwise differences between positive and negative predictions for the class
            pairwise_matrix = pos_pred.unsqueeze(1) - neg_pred.unsqueeze(0)

            # Apply a logistic function to the pairwise differences
            transform = logistic_func(pairwise_matrix, k=20)

            # Compute the mean of the transformed differences as the AUC score for the class
            class_auc = transform.mean()

            # Accumulate the AUC scores across all classes
            sum_per_class_auc += class_auc

        # Calculate the final loss as 1 minus the average of the AUC scores across all classes
        return 1 - (sum_per_class_auc / num_classes)
