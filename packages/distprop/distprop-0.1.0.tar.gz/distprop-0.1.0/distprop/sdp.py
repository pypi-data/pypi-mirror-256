import torch
import numpy as np

# PyTorch SDP wrapper implementation.  (tested with PyTorch version 1.13.1)


class SDP(torch.nn.Module):
    def __init__(self, net, std=1., num_outputs=10, create_graph=True, vectorize=False):
        super(SDP, self).__init__()
        self.net = net
        self.std = std
        self.num_outputs = num_outputs
        self.create_graph = create_graph
        self.vectorize = vectorize
        # vectorize=True is only faster for large numbers of classes / small models

    def forward(self, x):
        assert len(x.shape) >= 2, x.shape  # First dimension is a batch dimension.

        # Two separate implementations:
        # the top one is for larger models and the bottom for smaller models.
        if not self.vectorize:
            x.requires_grad_()
            y = self.net(x)
            jacs = []
            for i in range(self.num_outputs):
                jacs.append(torch.autograd.grad(
                    y[:, i].sum(0), x,
                    create_graph=self.create_graph, retain_graph=True
                )[0])
            jac = torch.stack(jacs, dim=1).reshape(
                x.shape[0], self.num_outputs, np.prod(x.shape[1:])
            )

        else:
            e = torch.zeros(x.shape[0] * self.num_outputs, self.num_outputs).to(x.device)
            for out_dim_idx in range(self.num_outputs):
                e[x.shape[0] * out_dim_idx:x.shape[0] * (out_dim_idx + 1), out_dim_idx] = 1.
            vjps = torch.autograd.functional.vjp(
                self.net, x.repeat(self.num_outputs, *[1] * (len(x.shape) - 1)), v=e,
                create_graph=self.create_graph, strict=True
            )
            y = vjps[0][:x.shape[0]]
            jac = vjps[1].view(
                self.num_outputs, x.shape[0], np.prod(x.shape[1:])).transpose(0, 1)

        cov = torch.bmm(jac, jac.transpose(-2, -1)) * self.std ** 2

        return y, cov


if __name__ == '__main__':
    # Usage example
    model = torch.nn.Sequential(
        torch.nn.Linear(4, 100),
        torch.nn.ReLU(),
        torch.nn.Linear(100, 100),
        torch.nn.ReLU(),
        torch.nn.Linear(100, 3),
    )
    data = torch.randn(10, 4)

    sdp_model = SDP(model, std=0.1, num_outputs=3)
    output_mean, output_cov = sdp_model(data)
    print(output_mean.shape, output_cov.shape)
