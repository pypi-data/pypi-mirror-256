"""DC analyses."""

import abc
from functools import cache
import numpy as np
from numpy.linalg.linalg import LinAlgError
import scipy.sparse
import scipy.sparse.linalg
import xarray as xr
from .util import create_axis
from ..components import NodeType, VSource, ISource
from ..solutions import OperatingPointSolution, SweepSolution
from ..library.constants import TREF
from ..library.materials import Vth


class Analysis(metaclass=abc.ABCMeta):
    def __init__(self, circuit, er=1e-3, ea=1e-9, eresiduals=1e-6):
        self.circuit = circuit
        self.er = er
        self.ea = ea
        self.eresiduals = eresiduals

    @property
    def nnodes(self):
        return len(self.circuit.nodes)

    @property
    def dim_size(self):
        # Required KCL and KVL equations for the circuit.
        return self.nnodes + len(self.circuit.current_nodes)

    @property
    def reduced_dim_size(self):
        """Dimension size with ground nodes removed."""
        return self.dim_size - 1

    @cache
    def _map_component_nodes(self):
        current_node_indices = {"gnd": 0}  # Force gnd to be first index.
        voltage_node_indices = {}
        component_node_indices = {}
        next_index = 1

        # KCL (node voltages).
        for component in self.circuit.component_nodes:
            for name, node in zip(self.circuit.component_nodes[component], component.voltage_nodes):
                if name not in current_node_indices:
                    current_node_indices[name] = next_index
                    next_index += 1

                component_node_indices[node] = current_node_indices[name]

        # KVL (component currents).
        for component in self.circuit.component_nodes:
            for node in component.current_nodes:
                # Don't need to check for existing nodes because they can't be shared.
                name = component.name
                voltage_node_indices[name] = next_index
                next_index += 1

                component_node_indices[node] = voltage_node_indices[name]

        assert len(current_node_indices) == self.nnodes
        assert len(voltage_node_indices) == len(self.circuit.current_nodes)
        return current_node_indices, voltage_node_indices, component_node_indices

    @cache
    def current_node_indices(self, reduced):
        current_node_indices, _, _ = self._map_component_nodes()

        if reduced:
            # Remove the ground node, and compensate remaining indices.
            current_node_indices = {
                name: index - 1 for name, index in current_node_indices.items()
                if name != "gnd"
            }

        return current_node_indices

    @cache
    def voltage_node_indices(self, reduced):
        _, voltage_node_indices, _ = self._map_component_nodes()

        if reduced:
            # Compensate non-ground indices.
            voltage_node_indices = {
                name: index - 1 for name, index in voltage_node_indices.items()
            }

        return voltage_node_indices

    @cache
    def component_node_indices(self, reduced):
        _, _, component_node_indices = self._map_component_nodes()

        if reduced:
            # Compensate non-ground indices.
            component_node_indices = {
                node: index - 1 for node, index in component_node_indices.items()
                if not self.node_is_ground(node)
            }

        return component_node_indices

    @cache
    def node_description_indices(self, reduced):
        """Map of matrix indices to what they represent.

        This is typically used for error messages.
        """
        return {
            **dict(zip(self.current_node_indices(reduced).values(), self.current_node_indices(reduced).keys())),
            **dict(zip(self.voltage_node_indices(reduced).values(), self.voltage_node_indices(reduced).keys()))
        }

    def node_is_ground(self, node):
        return self.component_node_indices(False)[node] == 0

    def fill_mna_matrix(self, mna):
        """Generate modified nodal analysis matrix."""
        for component in self.circuit.components.values():
            for nin, nout, coefficient in component.dc_couplings():
                # Map the component's own node indices to the global circuit ones.
                globalidxin = self.component_node_indices(False)[nin]
                globalidxout = self.component_node_indices(False)[nout]
                mna[globalidxin, globalidxout] += coefficient

        return mna

    def fill_sources_matrix(self, sources):
        """Generate sources matrix."""
        for component in self.circuit.components.values():
            for node, coefficient in component.dc_current_sources():
                # Map the component's node index to the global circuit one.
                globalidx = self.component_node_indices(False)[node]
                sources[globalidx, 0] += coefficient

        return sources

    @property
    def use_sparse(self):
        return self.reduced_dim_size > 300

    def converged(self, x, dx, residuals):
        """Perform a convergence check
        **Parameters:**
        x : array-like
            The results to be checked.
        dx : array-like
            The last increment from a Newton-Rhapson iteration, solving
            ``F(x) = 0``.
        residuals : array-like
            The remaining error, ie ``F(x) = residdum``
        ea : float
            The value to be employed for the absolute error.
        er : float
            The value for the relative error to be employed.
        eresiduals : float
            The maximum allowed error for the residuals (left over error).
        **Returns:**
        chk : boolean
            Whether the check was passed or not. ``True`` means 'convergence!'.
        rbn : ndarray
            The convergence check results by node, if ``debug`` was set to ``True``,
            else ``None``.
        """
        # This code only works properly when we're dealing with (n×1) arrays.
        assert x.shape[1] == dx.shape[1] == residuals.shape[1] == 1

        return np.logical_and(
            np.abs(dx) < (self.er * np.abs(x) + self.ea),
            np.abs(residuals) < self.eresiduals
        )


