from ...core.derivatives.mseloss import MSELossDerivatives
from ...core.derivatives.crossentropyloss import CrossEntropyLossDerivatives
from ..strategies import LossHessianStrategy
from .hbpbase import HBPBase


class HBPLoss(HBPBase):
    def __init__(self, params=None):
        super().__init__(params=params)

        self.LOSS_HESSIAN_GETTERS = {
            LossHessianStrategy.EXACT: self.sqrt_hessian,
            LossHessianStrategy.SAMPLING: self.sqrt_hessian_sampled,
            LossHessianStrategy.AVERAGE: self.sum_hessian,
        }

    def backpropagate(self, module, grad_input, grad_output):
        H_func = self.LOSS_HESSIAN_GETTERS[LossHessianStrategy.CURRENT]
        H_loss = H_func(module, grad_input, grad_output)

        self.set_mat_in_ctx(H_loss)


class HBPMSELoss(HBPLoss, MSELossDerivatives):
    pass


class HBPCrossEntropyLoss(HBPLoss, CrossEntropyLossDerivatives):
    pass


EXTENSIONS = [HBPCrossEntropyLoss(), HBPMSELoss()]
