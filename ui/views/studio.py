"""
FloquetSim Explorer - Section 02: Simulation Studio
Specification: Frontend UI Blueprint v1.2 FINAL, Page 3
Configure and execute individual Trotter experiments with clear parameter controls,
topology preview, state management, and real-time execution feedback.
"""

import streamlit as st
import pandas as pd
from ui.graph_3d import create_3d_quantum_graph_figure
from src.processors import load_processor, get_processor_status
from src.circuits import build_trotter_circuit
from src.transpiler import transpile_trotter_circuit
from src.noise import build_noise_model
from src.simulation import simulate_ideal_statevector, simulate_noisy_shots
from src.observables import expectation_from_statevector, expectation_from_counts
from src.metrics import extract_circuit_metrics, calculate_shot_uncertainty
from src.classical_solver import simulate_exact_evolution


def render_studio_view():
    """Render Section 02: Simulation Studio."""
    st.markdown("## 🔬 Simulation Studio")
    st.caption("Configure and execute individual quantum simulation benchmarks with verified parameters.")

    col_controls, col_preview = st.columns([1.15, 0.85], gap="large")

    with col_controls:
        st.markdown("#### 1. Hardware & Core Parameters")
        
        selected_proc = st.selectbox(
            "Target Quantum Processor",
            options=["demo_processor_A", "demo_processor_B"],
            format_func=lambda x: "Demo Processor A (5-Qubit Linear Chain)" if "A" in x else "Demo Processor B (7-Qubit Heavy-Hex Ring)",
            index=0,
            key="studio_proc_select",
        )

        try:
            config, cmap = load_processor(selected_proc)
            status_info = get_processor_status(config)
        except Exception as e:
            st.error(f"Error loading processor: {e}")
            return

        if not status_info["is_official"]:
            st.markdown(
                """
                <div class="banner-demo">
                    <b>[PROVISIONAL DEMONSTRATION TOPOLOGY]</b><br>
                    Notice: Standalone official processor files were not provided in the public kit. 
                    Simulations use strictly verified demonstration configurations and synthetic noise models. Zero claims of physical IBM hardware calibration.
                </div>
                """,
                unsafe_allow_html=True,
            )

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            trotter_m = st.slider("Trotter Discretization Steps (m)", min_value=1, max_value=5, value=3, step=1, key="studio_m")
            evolution_time = st.slider("Evolution Time Horizon t (s)", min_value=1.0, max_value=10.0, value=5.0, step=0.5, key="studio_t")
        with col_p2:
            shots_count = st.selectbox("Measurement Shots", options=[1024, 2048, 4096], index=1, key="studio_shots")
            random_seed = st.number_input("Deterministic Seed", min_value=0, max_value=999999, value=42, step=1, key="studio_seed")

        with st.expander("⚙️ Advanced Physical Parameters", expanded=False):
            st.caption("Parameters of the Transverse-Field Ising Model (TFIM) in units of rad/s:")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                coupling_J = st.slider("Ising Coupling J (rad/s)", 0.0, 2.0, 1.0, 0.1, key="studio_J")
                transverse_hx = st.slider("Transverse Field hx (rad/s)", 0.0, 2.0, 1.0, 0.1, key="studio_hx")
            with col_a2:
                longitudinal_hz = st.slider("Longitudinal Field hz (rad/s)", 0.0, 0.5, 0.1, 0.05, key="studio_hz")
                noise_scale = st.slider("Noise Multiplier λ", 0.0, 3.0, 1.0, 0.25, key="studio_noise_scale")

        with st.expander("📖 Hamiltonian Specification", expanded=False):
            st.latex(r"H = H_{ZZ} + H_X + H_Z")
            st.latex(r"H_{ZZ} = J \sum_{j=0}^{2} Z_j Z_{j+1} + J Z_3 Z_0")
            st.latex(r"H_X = \sum_{j=0}^{3} (h_x + \delta h_x^j) X_j, \quad H_Z = h_z \sum_{j=0}^{3} Z_j")
            st.caption("Periodic boundary condition Z3 Z0 requires compiler-inserted SWAP routing on both processors.")

        st.write("")
        run_btn = st.button("▶️ Run Simulation", type="primary", use_container_width=True, key="studio_run_btn")

    with col_preview:
        st.markdown("#### Topology Preview")
        try:
            fig_prev = create_3d_quantum_graph_figure(
                config=config,
                height=320,
                show_node_labels=True,
            )
            st.plotly_chart(fig_prev, use_container_width=True)
            st.caption(f"Active graph: {config.name} | Edges: {len(config.coupling_map)}")
        except Exception as exc:
            st.info(f"Topology preview unavailable: {exc}")

        # Summary specification card
        st.markdown(
            f"""
            <div class="scientific-card-alt">
                <span style="font-weight: 600; font-size: 0.9rem; color: #172033;">Execution Target</span><br>
                <span class="caption-text">Processor: <b>{config.processor_id}</b> ({config.num_qubits} Qubits)</span><br>
                <span class="caption-text">Basis Gates: <code>{', '.join(config.basis_gates)}</code></span><br>
                <span class="caption-text">Trotter Steps: <b>m = {trotter_m}</b> (dt = {evolution_time / trotter_m:.2f} s)</span><br>
                <span class="caption-text">Noise Model: <b>Synthetic Depolarizing + Readout (λ={noise_scale:.2f})</b></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------
    # Simulation Execution & State Handling
    # -------------------------------------------------------------
    if run_btn:
        with st.status("Executing Quantum Simulation Pipeline...", expanded=True) as status:
            try:
                st.write("1. Synthesizing first-order Lie-Trotter circuit...")
                qc_logical = build_trotter_circuit(
                    num_spins=4,
                    trotter_steps=trotter_m,
                    total_time=evolution_time,
                    J=coupling_J,
                    hx=transverse_hx,
                    hz=longitudinal_hz,
                )

                st.write("2. Transpiling with Sabre Layout & Routing (Optimization Level 1)...")
                qc_transpiled = transpile_trotter_circuit(
                    circuit=qc_logical,
                    coupling_map=cmap,
                    basis_gates=config.basis_gates,
                    optimization_level=1,
                    seed_transpiler=random_seed,
                )
                metrics = extract_circuit_metrics(qc_transpiled, config)

                st.write("3. Computing exact classical reference (SciPy expm)...")
                exact_res = simulate_exact_evolution(
                    num_spins=4,
                    time_points=[evolution_time],
                    initial_state="0000",
                    J=coupling_J,
                    hx=transverse_hx,
                    hz=longitudinal_hz,
                )
                exact_m = exact_res["staggered_m"][0]

                st.write("4. Simulating ideal noiseless statevector...")
                sv = simulate_ideal_statevector(qc_logical)
                _, _, ideal_m = expectation_from_statevector(sv, num_spins=4)

                st.write(f"5. Simulating noisy execution in Qiskit Aer ({shots_count} shots)...")
                noise_model = build_noise_model(config, scale_factor=noise_scale)
                noisy_counts = simulate_noisy_shots(
                    circuit=qc_transpiled,
                    noise_model=noise_model,
                    shots=shots_count,
                    seed=random_seed,
                )
                _, _, noisy_m = expectation_from_counts(noisy_counts, num_spins=4)
                err_bar = calculate_shot_uncertainty(noisy_m, shots_count)

                # Store active run in session state
                st.session_state["latest_run"] = {
                    "processor_id": selected_proc,
                    "trotter_m": trotter_m,
                    "evolution_time": evolution_time,
                    "shots": shots_count,
                    "seed": random_seed,
                    "noise_scale": noise_scale,
                    "metrics": metrics,
                    "exact_m": exact_m,
                    "ideal_m": ideal_m,
                    "noisy_m": noisy_m,
                    "error_bar": err_bar,
                    "trotter_error": abs(ideal_m - exact_m),
                    "total_error": abs(noisy_m - exact_m),
                }

                status.update(label="Simulation Completed Successfully!", state="complete", expanded=False)

            except Exception as exc:
                status.update(label=f"Simulation Failed: {exc}", state="error")
                st.error(f"Error during execution: {exc}")
                return

    # Display results if available in session state
    if "latest_run" in st.session_state:
        run_data = st.session_state["latest_run"]
        m = run_data["metrics"]

        st.write("---")
        st.markdown("### Latest Execution Output")

        res_c1, res_c2, res_c3, res_c4, res_c5 = st.columns(5)
        res_c1.metric("Transpiled Depth", f"{m['circuit_depth']}")
        res_c2.metric("2-Qubit Gates", f"{m['count_2q_gates']} CX")
        res_c3.metric("Inserted SWAPs", f"{m['count_swap_gates']}")
        res_c4.metric("Exact M_stag", f"{run_data['exact_m']:+.4f}")
        res_c5.metric("Noisy M_stag", f"{run_data['noisy_m']:+.4f} ± {run_data['error_bar']:.3f}")

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.info(
                f"**Discretization Error:** {run_data['trotter_error']:.4f} | "
                f"**Total Noisy Error:** {run_data['total_error']:.4f}"
            )
        with col_b2:
            if st.button("📊 View Complete Scientific Results", type="primary", use_container_width=True):
                st.session_state["nav_destination"] = "Scientific Results"
                st.rerun()
