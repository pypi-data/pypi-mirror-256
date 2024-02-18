# (C) Copyright IBM Corp. 2019, 2020, 2021, 2022.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#           http://www.apache.org/licenses/LICENSE-2.0

#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from unittest import TestCase
from typing import Optional
import numpy as np
from tests.config import configure_dtype

torch = configure_dtype()

from utils import configure_device

DEVICE = configure_device()


# Model template
def model(
    product_type=None,
    multiply_by_trunk: bool = False,
    n_outputs: int = 4,
    use_bias: bool = False,
    residual: bool = False,
):
    from simulai.models import FlexibleDeepONet
    from simulai.regression import DenseNetwork

    n_inputs_t = 1
    n_inputs_b = 4
    n_latent = 100

    if product_type == None:
        output_size = n_latent * n_outputs
    else:
        output_size = n_latent

    if use_bias == True:
        extra_dim = n_outputs
    else:
        extra_dim = 0

    # Configuration for the fully-connected trunk network
    trunk_config = {
        "layers_units": 7 * [100],  # Hidden layers
        "activations": "tanh",
        "input_size": n_inputs_t,
        "output_size": output_size,
        "name": "trunk_net",
    }

    pre_config = {
        "layers_units": 2 * [100],  # Hidden layers
        "activations": "tanh",
        "input_size": n_inputs_b,
        "output_size": 2 * n_inputs_t,
        "name": "trunk_net",
    }

    # Configuration for the fully-connected branch network
    branch_config = {
        "layers_units": 7 * [100],  # Hidden layers
        "activations": "tanh",
        "input_size": n_inputs_b,
        "output_size": n_latent * n_outputs + extra_dim,
        "name": "branch_net",
    }

    # Instantiating and training the surrogate model
    trunk_net = DenseNetwork(**trunk_config)
    pre_net = DenseNetwork(**pre_config)
    branch_net = DenseNetwork(**branch_config)

    net = FlexibleDeepONet(
        trunk_network=trunk_net,
        branch_network=branch_net,
        pre_network=pre_net,
        var_dim=n_outputs,
        multiply_by_trunk=multiply_by_trunk,
        product_type=product_type,
        residual=residual,
        model_id="net",
        use_bias=use_bias,
    )

    return net


class TestImprovedDeeponet(TestCase):
    def setUp(self) -> None:
        pass

    def test_deeponet_forward(self):
        for device in ["cpu", "gpu", None]:
            net = model()
            net.summary()

            # Checking if the model is coretly placed when no device is
            # informed
            if not device:
                assert net.device == "cpu", (
                    "When no device is provided it is expected the model"
                    + f"being on cpu, but received {net.device}."
                )

            data_trunk = torch.rand(1_000, 1)
            data_branch = torch.rand(1_000, 4)

            print(f"Network has {net.n_parameters} parameters.")

            output = net.forward(input_trunk=data_trunk, input_branch=data_branch)

            assert output.shape[1] == 4, "The network output is not like expected."

            output = net.eval_subnetwork(
                name="trunk", trunk_data=data_trunk, branch_data=data_branch
            )
            assert output.shape[1] == 400, "The network output is not like expected."
            assert isinstance(output, np.ndarray)

            output = net.eval_subnetwork(
                name="branch", trunk_data=data_trunk, branch_data=data_branch
            )
            assert output.shape[1] == 400, "The network output is not like expected."
            assert isinstance(output, np.ndarray)

            output = net.eval_subnetwork(
                name="pre", trunk_data=data_trunk, branch_data=data_branch
            )
            assert output.shape[1] == 2, "The network output is not like expected."
            assert isinstance(output, np.ndarray)

    def test_deeponet_train(self):
        from simulai.optimization import Optimizer

        optimizer_config = {"lr": 1e-3}

        data_trunk = torch.rand(1_000, 1)
        data_branch = torch.rand(1_000, 4)
        output_target = torch.rand(1_000, 2)

        n_epochs = 10
        maximum_values = (1 / np.linalg.norm(output_target, 2, axis=0)).tolist()
        params = {"lambda_1": 0.0, "lambda_2": 1e-10, "weights": maximum_values}

        input_data = {"input_branch": data_branch, "input_trunk": data_trunk}

        optimizer = Optimizer("adam", params=optimizer_config)

        for product_type in [None, "dense"]:
            for multiply_by_trunk in [True, False]:
                print(
                    f"Multiply by trunk: {multiply_by_trunk}, Product type: {product_type}"
                )

                net = model(
                    multiply_by_trunk=multiply_by_trunk, product_type=product_type
                )

                optimizer.fit(
                    op=net,
                    input_data=input_data,
                    target_data=output_target,
                    n_epochs=n_epochs,
                    loss="wrmse",
                    params=params,
                    device=DEVICE,
                )

                output = net.forward(input_trunk=data_trunk, input_branch=data_branch)

                assert output.shape[1] == 4, "The network output is not like expected."

            for use_bias in [False]:
                print(f"use_bias: {use_bias}, Product type: {product_type}")

                net = model(use_bias=use_bias, product_type=product_type)

                optimizer.fit(
                    op=net,
                    input_data=input_data,
                    target_data=output_target,
                    n_epochs=n_epochs,
                    loss="wrmse",
                    params=params,
                    device=DEVICE,
                )

                output = net.forward(input_trunk=data_trunk, input_branch=data_branch)

                assert output.shape[1] == 4, "The network output is not like expected."

    # Vanilla DeepONets are single output
    def test_vanilla_deeponet_train(self):
        from simulai.optimization import Optimizer

        optimizer_config = {"lr": 1e-3}

        data_trunk = torch.rand(1_000, 1)
        data_branch = torch.rand(1_000, 4)
        output_target = torch.rand(1_000, 1)

        n_epochs = 1_00
        maximum_values = (1 / np.linalg.norm(output_target, 2, axis=0)).tolist()
        params = {"lambda_1": 0.0, "lambda_2": 1e-10, "weights": maximum_values}

        input_data = {"input_branch": data_branch, "input_trunk": data_trunk}

        optimizer = Optimizer("adam", params=optimizer_config)

        net = model(n_outputs=1)

        optimizer.fit(
            op=net,
            input_data=input_data,
            target_data=output_target,
            n_epochs=n_epochs,
            loss="wrmse",
            params=params,
            device=DEVICE,
        )

        output = net.forward(input_trunk=data_trunk, input_branch=data_branch)

        assert output.shape[1] == 1, "The network output is not like expected."
