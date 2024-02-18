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

import os
from unittest import TestCase

import h5py
import numpy as np

from simulai.batching import batchdomain_constructor
from simulai.io import ByPassPreparer, Reshaper
from simulai.math.progression import gp
from simulai.metrics import L2Norm
from simulai.rom import IPOD
from simulai.simulation import Pipeline
from simulai.special import Scattering, bidimensional_map_nonlin_3, time_function
from simulai.utilities import make_temp_directory


class TestIPCADecomposition(TestCase):
    def setUp(self) -> None:
        self.N = 200

    """ Dataset constructed with an expression in which
        the variables are separable: U = exp(y)*cos(x)
    """

    def test_2D_separable_dataset(self) -> None:
        Nx = int(1e3)
        Ny = int(1e4)

        # Constructing dataset
        x = np.linspace(0, 1, Nx)
        y = np.linspace(0, 1, Ny)

        batch_sizes = gp(init=100, factor=10, n=3)

        for batch_size in batch_sizes:
            print(f"Using batch size as {batch_size}")

            batches = batchdomain_constructor([0, Ny], batch_size)

            with make_temp_directory() as tmp_dir:
                with h5py.File(
                    os.path.join(tmp_dir, f"test_data_{batch_size}.h5"), "w"
                ) as fp:
                    dataset = fp.create_dataset("data", shape=(Ny, Nx))

                    for j, batch in enumerate(batches):
                        print(f"Sub-domain {j}")

                        Y, X = np.meshgrid(y[slice(*batch)], x, indexing="ij")

                        dataset[slice(*batch)] = np.exp(Y) * np.cos(X)

                    N_components = [None] + gp(init=5, factor=2, n=4)

                    self._exec_IPCA_tests(dataset, N_components, batch_size, tmp_dir)

    def test_2D_non_separable_dataset(self) -> None:
        Nx = 64
        Ny = 64
        Nt = self.N

        x = np.linspace(0, 1, Nx)
        y = np.linspace(0, 1, Ny)
        t = np.linspace(0, 100, Nt)

        batch_sizes = gp(init=10, factor=2, n=3)

        for batch_size in batch_sizes:
            print(f"Using batch size as {batch_size}")

            batches = batchdomain_constructor([0, Ny], batch_size)

            with make_temp_directory() as tmp_dir:
                with h5py.File(
                    os.path.join(tmp_dir, f"test_data_{batch_size}.h5"), "w"
                ) as fp:
                    dataset = fp.create_dataset("data", shape=(Nt, Nx * Ny))

                    for j, batch in enumerate(batches):
                        print(f"Sub-domain {j}")

                        T, X, Y = np.meshgrid(t[slice(*batch)], x, y, indexing="ij")

                        generator = Scattering(
                            root=time_function, scatter_op=bidimensional_map_nonlin_3
                        )

                        Z_ = generator.exec(data=T, scatter_data=(X, Y, 0.5, 0.5))
                        Z_ *= generator.exec(data=T, scatter_data=(X, Y, 0.25, 0.25))

                        Z = Z_.reshape(-1, Z_.shape[1] * Z_.shape[2])

                        dataset[slice(*batch)] = Z

                    N_components = [None] + gp(init=1, factor=2, n=3)

                    self._exec_IPCA_tests(dataset, N_components, batch_size, tmp_dir)

    def test_2D_non_separable_structured_dataset(self) -> None:
        Nx = 64
        Ny = 64
        Nt = self.N

        x = np.linspace(0, 1, Nx)
        y = np.linspace(0, 1, Ny)
        t = np.linspace(0, 100, Nt)

        batch_sizes = gp(init=10, factor=2, n=3)

        with make_temp_directory() as tmp_dir:
            with h5py.File(os.path.join(tmp_dir, f"test_data.h5"), "w") as fp:
                dataset = fp.create_dataset(
                    "data",
                    shape=(Nt, Nx * Ny, 1),
                    dtype=[("Z_1", float), ("Z_2", float), ("Z_3", float)],
                )

                batches = batchdomain_constructor([0, Nt], batch_sizes[1])

                for j, batch in enumerate(batches):
                    print(f"Sub-domain {j}")

                    T, X, Y = np.meshgrid(t[slice(*batch)], x, y, indexing="ij")

                    generator = Scattering(
                        root=time_function, scatter_op=bidimensional_map_nonlin_3
                    )

                    Z_ = generator.exec(data=T, scatter_data=(X, Y, 0.5, 0.5))
                    Z_ *= generator.exec(data=T, scatter_data=(X, Y, 0.25, 0.25))

                    Z = Z_.reshape(-1, Z_.shape[1] * Z_.shape[2])

                    Z_array = np.core.records.fromarrays(
                        [Z[..., None], 2 * Z[..., None], 3 * Z[..., None]],
                        names=["Z_1", "Z_2", "Z_3"],
                        formats=["f8", "f8", "f8"],
                    )

                    dataset[slice(*batch)] = Z_array

                for batch_size in batch_sizes:
                    print(f"Using batch size as {batch_size}")

                    N_components = [None] + gp(init=1, factor=2, n=3)

                    self._exec_IPCA_tests_reshaper(
                        dataset, N_components, batch_size, tmp_dir
                    )

    def _exec_IPCA_tests(self, dataset, N_components, batch_size, save_path) -> None:
        train_factor = 0.6
        N_samples = dataset.shape[0]
        N_train = int(train_factor * N_samples)
        N_test = N_samples - N_train

        for n_components in N_components:
            rom_config = {"n_components": n_components, "mean_component": True}

            pipeline = Pipeline(
                stages=[
                    ("data_preparer", ByPassPreparer(channels_last=True)),
                    ("rom", IPOD(config=rom_config)),
                ],
                channels_last=True,
            )

            pipeline.exec(
                input_data=dataset, data_interval=[0, N_train], batch_size=batch_size
            )

            print("Testing to project.")
            projected = pipeline.project_data(
                data=dataset,
                data_interval=[N_train, N_train + N_test],
                batch_size=batch_size,
            )

            print("Testing to reconstruct.")
            reconstructed = pipeline.reconstruct_data(
                data=projected,
                data_interval=[0, N_test],
                batch_size=batch_size,
                dump_path=os.path.join(
                    save_path, f"reconstruct_data_{batch_size}_{n_components}.h5"
                ),
            )

            l2_norm = L2Norm()
            error = l2_norm(
                data=reconstructed,
                reference_data=dataset,
                relative_norm=True,
                data_interval=[N_train, N_train + N_test],
            )

            print(
                f"PCA projection error for one-dimensional case performed with {n_components} components: {100*error} %."
            )

    def _exec_IPCA_tests_reshaper(
        self, dataset, N_components, batch_size, save_path
    ) -> None:
        train_factor = 0.6
        N_samples = dataset.shape[0]
        N_train = int(train_factor * N_samples)
        N_test = N_samples - N_train
        variables_names = dataset.dtype.names

        for n_components in N_components:
            rom_config = {"n_components": n_components, "mean_component": True}

            pipeline = Pipeline(
                stages=[
                    ("data_preparer", Reshaper(channels_last=True)),
                    ("rom", IPOD(config=rom_config)),
                ],
                channels_last=True,
            )

            pipeline.exec(
                input_data=dataset, data_interval=[0, N_train], batch_size=batch_size
            )

            print("Testing to project.")
            projected = pipeline.project_data(
                data=dataset,
                data_interval=[N_train, N_train + N_test],
                variables_list=variables_names,
                batch_size=batch_size,
            )

            print("Testing to reconstruct.")
            reconstructed = pipeline.reconstruct_data(
                data=projected,
                data_interval=[0, N_test],
                batch_size=batch_size,
                variables_list=variables_names,
                dump_path=os.path.join(
                    save_path, f"reconstruct_data_{batch_size}_{n_components}.h5"
                ),
            )

            l2_norm = L2Norm()
            error = l2_norm(
                data=reconstructed,
                reference_data=dataset,
                relative_norm=True,
                data_interval=[N_train, N_train + N_test],
            )

            print(
                f"PCA projection error for one-dimensional case performed with {n_components} components: {100 * error} %."
            )
