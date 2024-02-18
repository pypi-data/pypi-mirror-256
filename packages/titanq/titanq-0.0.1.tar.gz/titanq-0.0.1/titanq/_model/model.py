import io
import json
import logging
import numpy as np
import zipfile
from typing import Any, Dict, List, Tuple

from .errors import MaximumVariableLimitError, MissingVariableError, MissingObjectiveError, ObjectiveAlreadySetError, OptimizeError
from .objective import Objective, Target
from .optimize_response import OptimizeResponse
from .variable import VariableVector, Vtype
from .._client import api_model, Client
from .._storage import ManagedStorage, StorageClient

log = logging.getLogger("TitanQ")

_TITANQ_BASE_URL = "https://titanq.infinityq.io"


class Model:
    """
    Root object to define a problem to be optimize
    """

    def __init__(
        self,
        *,
        api_key: str,
        storage_client: StorageClient = None,
        base_server_url: str = _TITANQ_BASE_URL
        ) -> None:
        """
        Initiate the model depending on the provided arguments.

        If the storage_client is missing, the storage will be managed by titanQ.

        NOTE: the storage manged by titanQ supports weight matrices with a size up to 10k

        :param api_key: TitanQ api key to access the service.
        :param storage_client: Storage to choose in order to store some items
        :param base_server_url: titanQ server url
        """
        self._variables: VariableVector = None
        self._objective: Objective = None
        self._titanq_client = Client(api_key, base_server_url)

        # the user chose a managed storage or left it as default
        if storage_client is None:
            storage_client = ManagedStorage(self._titanq_client)

        self._storage_client = storage_client


    def add_variable_vector(self, name='', size=1, vtype=Vtype.BINARY):
        """
        Add a vector of variable to the model.

        :param name: The name given to this variable vector.
        :param size: The size of the vector.
        :param vtype: Type of the variables inside the vector.

        :raise MaximumVariableLimitError: If a variable is already defined.
        :raise ValueError: If the size of the vector is < 1.
        """
        if self._variables is not None:
            raise MaximumVariableLimitError("Cannot add additional variable without busting the maximum number of variable (1).")

        log.debug(f"add variable name='{name}'.")

        self._variables = VariableVector(name, size, vtype)


    def set_objective_matrices(self, weights: np.ndarray, bias: np.ndarray, target=Target.MINIMIZE):
        """
        Set the objective matrices for the model.

        :param weights: The quadratic objective matrix - a NumPy 2-D dense ndarray.
        :param bias: The linear constraint vector - a NumPy 1-D ndarray.
        :param target: The target of this objective matrix.

        :raise MissingVariableError: If no variable have been added to the model.
        :raise ObjectiveAlreadySetError: If an objective has already been setted in this model.
        :raise ValueError: If the weights shape or the bias shape does not fit the variable in the model.
        :raise ValueError: If the weights or bias data type is not f32.
        """

        if self._variables is None:
            raise MissingVariableError("Cannot set objective before adding a variable to the model.")

        if self._objective is not None:
            raise ObjectiveAlreadySetError("An objective has already have been set for this model.")

        log.debug(f"set objective matrix and bias vector.")

        self._objective = Objective(self._variables.size(), weights, bias, target)


    def optimize(self, *, beta=[0.1], coupling_mult=0.5, timeout_in_secs=10.0, num_chains=8, num_engines=1):
        """
        Optimize this model.

        Note: All the file used during the computation will be cleaned at the end.

        :param beta: beta hyper parameter used by the backend solver.
        :param coupling_mult: coupling_mult hyper parameter used by the backend solver.
        :param timeout_in_secs: Maximum time (in seconds) the backend solver can take to resolve this problem.
        :param num_chains: num_chains hyper parameter used by the backend solver.
        :param num_engines: num_engines parameter used by the backend solver.

        :raise MissingVariableError: If no variable have been added to the model.
        :raise MissingObjectiveError: If no variable have been added to the model.
        """
        if self._variables is None:
            raise MissingVariableError("Cannot optimize before adding a variable to the model.")

        if self._objective is None:
            raise MissingObjectiveError("Cannot optimize before adding an objective to the model.")

        result, metrics = self._solve(beta, coupling_mult, timeout_in_secs, num_chains, num_engines)

        return OptimizeResponse(self._variables.name(), result, metrics)

    def _solve(self,
            beta: List[float],
            coupling_mult: float,
            timeout_in_secs: float,
            num_chains: int,
            num_engines: int
        ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        issue a solve request and wait for it to complete.

        :param beta: beta hyper parameter used by the backend solver.
        :param coupling_mult: coupling_mult hyper parameter used by the backend solver.
        :param timeout_in_secs: Maximum time (in seconds) the backend solver can take to resolve this problem.
        :param num_chains: num_chains hyper parameter used by the backend solver.
        :param num_engines: num_engines parameter used by the backend solver.

        :return: the result numpy array and the metric json object
        """
        with self._storage_client.temp_files_manager(
            self._objective.bias(),
            self._objective.weights()
        ) as temp_files:
            request = api_model.SolveRequest(
                input=temp_files.input(),
                output=temp_files.output(),
                parameters=api_model.Parameters(
                    beta=beta,
                    coupling_mult=coupling_mult,
                    num_chains=num_chains,
                    num_engines=num_engines,
                    timeout_in_secs=timeout_in_secs,
                    variables_format=str(self._variables.vtype())
                )
            )

            solve_response = self._titanq_client.solve(request)

            # wait for result to be uploaded by the solver and download it
            archive_file_content = temp_files.download_result()
            with zipfile.ZipFile(io.BytesIO(archive_file_content), 'r') as zip_file:
                try:
                    metrics_content = zip_file.read("metrics.json")
                    result_content = zip_file.read("result.npy")
                except KeyError as ex:
                    raise OptimizeError(
                        "Unexpected error in the solver, please contact titanQ support for more help" \
                        f" and provide the following computation id {solve_response.computation_id}") from ex

        log.debug("Optimization completed")
        return np.load(io.BytesIO(result_content)), json.loads(metrics_content)
