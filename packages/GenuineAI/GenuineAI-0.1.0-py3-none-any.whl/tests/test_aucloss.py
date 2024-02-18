#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geniune AI functions
Related to the IMICS lab research projects

@author: Ernest Namdar  ernest.namdar@utoronto.ca
"""
import unittest
import torch
from GenuineAI.loss_functions import AUCLoss

class TestAUCLoss(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""
        self.loss_function = AUCLoss()
        torch.manual_seed(0)  # For reproducibility

    def test_auclass_positive_vs_negative(self):
        """Test AUCLoss with a simple positive vs. negative scenario."""
        # Mock outputs from a model for a batch size of 4
        # Assume logits for two classes; the correct implementation should apply softmax
        output = torch.tensor([[0.1, 0.9], [0.8, 0.2], [0.4, 0.6], [0.3, 0.7]])
        # Ground truth: first two samples are positive, last two are negative
        target = torch.tensor([1, 1, 0, 0])

        # Compute loss
        loss = self.loss_function(output, target)

        # Check if loss is a tensor and a single value
        self.assertTrue(torch.is_tensor(loss), "Loss should be a tensor.")
        self.assertEqual(loss.dim(), 0, "Loss should be a scalar tensor.")

        # Further tests can be added to check the correctness of the loss value
        # This might involve comparing to a pre-computed value or ensuring it falls within expected bounds


# This allows the test script to be run from the command line
if __name__ == '__main__':
    unittest.main()
