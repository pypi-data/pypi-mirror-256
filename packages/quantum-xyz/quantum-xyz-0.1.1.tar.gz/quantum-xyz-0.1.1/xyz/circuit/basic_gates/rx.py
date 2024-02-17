#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2023-09-13 10:22:43
Last Modified by: Hanyu Wang
Last Modified time: 2023-09-13 10:23:19
"""

from .base import BasicGate, QBit, QGateType, RotationGate


class RX(RotationGate, BasicGate):
    """Constructs a RX gate .

    :param RotationGate: [description]
    :type RotationGate: [type]
    :param BasicGate: [description]
    :type BasicGate: [type]
    """

    def __init__(self, theta: float, target_qubit: QBit) -> None:
        BasicGate.__init__(self, QGateType.RX, target_qubit)
        RotationGate.__init__(self, theta)

    def __str__(self) -> str:
        return f"RX({self.theta:0.02f})"

    def get_cnot_cost(self) -> int:
        """Returns the cost of the cost of the gate.

        :return: [description]
        :rtype: int
        """
        return 0
