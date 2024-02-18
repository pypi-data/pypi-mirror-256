from __future__ import annotations

from typing import List, Union

import numpy as np
import roboticstoolbox as rtb
from dqrobotics import C8, DQ, haminus8, vec8
from dqrobotics.robots import FrankaEmikaPandaRobot
from dqrobotics.utils.DQ_LinearAlgebra import pinv

from .basemg import BaseMotionGenerator, ManipulabilityMotionGenerator
from .screwmpc import BOUND


class PandaScrewMotionGenerator(BaseMotionGenerator):
    r"""Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.

    :param n_p: Prediction horizon :math:`n_p`.
    :type n_p: int
    :param n_c: Control horizon :math:`n_c`.
    :type n_c: int
    :param q_mpc: :math:`\boldsymbol{Q}=q_{mpc}\boldsymbol{I}`.
    :type q_mpc: float
    :param r_mpc: :math:`\boldsymbol{R}=r_{mpc}\boldsymbol{I}`.
    :type r_mpc: float
    :param lu_bound_vel: lower- and upper bound for velocity.
    :type lu_bound_vel: BOUND
    :param lu_bound_acc: lower- and upper bound for accerlation.
    :type lu_bound_acc: BOUND
    :param lu_bound_jerk: lower- and upper bound for jerk.
    :type lu_bound_jerk: BOUND
    :param sclerp: ScLERP interpolation for EE pose generatation,
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
    """

    def __init__(
        self,
        n_p: int,
        n_c: int,
        q_mpc: float,
        r_mpc: float,
        lu_bound_vel: BOUND,
        lu_bound_acc: BOUND,
        lu_bound_jerk: BOUND,
        sclerp: float = 0.1,
    ) -> None:
        super().__init__(
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        self._kin = FrankaEmikaPandaRobot.kinematics()

    def step(self, q_robot: np.ndarray, goal: DQ) -> np.ndarray:
        r"""Perform one step for motion generation.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """

        x_current = self._kin.fkm(q_robot)
        error, smooth_traj = super().step(x_current, goal)
        dot_x = vec8(error)
        j_pose = np.linalg.multi_dot(
            [haminus8(smooth_traj), C8(), self._kin.pose_jacobian(q_robot)]
        )

        return pinv(j_pose) @ dot_x


class PandaScrewMpMotionGenerator(ManipulabilityMotionGenerator):
    r"""Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.
        Further, the manipulability of the robot is considered.

    :param n_p: Prediction horizon :math:`n_p`.
    :type n_p: int
    :param n_c: Control horizon :math:`n_c`.
    :type n_c: int
    :param q_mpc: :math:`\boldsymbol{Q}=q_{mpc}\boldsymbol{I}`.
    :type q_mpc: float
    :param r_mpc: :math:`\boldsymbol{R}=r_{mpc}\boldsymbol{I}.
    :type r_mpc: float
    :param lu_bound_vel: lower- and upper bound for velocity.
    :type lu_bound_vel: BOUND
    :param lu_bound_acc: lower- and upper bound for accerlation.
    :type lu_bound_acc: BOUND
    :param lu_bound_jerk: lower- and upper bound for jerk.
    :type lu_bound_jerk: BOUND
    :param sclerp: ScLERP interpolation for EE pose generatation,
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
    :type sclerp: float, optional
    """

    def __init__(
        self,
        n_p: int,
        n_c: int,
        q_mpc: float,
        r_mpc: float,
        lu_bound_vel: BOUND,
        lu_bound_acc: BOUND,
        lu_bound_jerk: BOUND,
        sclerp: float = 0.1,
    ) -> None:
        super().__init__(
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        self._panda_kin_dq = FrankaEmikaPandaRobot.kinematics()
        self._panda_rtb = rtb.models.Panda()

    def step(self, *args: List[Union[DQ, np.ndarray]]) -> np.ndarray:  # noqa: UP006
        r"""Perform one step for motion generation.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :raises ValueError: If the the number of arguments mismatch.
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """
        if len(args) != 2:
            msg = "Unexpected number of arguments, expected 2!"
            raise ValueError(msg)

        q_robot: np.ndarray = args[0]
        goal: DQ = args[1]

        x_current = self._panda_kin_dq.fkm(q_robot)
        j_m_task = np.squeeze(
            self._panda_rtb.jacob0(q_robot) @ self._panda_rtb.jacobm(q_robot), axis=-1
        )
        error, smooth_traj = super().step(x_current, goal, j_m_task)
        dot_x = vec8(error)
        j_pose = np.linalg.multi_dot(
            [haminus8(smooth_traj), C8(), self._panda_kin_dq.pose_jacobian(q_robot)]
        )

        return pinv(j_pose) @ dot_x
