"""
Compute the gradient with PyTorch and the gradient 2nd moment with BackPACK.
"""

from torch.nn import CrossEntropyLoss, Flatten, Linear, Sequential

from backpack import backpack, extend, extensions
from utils import load_mnist_data

B = 64
X, y = load_mnist_data(B)

print(f"# Gradient with PyTorch, gradient 2nd moment with BackPACK (B={B})")

model = Sequential(
    Flatten(),
    Linear(784, 10),
)
lossfunc = CrossEntropyLoss()

model = extend(model)
lossfunc = extend(lossfunc)

loss = lossfunc(model(X), y)

with backpack(extensions.SumGradSquared()):
    loss.backward()

for name, param in model.named_parameters():
    print(
        f"\n{name}:",
        f"\n\t.grad.shape:             {param.grad.shape}",
        f"\n\t.sum_grad_squared.shape: {param.sum_grad_squared.shape}",
        # f"\n\t.grad:                   {param.grad}",
        # f"\n\t.sum_grad_squared:       {param.sum_grad_squared}",
    )
