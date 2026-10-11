"""
FloquetSim Explorer - Section 02: Simulation Studio
Specification: Nagrik Scientific Research Interface Design Reference
Two-column workspace: Grouped parameters with verified units on left,
live 3D processor topology preview on right, with real execution metrics and status feedback.
"""

import time
import streamlit as st
import pandas as pd
from ui.graph_3d import create_3d_quantum_graph_figure
from src.processors import load_processor, get_processor_status
from src.circuits import build_trotter_circuit
from src.transpiler import transpile_trotter_circuit
from src.noise import build_noise_model
from src.simulation import simulate_ideal_statevector, simulate_noisy_shots
from src.observables import expectation_from_statevector, expectation_from_counts
from src.metrics import extract_circuit_metrics, calculate_shot_uncertainty, calculate_trotter_error, calculate_noise_error, calculate_total_error
from src.classical_solver import simulate_exact_evolution
from ui.theme import (
    COLOR_CANVAS,
    COLOR_SURFACE,
    COLOR_RAISED,
    COLOR_BORDER,
    COLOR_CYAN,
    COLOR_AMBER,
    COLOR_VIOLET,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_SUCCESS,
    COLOR_ERROR,
)


def render_studio_view():
    """Render Section 02: Simulation Studio."""
    st.markdown("## 🔬 Simulation Studio")
    st.caption("Configure and execute individual quantum simulation benchmarks with verified parameters and live 3D preview.")

    col_controls, col_preview = st.columns([1.1, 0.9], gap="large")

    with col_controls:
        # 1. Quantum Architecture Selection
        st.markdown("#### 1. Hardware Architecture")
        with st.container():
            selected_proc = st.selectbox(
                "Target Demonstration Processor",
                options=["demo_processor_A", "demo_processor_B"],
                format_func=lambda x: "Demo Processor A (5-Qubit Linear Chain)" if "A" in x else "Demo Processor B (7-Qubit Hex-Ring + Leaf)",
                index=0,
                key="studio_proc_select",
                help="Select target coupling topology. Neither demonstration processor has native C4 connectivity.",
            )
            st.session_state["selected_processor_id"] = selected_proc

            try:
                config, cmap = load_processor(selected_proc)
                status_info = get_processor_status(config)
            except Exception as e:
                st.error(f"Error loading processor: {e}")
                return

            st.markdown(
                f"""
                <div class="banner-demo">
                    <b>[PROVISIONAL DEMONSTRATION TOPOLOGY]</b><br>
                    Simulations execute on local CPU via Qiskit Aer with synthetic depolarizing and readout noise. 
                    Zero claims of physical IBM hardware calibration or live cloud connectivity.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 2. Time & Trotter Discretization Parameters
        st.markdown("#### 2. Trotter Discretization & Time Horizon")
        with st.container():
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                trotter_m = st.slider(
                    "Trotter Steps (m)",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key="studio_m",
                    help="Discretization steps m. Higher m reduces algorithmic Trotter error O(Δt) but increases gate noise.",
                )
            with col_t2:
                evolution_time = st.slider(
                    "Total Time Horizon t (s)",
                    min_value=0.5,
                    max_value=10.0,
                    value=5.0,
                    step=0.5,
                    key="studio_t",
                    help="Evolution horizon t in seconds. Time-step per Trotter slice is Δt = t / m.",
                )

        # 3. Measurement & Sampling Settings
        st.markdown("#### 3. Measurement & Noise Sampling")
        with st.container():
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                shots_count = st.selectbox(
                    "Measurement Shots",
                    options=[1024, 2048, 4096],
                    index=1,
                    key="studio_shots",
                    help="Number of statistical projective measurements. Error bars scale as 1/sqrt(shots).",
                )
            with col_m2:
                random_seed = st.number_input(
                    "Deterministic RNG Seed",
                    min_value=0,
                    max_value=999999,
                    value=42,
                    step=1,
                    key="studio_seed",
                    help="Seed for transpiler routing and Qiskit Aer Monte Carlo shot sampling.",
                )

        # 4. Physical Hamiltonian Parameters
        with st.expander("⚙️ Physical Coupling & Field Strengths (rad/s)", expanded=False):
            st.caption("Parameters of the Transverse-Field Ising Model (TFIM) in units of rad/s (ħ = 1):")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                coupling_J = st.slider("Ising Coupling J (rad/s)", 0.0, 2.0, 1.0, 0.1, key="studio_J", help="ZZ coupling strength")
                transverse_hx = st.slider("Transverse Field hx (rad/s)", 0.0, 2.0, 1.0, 0.1, key="studio_hx", help="Transverse X field strength")
            with col_p2:
                longitudinal_hz = st.slider("Longitudinal Field hz (rad/s)", 0.0, 0.5, 0.1, 0.05, key="studio_hz", help="Longitudinal Z field symmetry breaking")
                noise_scale = st.slider("Noise Multiplier λ", 0.0, 3.0, 1.0, 0.25, key="studio_noise_scale", help="Scalar multiplier on 1Q, 2Q, and readout noise error rates")

        # 5. Hamiltonian Equation Summary
        with st.expander("📖 Implemented Hamiltonian Specification", expanded=False):
            st.latex(r"H = H_{ZZ} + H_X + H_Z")
            st.latex(r"H_{ZZ} = J \sum_{j=0}^{2} Z_j Z_{j+1} + J Z_3 Z_0")
            st.latex(r"H_X = \sum_{j=0}^{3} (h_x + \delta h_x) X_j, \quad H_Z = h_z \sum_{j=0}^{3} Z_j")
            st.caption("Periodic boundary condition Z3 Z0 requires compiler-inserted SWAP routing on both demonstration processors.")

        # Configuration status banner
        last_run_config = st.session_state.get("last_run_config", None)
        current_config = {
            "proc": selected_proc,
            "m": trotter_m,
            "t": evolution_time,
            "shots": shots_count,
            "seed": random_seed,
            "noise_scale": noise_scale,
        }
        is_stale = (last_run_config is not None and last_run_config != current_config)

        if is_stale:
            st.markdown(
                f"""
                <div style="font-size:0.8rem; color:{COLOR_AMBER}; background-color:{COLOR_RAISED}; border:1px solid {COLOR_BORDER}; border-radius:6px; padding:6px 10px; margin-bottom:10px;">
                    ℹ️ Parameters changed since last execution. Click Run to re-calculate.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        run_btn = st.button("▶️ Execute Quantum Simulation", type="primary", use_container_width=True, key="studio_run_btn")

    with col_preview:
        st.markdown("#### Live Processor Architecture Preview")
        
        # 3D Graph Preview
        fig_preview = create_3d_quantum_graph_figure(
            config=config,
            selected_node=0,
            show_node_labels=True,
            show_connections=True,
            height=380,
        )
        st.plotly_chart(fig_preview, use_container_width=True)

        st.markdown(
            f"""
            <div class="scientific-card" style="font-size: 0.82rem; line-height: 1.6;">
                <div style="font-weight: 700; color: {COLOR_CYAN}; margin-bottom: 4px;">Topological Reality:</div>
                • Shortest logical path dist(0, 3) = <b>3 hops</b> on both Processor A and B.<br>
                • Transpiler must insert SWAP gates to mediate non-local interaction <i>Z3 Z0</i>.<br>
                • Linear chain (A) requires linear routing; Hex-ring (B) routes through cycle.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------
    # SIMULATION EXECUTION & RESULT RENDERING
    # -------------------------------------------------------------
    if run_btn:
        st.session_state["sim_status"] = "running"
        with st.spinner("Compiling Trotter circuit, evaluating exact classical benchmark, and running Qiskit Aer noisy simulation..."):
            t_start = time.time()
            try:
                # 1. Build logical Trotter circuit
                qc_logical = build_trotter_circuit(
                    num_spins=4,
                    trotter_steps=trotter_m,
                    total_time=evolution_time,
                    initial_state="0000",
                    measure=False,
                )

                # 2. Transpile against hardware topology
                qc_transpiled = transpile_trotter_circuit(
                    circuit=qc_logical,
                    coupling_map=cmap,
                    basis_gates=config.basis_gates,
                    optimization_level=1,
                    seed_transpiler=random_seed,
                )
                metrics = extract_circuit_metrics(qc_transpiled, config)

                # 3. Exact classical benchmark
                exact_res = simulate_exact_evolution(
                    num_spins=4,
                    time_points=[evolution_time],
                    initial_state="0000",
                    J=coupling_J,
                    hz=longitudinal_hz,
                    hx=transverse_hx,
                )
                exact_m = exact_res["staggered_m"][0]
                exact_local_z = exact_res["local_z"][0]

                # 4. Ideal statevector simulation
                sv = simulate_ideal_statevector(qc_logical)
                ideal_local_z, _, ideal_m = expectation_from_statevector(sv, num_spins=4)

                # 5. Noisy Qiskit Aer simulation
                noise_model = build_noise_model(config, scale_factor=noise_scale)
                noisy_counts = simulate_noisy_shots(
                    circuit=qc_transpiled,
                    noise_model=noise_model,
                    shots=shots_count,
                    seed=random_seed,
                )
                noisy_local_z, _, noisy_m = expectation_from_counts(noisy_counts, num_spins=4)

                # 6. Errors & uncertainties
                err_trot = calculate_trotter_error(ideal_m, exact_m)
                err_noise = calculate_noise_error(noisy_m, ideal_m)
                err_tot = calculate_total_error(noisy_m, exact_m)
                err_bar = calculate_shot_uncertainty(noisy_m, shots_count)
                t_elapsed = time.time() - t_start

                # Persist in session state
                st.session_state["last_run_config"] = current_config
                st.session_state["sim_status"] = "completed"
                st.session_state["latest_studio_result"] = {
                    "exact_m": exact_m,
                    "ideal_m": ideal_m,
                    "noisy_m": noisy_m,
                    "exact_local_z": exact_local_z,
                    "noisy_local_z": noisy_local_z,
                    "err_trot": err_trot,
                    "err_noise": err_noise,
                    "err_tot": err_tot,
                    "err_bar": err_bar,
                    "metrics": metrics,
                    "t_elapsed": t_elapsed,
                }
            except Exception as e:
                st.session_state["sim_status"] = "failed"
                st.error(f"Simulation execution failed: {e}")
                return

    # Display results if available
    res = st.session_state.get("latest_studio_result", None)
    if res:
        st.write("---")
        st.markdown("### 📊 Execution Results & Transpilation Telemetry")
        
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        with m_col1:
            st.metric("Exact Classical ⟨M⟩", f"{res['exact_m']:+.4f}", "Benchmark")
        with m_col2:
            st.metric("Ideal Trotter ⟨M⟩", f"{res['ideal_m']:+.4f}", f"Δ = {res['err_trot']:.4f}")
        with m_col3:
            st.metric("Noisy Aer ⟨M⟩", f"{res['noisy_m']:+.4f}", f"± {res['err_bar']:.4f}")
        with m_col4:
            st.metric("Total Error ϵ", f"{res['err_tot']:.4f}", "Combined")
        with m_col5:
            st.metric("Execution Time", f"{res['t_elapsed']:.3f} s", "Aer CPU")

        # Hardware Compilation Metrics
        st.markdown("#### Hardware Circuit Compilation Metrics")
        cm_col1, cm_col2, cm_col3, cm_col4 = st.columns(4)
        with cm_col1:
            st.metric("Transpiled Depth", f"{res['metrics'].depth}", "Post-transpile")
        with cm_col2:
            st.metric("Total Gate Count", f"{res['metrics'].total_gates}", "Physical basis")
        with cm_col3:
            st.metric("Native CNOT Count", f"{res['metrics'].cnot_count}", "2Q operations")
        with cm_col4:
            st.metric("SWAP Gates Inserted", f"{res['metrics'].swap_count}", "Routing penalty")

        # Site-Resolved Polarization Table
        st.markdown("#### Site-Resolved Local Polarization ⟨Z_j⟩")
        site_rows = []
        for j in range(4):
            site_rows.append({
                "Spin Site": f"Site {j}",
                "Exact ⟨Z_j⟩": f"{res['exact_local_z'][j]:+.4f}",
                "Noisy Aer ⟨Z_j⟩": f"{res['noisy_local_z'][j]:+.4f}",
                "Discrepancy": f"{abs(res['noisy_local_z'][j] - res['exact_local_z'][j]):.4f}",
            })
        df_sites = pd.DataFrame(site_rows)
        st.dataframe(df_sites, use_container_width=True)
