# qiskit_transpiler_service

A library to use [Qiskit Transpiler service](https://docs.quantum.ibm.com/transpile/qiskit-transpiler-service) and the [AI transpiler passes](https://docs.quantum.ibm.com/transpile/ai-transpiler-passes).

**Note** The Qiskit transpiler service and the AI transpiler passes use different experimental services that are only available for IBM Quantum Premium Plan users. This library and the releated services are an alpha release, subject to change.

## Installing the qiskit-transpiler-service

To use the Qiskit transpiler service, install the `qiskit-transpiler-service` package:

```sh
pip install qiskit-transpiler-service
```

By default, the package tries to authenticate to IBM Quantum services with the defined Qiskit API token, and uses your token from the `QISKIT_IBM_TOKEN` environment variable or from the file `~/.qiskit/qiskit-ibm.json` (under the section `default-ibm-quantum`).

## How to use the library?

### Using the Qiskit Transpiler service

The following examples demonstrate how to transpile circuits using the Qiskit transpiler service with different parameters.

1. Create a random circuit and call the Qiskit transpiler service to transpile the circuit with `ibm_cairo` as the `target`, 1 as the `optimization_level`, and not using AI during the transpilation.

    ```python
    from qiskit.circuit.random import random_circuit
    from qiskit_transpiler_service.transpiler_service import TranspilerService

    random_circ = random_circuit(5, depth=3, seed=42).decompose(reps=3)

    cloud_transpiler_service = TranspilerService(
        target="ibm_cairo",
        ai=False,
        optimization_level=1,
    )
    transpiled_circuit = cloud_transpiler_service.run(random_circ)
    ```

_Note:_ you only can use `target` devices you are allowed to with your IBM Quantum Account. Apart from the `target`, the `TranspilerService` also allows coupling_map as parameter.

2. Produce a similar random circuit and transpile it, requesting AI transpiling capabilities by setting the flag `ai` to `True`:

    ```python
    from qiskit.circuit.random import random_circuit
    from qiskit_transpiler_service.transpiler_service import TranspilerService

    random_circ = random_circuit(5, depth=3, seed=42).decompose(reps=3)

    cloud_transpiler_service = TranspilerService(
        target="ibm_cairo",
        ai=True,
        optimization_level=1,
    )
    transpiled_circuit = cloud_transpiler_service.run(random_circ)
    ```

### Using the AIRouting pass manually

The `AIRouting` pass acts both as a layout stage and a routing stage. It can be used within a `PassManager` as follows:

```python
from qiskit.transpiler import PassManager
from qiskit_transpiler_service.ai.routing import AIRouting
from qiskit.circuit.library import EfficientSU2

ai_passmanager = PassManager([
  AIRouting(target="ibm_sherbrooke", optimization_level=2, layout_mode="optimize")
])

circuit = EfficientSU2(120, entanglement="circular", reps=1).decompose()

transpiled_circuit = ai_passmanager.run(circuit)
```

Here, the `target` determines which backend to route for, the `optimization_level` (1, 2, or 3) determines the computational effort to spend in the process (higher usually gives better results but takes longer), and the `layout_mode` specifies how to handle the layout selection.
The `layout_mode` includes the following options:

- `keep`: This respects the layout set by the previous transpiler passes (or uses the trivial layout if not set). It is typically only used when the circuit must be run on specific qubits of the device. It often produces worse results because it has less room for optimization.
- `improve`: This uses the layout set by the previous transpiler passes as a starting point. It is useful when you have a good initial guess for the layout; for example, for circuits that are built in a way that approximately follows the device's coupling map. It is also useful if you want to try other specific layout passes combined with the `AIRouting` pass.
- `optimize`: This is the default mode. It works best for general circuits where you might not have good layout guesses. This mode ignores previous layout selections.
