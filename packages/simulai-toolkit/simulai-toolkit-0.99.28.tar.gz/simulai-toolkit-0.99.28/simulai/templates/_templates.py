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

import importlib
import warnings
from typing import Optional, Tuple, Union

import numpy as np
import torch
import scipy.sparse as sparse

from simulai.abstract import Regression

from ._pytorch_network import NetworkTemplate


class ReservoirComputing(Regression):
    def __init__(self, reservoir_dim=None, sparsity_level=None):
        super().__init__()

        self.sparsity_tolerance = 0.0025  # Default choice

        self.reservoir_dim = reservoir_dim

        self.sparsity_level = sparsity_level

    @property
    def _reservoir_dim_corrected_sparsity_level(self):
        # Guaranteeing a minimum sparsity tolerance
        dim = (
            max(self.sparsity_level, self.sparsity_tolerance)
            if self.reservoir_dim == 0
            else self.reservoir_dim
        )
        effective_sparsity = self.sparsity_level / dim
        if effective_sparsity < self.sparsity_tolerance:
            return self.sparsity_tolerance
        else:
            return self.sparsity_level / dim

    # It creates a sparse and randomly distributed reservoir matrix
    def create_reservoir(self, reservoir_dim=None):
        return sparse.rand(
            self.reservoir_dim,
            self.reservoir_dim,
            density=self._reservoir_dim_corrected_sparsity_level,
        )