class OperatingPoint(Analysis):
    def run(self, x=None, **kwargs):
        # Initial x vector guess. This contains the values at each node. If not specified, it's
        # set to zero.
        if x is None:
            x = np.zeros((self.reduced_dim_size, 1))

        residuals = np.zeros((self.reduced_dim_size, 1))
        is_converged, iterations = self.solve(x, residuals, **kwargs)

        node_voltage_indices = list(self.current_node_indices(True).values())
        component_current_indices = list(self.voltage_node_indices(True).values())

        # Split the node voltage and component current outputs into separate arrays.
        voltages = np.take(x, node_voltage_indices)
        currents = np.take(x, component_current_indices)

        return OperatingPointSolution(
            data=xr.Dataset(
                {
                    "voltage": xr.DataArray(
                        voltages,
                        dims=("node",),
                        coords={
                            "node": list(self.current_node_indices(True).keys()),
                        },
                        attrs={
                            "units": "V"
                        }
                    ),
                    "current": xr.DataArray(
                        currents,
                        dims=("component",),
                        coords={
                            "component": list(self.voltage_node_indices(True).keys()),
                        },
                        attrs={
                            "units": "A"
                        }
                    )
                }
            ),
            residuals=residuals,
            converged=is_converged,
            iterations=iterations
        )

    def solve(self, x, residuals, Ntran=0, Gmin=0, time=None, maxiter=10000):
        """Low-level method to perform a DC solution of the circuit
        .. note::
            Typically the user calls :func:`dc_analysis.op_analysis` or
            :func:`dc_analysis.dc_analysis`, which in turn will setup all
            matrices and call this method on their behalf.
        The system we want to solve is:
        .. math::
            (mna + G_{min}) \\cdot x + N(t) + T(x, t) = 0
        Where:
        * :math:`mna` is the reduced MNA matrix with the required KVL/KCL rows
        * :math:`N` is composed by a DC part, :math:`N_{dc}`, and a dynamic
        time-dependent part :math:`N_{tran}(t)` and a time-dependent part
        :math:`T_t(t)`.
        * :math:`T(x, t)` is both time-dependent and non-linear with respect to
        the circuit solution :math:`x`, and it will be built at each iteration
        over :math:`t` and :math:`x`.

        Parameters
        ----------

        Ntran : ndarray, optional
            The linear time-dependent and *dynamic* part of :math:`N`, if available.
            Notice this is typically set when a DF being applied and the method is
            being called from a transient analysis.
        Gmin : ndarray, optional
            A matrix of the same size of ``mna``, containing the minimum
            transconductances to ground. It can be built with
            :func:`build_gmin_matrix`. If not set, no Gmin matrix is used.
        x  : ndarray or results.op_solution instance, optional
            The initial guess for the Newthon-Rhapson algorithm. If not specified,
            the all-zeros vector will be used.
        maxiter : int, optional
            The maximum number of Newton Rhapson iterations to be performed before
            giving up. If unset, ``options.dc_max_nr_iter`` is used.

        Returns
        -------
        error : ndarray
            The error associated with each solution item, if it was found.
        is_converged : boolean
            A flag set to True when convergence was detected.
        iterations : int
            Total number of NR iterations run.
        """
        mna_ref = self.fill_mna_matrix(np.zeros((self.dim_size, self.dim_size)))
        sources_ref = self.fill_sources_matrix(np.zeros((self.dim_size, 1)))

        # Remove grounds.
        mna_ref = mna_ref[1:, 1:]
        sources_ref = sources_ref[1:, :]

        print(self.node_description_indices(True))
        print(mna_ref)
        print(sources_ref)

        iterations = 0

        # time variable component: Tt this is always the same in each iter. So we
        # build it once for all.
        # Tt = np.zeros((self.reduced_dim_size, 1))
        # if not skip_Tt:
        #     i_index = self.nnodes

        #     for component in self.circuit.components:
        #         if isinstance(component, (VSource, ISource)):
        #             if isinstance(component, VSource):
        #                 Tt[i_index, 0] = -1 * component.voltage(time)
        #             elif isinstance(component, ISource):
        #                 if component.n1:
        #                     Tt[component.n1 - 1, 0] = Tt[component.n1 - 1, 0] + component.current(time)
        #                 if component.n2:
        #                     Tt[component.n2 - 1, 0] = Tt[component.n2 - 1, 0] - component.current(time)

        #             if component.GENERATES_VOLTAGE:
        #                 i_index += 1

        # # update N to include the time variable sources
        # sources_ref += Tt

        # Only check the first axis, so the input can be a slice of a larger matrix (e.g. for
        # sweeps).
        if x.shape[0] != self.reduced_dim_size:
            raise ValueError(
                f"x first axis must be of length {self.reduced_dim_size} (got {x.shape[0]})"
            )

        is_converged = False

        while not is_converged:
            mna = mna_ref + Gmin
            sources = sources_ref + Ntran

            try:
                is_converged, n_iter, convergence_by_node = self.mdn_solver(
                    x,
                    mna,
                    T=sources,
                    time=time,
                    maxiter=maxiter,
                    residuals=residuals
                )
            except LinAlgError:
                n_iter = 0
                is_converged = False
                print("failed.")
                printing.print_general_error("J Matrix is singular")
            except OverflowError:
                n_iter = 0
                is_converged = False
                print("failed.")
                printing.print_general_error("Overflow")
            else:
                iterations += n_iter

            if not is_converged:
                if convergence_by_node is not None:
                    # Check which node(s) failed to converge.
                    descriptions = self.node_description_indices(True)
                    unconverged = [
                        descriptions[index] for index, success in enumerate(convergence_by_node)
                        if not success
                    ]
                    print(f"the following failed to converge: {', '.join(unconverged)}")

                if n_iter == maxiter - 1:
                    printing.print_general_error("Error: maxiter exceeded (" + str(maxiter) + ")")

                x.fill(np.nan)
                residuals.fill(np.nan)
                break

        return is_converged, iterations

    def mdn_solver(self, x, mna, T, maxiter, residuals, time=None):
        """
        Solves a problem like F(x) = 0 using the Newton Algorithm with a variable
        damping.
        Where:
        .. math::
            F(x) = mna*x + T + T(x)
        * :math:`mna` is the Modified Network Analysis matrix of the circuit
        * :math:`T(x)` is the contribute of nonlinear elements to KCL
        * :math:`T` contains the contributions of the independent sources, time
        * invariant and linear
        If :math:`x(0)` is the initial guess, every :math:`x(n+1)` is given by:
        .. math::
            x(n+1) = x(n) + td \\cdot dx
        Where :math:`td` is a damping coefficient to avoid overflow in non-linear
        components and excessive oscillation in the very first iteration. Afterwards
        :math:`td=1` To calculate :math:`td`, an array of locked nodes is needed.
        The convergence check is done this way:
        **Parameters:**
        x : ndarray
            The initial guess. If set to ``None``, it will be initialized to all
            zeros. Specifying a initial guess may improve the convergence time of
            the algorithm and determine which solution (if any) is found if there
            are more than one.
        mna : ndarray
            The Modified Network Analysis matrix of the circuit, reduced, see above.
        circ : circuit instance
            The circuit instance.
        T : ndarray,
            The :math:`T` vector described above.
        maxiter : int
            The maximum iterations that the method may perform.
        nv : int
            Number of nodes in the circuit (counting the ref, 0)
        time : float or None, optional
            The value of time to be passed to non_linear _and_ time variant
            elements.
        print_steps : boolean, optional
            Show a progress indicator, very verbose. Defaults to ``False``.
        **Returns:**
        sol : ndarray
            The solution.
        residuals : ndarray
            The residuals.
        is_converged : boolean
            A boolean that is set to ``True`` whenever the method exits because of a
            successful convergence check. ``False`` whenever convergence problems
            where found.
        N : int
            The number of NR iterations performed.
        convergence_by_node : list
            If ``debug`` was set to ``True``, this list has the same size of the MNA
            matrix and contains the information regarding which nodes fail to
            converge in the circuit. Ie. ``if convergence_by_node[j] == False``,
            node ``j`` has a convergence problem. This may significantly help
            debugging non-convergent circuits.
        """
        if T is None:
            T = np.zeros((self.reduced_dim_size, 1))

        # Allocate the matrices (these get reused for each solve step).
        if self.use_sparse:
            mna = scipy.sparse.coo_matrix(mna)
            J = scipy.sparse.lil_matrix((self.reduced_dim_size, self.reduced_dim_size))
        else:
            J = np.zeros((self.reduced_dim_size, self.reduced_dim_size))
        Tx = np.zeros((self.reduced_dim_size, 1))

        if residuals is None:
            residuals = np.zeros((self.reduced_dim_size, 1))

        is_converged = False
        count = 0

        while count < maxiter:  # Newton iteration counter.
            count += 1

            # Build dT(x)/dx (stored in J) and Tx(x).
            J.fill(0)
            Tx.fill(0)

            for component in self.circuit.nonlinear_components:
                # Compute current voltage across the component's drive ports.
                drive_port_voltages = []

                for ndrva, ndrvc in component.drive_ports:
                    v = 0.0

                    if not self.node_is_ground(ndrva):
                        v += x[self.component_node_indices(True)[ndrva], 0]
                    if not self.node_is_ground(ndrvc):
                        v -= x[self.component_node_indices(True)[ndrvc], 0]

                    drive_port_voltages.append(v)

                for nouta, noutc in component.output_ports:
                    # Compute current at this output port.
                    output_current = component.output_port_current(
                        (nouta, noutc), drive_port_voltages=drive_port_voltages, time=time
                    )

                    if not self.node_is_ground(nouta):
                        globalnouta = self.component_node_indices(True)[nouta]
                        Tx[globalnouta, 0] += output_current
                    if not self.node_is_ground(noutc):
                        globalnoutc = self.component_node_indices(True)[noutc]
                        Tx[globalnoutc, 0] -= output_current

                    for ndrva, ndrvc in component.drive_ports:
                        # Compute differential (trans)conductance at this drive port.
                        drive_conductance = component.drive_port_conductance(
                            (ndrva, ndrvc), drive_port_voltages=drive_port_voltages, time=time
                        )

                        if not self.node_is_ground(nouta):
                            globalnouta = self.component_node_indices(True)[nouta]

                            if not self.node_is_ground(ndrva):
                                globalndrva = self.component_node_indices(True)[ndrva]
                                J[globalnouta, globalndrva] += drive_conductance
                            if not self.node_is_ground(ndrvc):
                                globalndrvc = self.component_node_indices(True)[ndrvc]
                                J[globalnouta, globalndrvc] -= drive_conductance
                        if not self.node_is_ground(noutc):
                            globalnoutc = self.component_node_indices(True)[noutc]

                            if not self.node_is_ground(ndrva):
                                globalndrva = self.component_node_indices(True)[ndrva]
                                J[globalnoutc, globalndrva] -= drive_conductance
                            if not self.node_is_ground(ndrvc):
                                globalndrvc = self.component_node_indices(True)[ndrvc]
                                J[globalnoutc, globalndrvc] += drive_conductance

            residuals = mna.dot(x) + T + Tx

            if self.use_sparse:
                lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(mna + J))
                dx = lu.solve(-residuals)
            else:
                dx = scipy.linalg.solve(mna + J, -residuals)

            x += self.damping_factor(dx, n=count) * dx

            if not self.circuit.nonlinear:
                # The circuit should have converged in a single pass.
                is_converged = True
                break
            elif np.all(self.converged(x, dx, residuals)):
                is_converged = True
                break

        if not is_converged:
            # re-run the convergence check, only this time get the results
            # by node, so we can show to the users which nodes are misbehaving.
            convergence_by_node = self.converged(x, dx, residuals)
        else:
            convergence_by_node = None

        return is_converged, count, convergence_by_node

    def damping_factor(self, dx, n=-1):
        """Calculates the damping coefficient for the Newthon method.

        The damping coefficient is choosen as the lowest between:

        - the damping required for the first NR iterations, a parameter which is set
        through the integer ``options.nr_damp_first_iters``.
        - If ``options.nl_voltages_lock`` evaluates to ``True``, the biggest damping
        factor that keeps the change in voltage across the locked nodes pairs less
        than the maximum variation allowed, set by:
        ``(options.nl_voltages_lock_factor * Vth)``
        - Unity.

        **Parameters:**

        dx : ndarray
            The undamped increment returned by the NR solver.
        self.circuit.locked_ports : list
            A vector of tuples of (internal) nodes that are a port of a non-linear
            component.
        n : int, optional
            The NR iteration counter

        .. note::

            If ``n`` is set to ``-1`` (or any negative value), ``td`` is independent
            from the iteration number and ``options.nr_damp_first_iters`` is ignored.

        **Returns:**

        td : float
            The damping coefficient.

        """
        nr_damp_first_iters = False
        nl_voltages_lock = True
        nl_voltages_lock_factor = 4

        if not nr_damp_first_iters or n < 0:
            td = 1
        else:
            if n < 10:
                td = 1e-2
            elif n < 20:
                td = 0.1
            else:
                td = 1

        td_new = 1
        VT = Vth(TREF)

        if nl_voltages_lock:
            for n1, n2 in self.circuit.locked_ports:
                if self.node_is_ground(n1):
                    if self.node_is_ground(n2):
                        raise ValueError("cannot ground both nodes of port")

                    globaln2 = self.component_node_indices(True)[n2]

                    if abs(dx[globaln2, 0]) > nl_voltages_lock_factor * VT:
                        td_new = (nl_voltages_lock_factor * VT) / abs(dx[globaln2, 0])
                else:
                    globaln1 = self.component_node_indices(True)[n1]

                    if self.node_is_ground(n2):
                        if abs(dx[globaln1, 0]) > nl_voltages_lock_factor * VT:
                            td_new = (
                                (nl_voltages_lock_factor * VT) / abs(dx[globaln1, 0])
                            )
                    else:
                        globaln2 = self.component_node_indices(True)[n2]

                        if abs(dx[globaln1, 0] - dx[globaln2, 0]) > nl_voltages_lock_factor * VT:
                            td_new = (
                                (nl_voltages_lock_factor * VT) / abs(dx[globaln1, 0] - dx[globaln2, 0])
                            )

                if td_new < td:
                    td = td_new

        return td


