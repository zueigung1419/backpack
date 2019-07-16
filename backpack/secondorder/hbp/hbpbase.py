from ...backpropextension import BackpropExtension
from ..strategies import BackpropStrategy
from ...context import get_from_ctx, set_in_ctx
from ...extensions import HBP


class HBPBase(BackpropExtension):
    MAT_NAME_IN_CTX = "_hbp_backpropagated_matrix"
    EXTENSION = HBP

    def __init__(self, params=None):
        if params is None:
            params = []
        super().__init__(self.get_module(), self.EXTENSION, params=params)

    def backpropagate(self, module, grad_input, grad_output):
        M = self.get_mat_from_ctx()

        if BackpropStrategy.is_batch_average():
            M_mod = self.backpropagate_batch_average(module, grad_input,
                                                     grad_output, M)

        elif BackpropStrategy.is_sqrt():
            M_mod = self.backpropagate_sqrt(module, grad_input, grad_output, M)

        self.set_mat_in_ctx(M_mod)

    def backpropagate_sqrt(self, module, grad_input, grad_output, H):
        return self.jac_t_mat_prod(module, grad_input, grad_output, H)

    def backpropagate_batch_average(self, module, grad_input, grad_output, H):
        return self.ea_jac_t_mat_jac_prod(module, grad_input, grad_output, H)

    def get_mat_from_ctx(self):
        return get_from_ctx(self.MAT_NAME_IN_CTX)

    def set_mat_in_ctx(self, mat):
        set_in_ctx(self.MAT_NAME_IN_CTX, mat)