class NetworkInstanceGen:

    """
    It generates instances of networks considering default choices
    """

    def __init__(
        self,
        architecture: str = None,
        dim: str = None,
        shallow: bool = False,
        use_batch_norm: bool = False,
        kernel_size: Optional[int] = None,
        unflattened_size: Tuple[int] = None,
        **kwargs,
    ) -> None:
        """

        Parameters
        ----------
        architecture : str
            The kind of network used, 'cnn' or 'dense'
        dim : str
            When 'cnn' is used as architecture, it is necessary to provide the dimensionality
            as an element of ['1d', '2d', '3d'].
        shallow : bool
            The network will be shallow or not.
        use_batch_norm : bool
            Batch normalization will be used or not.
        kernel_size : Optional[int]
            Convolutional kernel size.
        """

        self.shallow = shallow

        if architecture == "dense":
            if shallow == False:
                self.architecture = "DenseNetwork"
            else:
                self.architecture = "SLFNN"
        elif architecture == "cnn":
            self.architecture = "ConvolutionalNetwork"
        else:
            raise Exception(
                f"Option {architecture} for architecture is not supported."
                + f" It must be 'dense' or 'cnn'"
            )

        self.engine = "simulai.regression"

        self.engine_module = importlib.import_module(self.engine)
        self.architecture_class = getattr(self.engine_module, self.architecture)

        self.divisor = 2
        self.multiplier = 2

        self.use_batch_norm = use_batch_norm

        # It is still hard-coded
        self.interp_tag = {"1d": "linear", "2d": "bicubic", "3d": "trilinear"}

        if architecture == "cnn":
            assert dim in ["1d", "2d", "3d"], "dim must be in ['1d', '2d', '3d']. "

            self.dim = dim

            self.after_conv = "maxpool" + self.dim
            self.before_conv = "upsample"
            self.batch_norm = "batchnorm" + self.dim
            self.n_dims = int(self.dim[0])

            ### CNN specificities
            # Default number of channels used for the first layer of a convolutional
            # neural network
            self.channels = 16
            self.channels_multiplier = 2

            if kernel_size:
                self.kernel_size = kernel_size
                self.padding = "same"
            else:
                self.kernel_size = 3
                self.padding = 1

            self.stride = 1
            self.pool_kernel_size = 2
            self.pool_stride = 2

            self.scale_factor = 2
            self.mode = self.interp_tag.get(dim)
            self.channels_position = 1

        self.architecture_str = architecture
        self.unflattened_size = unflattened_size

    def _gen_dense_network(
        self,
        input_dim: int = None,
        output_dim: int = None,
        activation: str = None,
        name: str = None,
    ) -> dict:
        """
        Creating a configuration for instantiating a dense network.

        Parameters
        ----------
        input_dim : int
            Dimension for the input space.
        output_dim : int
            Dimension for the output space.
        activation : str
            The kind of activation being used.
        name : str
            A name for identifying the network.

        Returns
        -------
            A dictionary containing the configuration of the
            network.

        """
        assert type(input_dim) == int
        assert type(output_dim) == int
        assert type(activation) == str

        if self.shallow == True:
            config_dict = {
                "input_size": input_dim,
                "output_size": output_dim,
                "activation": "identity",
                "name": name,
            }

        else:
            # Creating the list of units
            ref = input_dim
            result = input_dim
            units_list = list()

            if input_dim > output_dim:
                while (ref % self.divisor < ref) and (
                    result > self.divisor * output_dim
                ):
                    result, remainder = divmod(ref, self.divisor)
                    ref = result
                    units_list.append(result)

            else:
                while result < int(output_dim / (self.multiplier)):
                    result *= self.multiplier

                    units_list.append(result)

            config_dict = {
                "layers_units": units_list,
                "activations": activation,
                "input_size": input_dim,
                "output_size": output_dim,
                "name": name,
            }

        return config_dict

    def _is_div_cnn_dims(self, dim: Tuple[int, ...]) -> bool:
        """
        Checking if the CNN dimension is divisible according to
        the default rule.

        Parameters
        ----------
        dim : Tuple[int, ...]
            The CNN input dimension
        Returns
        -------
            A boolean informing if is divisible or not.
        """

        reduce_dims = dim[2:]

        return all([idim % self.divisor == 0 for idim in reduce_dims])

    def _div_cnn_dims(self, dim: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        It creates the intermediary CNN dimensions according to the default
        dimensionality reduction rule.

        Parameters
        ----------
        dim : Tuple[int, ...]
            The dimension of the CNN input
        Returns
        -------
            A tuple containing the intermediary dimensions of the CNN network.
        """

        reduce_dims = dim[2:]

        return dim[:2] + tuple([int(idim / self.divisor) for idim in reduce_dims])

    def _multiply_cnn_dims(self, dim: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        It creates the intermediary CNN dimensions according to the default
        dimensionality increasing rule.

        Parameters
        ----------
        dim : Tuple[int, ...]
            The dimension of the CNN input
        Returns
        -------
            A tuple containing the intermediary dimensions of the CNN network.
        """

        reduce_dims = dim[2:]

        return dim[:2] + tuple([int(idim * self.multiplier) for idim in reduce_dims])

    def _gen_cnn_layer_increase_dimensionality(
        self, channels_in: int = None, channels_out: int = None
    ) -> dict:
        """
        It creates the layers configuration dictionary
        used for instantiating CNN networks which perform dimensionality amplification.

        Parameters
        ----------
        channels_in : int
            Number of channels at the input.
        channels_out : int
            Number of channels at the output

        Returns
        -------
            A dictionary containing the configuration used to instantiate the
            network layers.
        """

        if channels_out == None:
            if channels_in > 1:
                channels_out = int(channels_in / self.channels_multiplier)
            else:
                channels_out = channels_in

        layer_input = {
            "in_channels": channels_in,
            "out_channels": channels_out,
            "kernel_size": self.kernel_size,
            "stride": self.stride,
            "padding": self.padding,
            "before_conv": {
                "type": self.before_conv,
                "scale_factor": self.scale_factor,
                "mode": self.mode,
            },
        }

        if self.use_batch_norm:
            batch_norm_input = {
                "type": self.batch_norm,
                "num_features": channels_out,
            }

            layer_input["batch_norm"] = batch_norm_input

        return layer_input

    def _gen_cnn_layer_reduce_dimensionality(
        self, channels_in: int = None, channels_out: int = None
    ) -> dict:
        """
        It creates the layers configuration dictionary used
        for instantiating CNN networks which perform dimensionality reduction.

        Parameters
        ----------
        channels_in : int
            Number of channels at the input.
        channels_out : int
            Number of channels at the output

        Returns
        -------
            A dictionary containing the configuration used to instantiate the
            network layers.
        """

        if channels_out == None:
            channels_out = channels_in * self.channels_multiplier

        layer_input = {
            "in_channels": channels_in,
            "out_channels": channels_out,
            "kernel_size": self.kernel_size,
            "stride": self.stride,
            "padding": self.padding,
            "after_conv": {
                "type": self.after_conv,
                "kernel_size": self.pool_kernel_size,
                "stride": self.pool_stride,
            },
        }

        if self.use_batch_norm:
            batch_norm_input = {
                "type": self.batch_norm,
                "num_features": channels_out,
            }

            layer_input["batch_norm"] = batch_norm_input

        return layer_input

    def _gen_cnn_network_reduce(
        self,
        input_dim: Tuple[int, ...] = None,
        output_dim: Optional[Tuple[int, ...]] = None,
        activation: str = None,
        name: str = None,
        **kwargs,
    ) -> dict:
        """
        It creates a configuration dictionary to instantiate a CNN network
        aimed at performing dimensionality reduction.

        Parameters
        ----------
        input_dim : Tuple[int, ...]
            The CNN input dimension.
        output_dim : Optional[Tuple[int, ...]]
            The CNN output dimension.
        activation : str
            The kind of activation function used.
        name : str
            A name for identifying the model.

        Returns
        -------
            A complete configuration dictionary to instantiate the
            CNN network.
        """

        assert type(input_dim) == tuple
        assert type(activation) == str

        layers_list = list()
        ref_dim = input_dim
        channels = input_dim[self.channels_position]
        layer_count = 0

        while self._is_div_cnn_dims(ref_dim):
            if layer_count == 0:
                channels_out = self.channels
            else:
                channels_out = None

            layer = self._gen_cnn_layer_reduce_dimensionality(
                channels_in=channels, channels_out=channels_out
            )

            channels = layer["out_channels"]

            layers_list.append(layer)

            ref_dim = self._div_cnn_dims(ref_dim)

            layer_count += 1

        config_dict = {
            "layers": layers_list,
            "activations": activation,
            "case": self.dim,
            "name": name,
        }

        config_dict.update(kwargs)

        return config_dict

    def _gen_cnn_network_increase(
        self,
        input_dim: Union[int, Tuple[int, ...]] = None,
        output_dim: Tuple[int, ...] = None,
        activation: str = None,
        name: str = None,
        **kwargs,
    ) -> dict:
        """
        It creates a configuration dictionary to instantiate a CNN network.
        aimed at performing dimensionality increase.

        Parameters
        ----------
        input_dim : Tuple[int, ...]
            The CNN input dimension.
        output_dim : Optional[Tuple[int, ...]]
            The CNN output dimension.
        activation : str
            The kind of activation function used.
        name : str
            A name for identifying the model.

        Returns
        -------
            A complete configuration dictionary to instantiate the
            CNN network.
        """

        assert type(input_dim) in (int, tuple)
        assert type(output_dim) == tuple
        assert type(activation) == str

        layers_list = list()

        layer_count = 0

        if type(input_dim) == int:
            if self.unflattened_size:
                unflatten_layer = torch.nn.Unflatten(
                    dim=1, unflattened_size=self.unflattened_size
                )
            else:
                unflatten_layer = torch.nn.Unflatten(
                    dim=1, unflattened_size=(input_dim,) + self.n_dims * (1,)
                )
        else:
            unflatten_layer = None

        if type(input_dim) == tuple:
            channels = input_dim[self.channels_position]
            ref_dim = input_dim
        else:
            if self.unflattened_size:
                ref_dim = (None,) + self.unflattened_size
                channels = self.unflattened_size[0]
            else:
                ref_dim = (
                    None,
                    input_dim,
                ) + self.n_dims * (1,)
                channels = input_dim

        while not (sum(ref_dim[2:]) >= int(sum(output_dim[2:]) / self.multiplier)):
            layer = self._gen_cnn_layer_increase_dimensionality(channels_in=channels)

            channels = layer["out_channels"]

            layers_list.append(layer)

            ref_dim = self._multiply_cnn_dims(ref_dim)

            layer_count += 1

        layer = self._gen_cnn_layer_increase_dimensionality(
            channels_in=channels, channels_out=self.channels
        )
        layers_list.append(layer)

        config_dict = {
            "layers": layers_list,
            "activations": activation,
            "case": self.dim,
            "name": name,
        }

        if isinstance(unflatten_layer, torch.nn.Module):
            config_dict["pre_layer"] = unflatten_layer

        config_dict.update(kwargs)

        return config_dict

    def __call__(
        self,
        input_dim: Union[int, Tuple[int, ...]] = None,
        output_dim: Union[int, Tuple[int, ...]] = None,
        activation: str = None,
        channels: int = None,
        name: str = None,
        reduce_dimensionality: bool = True,
        **kwargs,
    ) -> NetworkTemplate:
        """
        The execution method.

        Parameters
        ----------
        input_dim : Union[int, Tuple[int, ...]]
            Dimension of the network input.
        output_dim : Union[int, Tuple[int, ...]]
            Dimension of the network output.
        activation : str
            The kind of activation used in network layers.
        channels : int
            Number of channels (ised just in case of CNN networks).
        name : str
            A name for identifying the network.
        reduce_dimensionality : bool
            Reducing dimensionality or not.

        Returns
        -------
            An instance of neural network created in accordance with
            the provided configurations.
        """

        # Selecting the architecture generator function to be used.
        if self.architecture_str == "cnn":
            if reduce_dimensionality == True:
                self.method_tag = "_reduce"
            else:
                self.method_tag = "_increase"
        else:
            self.method_tag = ""

        gen_network_name = f"_gen_{self.architecture_str}_network{self.method_tag}"

        gen_network = getattr(self, gen_network_name)

        if name == None:
            name = "net" + str(id(self))
        else:
            pass

        if self.architecture_str == "cnn":
            if channels == None:
                warnings.warn(
                    "As no value was provided for 'channels',"
                    + f" the default value of {self.channels} is being used. "
                )
            else:
                self.channels = channels

        config_dict = gen_network(
            input_dim=input_dim,
            output_dim=output_dim,
            activation=activation,
            name=name,
            **kwargs,
        )

        return self.architecture_class(**config_dict)


# Templates used for creating autoencoders using automatically
# generated configurations


# MLP autoencoder
def mlp_autoencoder_auto(
    input_dim: int = None,
    latent_dim: int = None,
    output_dim: Optional[int] = None,
    activation: str = None,
    shallow: bool = False,
    name: str = None,
) -> Tuple[NetworkTemplate, ...]:
    """
    Template for easily instantiating a MLP (dense) autoencoder.

    Parameters
    ----------
    input_dim : int
        The autoencoder input dimension.
    latent_dim : int
        Dimension of the autoencoder latent (or embedding) dimension.
    output_dim : Optional[int]
        The autoencoder output dimension. If 'None', it will considered
        as equal to 'input_dim'.
    activation : str
        The kind of activation function used in the autoencoder.
    shallow : bool
        Using a shallow bottleneck autoencoder or not.
    name : str
        A name for identifying the model.

    Returns
    -------
        A tuple of network instances, corresponding to the encoder and the decoder,
        respectively.
    """

    from simulai.templates import NetworkInstanceGen

    msg = (
        "If no encoder and decoder networks are provided, it is necessary to "
        "provide values for input_dim, latent_dim and output_dim in order to"
        "automatically construct the autoencoder."
    )

    if output_dim == None:
        print(
            "As no output_dim was provided, it is considered an identity autoencoder, so"
            + "output_dim == input_dim"
        )

        output_dim = input_dim

    assert type(input_dim) == type(output_dim) == type(latent_dim) == int, msg
    assert (
        type(activation) == str
    ), "It is necessary to provide a value for the activation"

    autogen = NetworkInstanceGen(architecture="dense", shallow=shallow)

    # Default choice for the model name
    if name == None:
        name = "mlp_autoencoder"

    encoder = autogen(
        input_dim=input_dim,
        output_dim=latent_dim,
        activation=activation,
        name="encoder_" + name,
    )
    decoder = autogen(
        input_dim=latent_dim,
        output_dim=output_dim,
        activation=activation,
        name="decoder_" + name,
    )

    return encoder, decoder


# CNN autoencoder
def cnn_autoencoder_auto(
    input_dim: Tuple[int, ...] = None,
    latent_dim: int = None,
    output_dim: Optional[Tuple[int, ...]] = None,
    activation: str = None,
    channels: int = None,
    kernel_size: Optional[int] = None,
    case: str = None,
    use_batch_norm: bool = False,
    shallow: bool = False,
    name: str = None,
    **kwargs,
) -> Tuple[NetworkTemplate, ...]:
    """
    A template for easily instantiating a CNN autoencoder

    Parameters
    ----------
    input_dim : Tuple[int, ...]
        The autoencoder input dimension.
    latent_dim : int
        The autoencoder latent (or embedding) dimension.
    output_dim : Optional[Tuple[int, ...]]
        The autoencoder output dimension.
    activation : str
        The activation function used in the autoencoder.
    channels : int
        The initial number of channels (filters).
    kernel_size : Optional[int]
        Size of the convolution kernel
    case : str
        The kind of convolution used: case in ['1d', '2d', '3d']
    use_batch_norm : bool
        Using batch normalization or not.
    shallow : bool
        Using a shallow bottleneck autoencoder or not.
    name : str
        A name for identifying the model.

    Returns
    -------
        A tuple of network instances, corresponding to the encoder and the decoder,
        respectively.

    """

    from simulai.templates import NetworkInstanceGen

    msg = (
        "If no encoder and decoder networks are provided, it is necessary to "
        "provide values for input_dim, latent_dim and output_dim in order to"
        "automatically construct the autoencoder."
    )

    if output_dim == None:
        print(
            "As no output_dim was provided, it is considered an identity autoencoder, so"
            + "output_dim == input_dim"
        )

        output_dim = input_dim

    assert type(input_dim) == type(output_dim) == tuple, msg
    assert type(latent_dim) == int, msg
    assert (
        type(activation) == str
    ), "It is necessary to provide a value for the activation"
    assert (
        type(case) == str
    ), "It is necessary to provide a value for the dimensional case"

    last_channels = output_dim[1]

    autogen_cnn = NetworkInstanceGen(
        architecture="cnn",
        dim=case,
        use_batch_norm=use_batch_norm,
        kernel_size=kernel_size,
        **kwargs,
    )

    autogen_dense = NetworkInstanceGen(architecture="dense", shallow=shallow)

    # Default choice for the model name
    if name == None:
        name = "cnn_autoencoder"

    encoder = autogen_cnn(
        input_dim=input_dim,
        activation=activation,
        channels=channels,
        flatten=False,
        name="cnn_encoder_" + name,
    )

    encoder.summary(input_shape=list(input_dim), display=False)

    # Product of the collapsible dimensions
    dense_input_size = int(np.prod(encoder.output_size[1:]))

    bottleneck_encoder = autogen_dense(
        input_dim=dense_input_size,
        output_dim=latent_dim,
        activation=activation,
        name="dense_encoder_" + name,
    )

    bottleneck_decoder = autogen_dense(
        input_dim=latent_dim,
        output_dim=dense_input_size,
        activation=activation,
        name="dense_decoder_" + name,
    )

    decoder = autogen_cnn(
        input_dim=encoder.output_shape,
        output_dim=output_dim,
        activation=activation,
        channels=last_channels,
        flatten=False,
        reduce_dimensionality=False,
        name="cnn_decoder_" + name,
    )

    return encoder, decoder, bottleneck_encoder, bottleneck_decoder


def autoencoder_auto(
    input_dim: Union[int, Tuple[int, ...]] = None,
    latent_dim: int = None,
    output_dim: Optional[Union[int, Tuple[int, ...]]] = None,
    activation: str = None,
    channels: int = None,
    kernel_size: Optional[int] = None,
    architecture: str = None,
    shallow: bool = False,
    use_batch_norm: bool = False,
    case: str = None,
    name: str = None,
    **kwargs,
) -> Tuple[Union[NetworkTemplate, None], ...]:
    """
    A higher level template for easily instantiating an autoencoder,
    both CNN and MLP.

    Parameters
    ----------
    input_dim : Tuple[int, ...]
        The autoencoder input dimension.
    latent_dim : int
        The autoencoder latent (or embedding) dimension.
    output_dim : Optional[Tuple[int, ...]]
        The autoencoder output dimension.
    activation : str
        The activation function used in the autoencoder.
    channels : int
        The initial number of channels (filters). Applicable for 'architecture' ='cnn'.
    kernel_size : Optional[int]
        Convolutional kernel size.
    architecture : str
        The kind of architecture used, 'cnn' or 'dense'.
    case : str
        The kind of convolution used: case in ['1d', '2d', '3d']
    use_batch_norm : bool
        Using batch normalization or not.
    shallow : bool
        Using a shallow bottleneck autoencoder or not.
    name : str
        A name for identifying the model.

    Returns
    -------
        A tuple of network instances, corresponding to the encoder and the decoder,
        respectively. When the architecture is not supported, it returns 'None'.

    Raises
    ------
    Exception :
        When the architecture is not supported: 'architecture' not in ['cnn', 'dense'].
    """

    if architecture == "dense":
        encoder, decoder = mlp_autoencoder_auto(
            input_dim=input_dim,
            latent_dim=latent_dim,
            output_dim=output_dim,
            activation=activation,
            shallow=shallow,
            name=name,
        )

        return encoder, decoder, None, None

    elif architecture == "cnn":
        encoder, decoder, bottleneck_encoder, bottleneck_decoder = cnn_autoencoder_auto(
            input_dim=input_dim,
            latent_dim=latent_dim,
            output_dim=output_dim,
            activation=activation,
            channels=channels,
            kernel_size=kernel_size,
            case=case,
            shallow=shallow,
            use_batch_norm=use_batch_norm,
            name=name,
            **kwargs,
        )

        return encoder, decoder, bottleneck_encoder, bottleneck_decoder

    else:
        raise Exception(f"The architecture {architecture} is not supported.")