class Sweep(Analysis):
    """Performs a sweep of the value of V or I of a independent source from start
    value to stop value using the provided step.

    For every circuit generated, computes the OP.  This function relays on
    :func:`dc_analysis.op_analysis` to actually solve each circuit.

    **Parameters:**

    circ : Circuit instance
        The circuit instance to be simulated.
    start : float
        Start value of the sweep source
    stop : float
        Stop value of the sweep source
    step : float
        The step size in the sweep
    source : string
        The part ID of the source to be swept, eg. ``'V1'``.
    sweep_type : string, optional
        Either options.dc_lin_step (default) or options.dc_log_step
    guess : boolean, optional
        op_analysis will guess to start the first NR iteration for the first point,
        the previsious OP is used from then on. Defaults to ``True``.
    outfile : string, optional
        Filename of the output file. If set to ``'stdout'`` (default), prints to
        screen.
    verbose : int
        The verbosity level, from 0 (silent) to 6 (debug).

    **Returns:**

    rstdc : results.dc_solution instance or None
        A ``results.dc_solution`` instance is returned, if a solution was found
        for at least one sweep value.  or ``None``, if an error occurred (eg
        invalid start/stop/step values) or there was no solution for any
        sweep value.
    """
    def run(self, source, start, stop, steps=None, step_size=None, sweep_type="linear", x=None):
        axis = create_axis(sweep_type, start, stop, steps=steps, step_size=step_size)
        axis_label = source.name

        # Initial x vector guess. This contains the values at each node at each step. If not
        # specified, it's set to zero.
        if x is None:
            x = np.zeros((self.reduced_dim_size, len(axis)))

        residuals = np.zeros((self.reduced_dim_size, len(axis)))
        is_converged, iterations = self.solve(x, axis, source, residuals)

        node_voltage_indices = list(self.current_node_indices(True).values())
        component_current_indices = list(self.voltage_node_indices(True).values())

        # Split the node voltage and component current outputs into separate arrays.
        voltages = np.take(x, node_voltage_indices, axis=0)
        currents = np.take(x, component_current_indices, axis=0)

        return SweepSolution(
            data=xr.Dataset(
                {
                    "voltage": xr.DataArray(
                        voltages,
                        dims=("node", axis_label),
                        coords={
                            "node": list(self.current_node_indices(True).keys()),
                            axis_label: axis
                        },
                        attrs={
                            "units": "V"
                        }
                    ),
                    "current": xr.DataArray(
                        currents,
                        dims=("component", axis_label),
                        coords={
                            "component": list(self.voltage_node_indices(True).keys()),
                            axis_label: axis
                        },
                        attrs={
                            "units": "A"
                        }
                    )
                }
            ),
            residuals=residuals,
            converged=is_converged,
            iterations=iterations,
            axis_label=axis_label
        )

    def solve(self, x, axis, source, residuals):
        try:
            initial_value = source.dc_value
        except AttributeError:
            raise ValueError(f"source {repr(source)} has no DC value")

        op_analysis = OperatingPoint(self.circuit)
        is_converged = True
        iterations = 0

        try:
            for index, value in enumerate(axis):
                # Update the source.
                source.dc_value = value

                # Extract the current step's columns in the result matrices. Using `np.newaxis`
                # preserves the singular second dimension, which the analysis needs to correctly
                # perform matrix operations, and avoids copying (can verify with
                # `np.shares_memory`).
                xcol = x[:, index][:, np.newaxis]
                rcol = residuals[:, index][:, np.newaxis]

                # Calculate the new operating point.
                step_converged, step_iterations = op_analysis.solve(xcol, rcol)

                is_converged = is_converged and step_converged
                iterations += step_iterations
        finally:
            # Reset the source.
            source.dc_value = initial_value

        return is_converged, iterations
