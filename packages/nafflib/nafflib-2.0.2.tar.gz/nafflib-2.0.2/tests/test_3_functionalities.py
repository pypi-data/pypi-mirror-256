import numpy as np
import nafflib


# -----
# Henon map tune
Q_h = 0.2064898024701758
# -----
example_signals = {}
for x_start, label in zip([0.1, 0.3, 0.51], ["low_J", "mid_J", "high_J"]):
    example_signals[label] = nafflib.henon_map(x_start, 0.35 * x_start, Q_h, int(3e4))


def test_parse_complex():

    for label, signal in example_signals.items():
        # Extracting signal
        x, px = signal
        z = x - 1j * px
        N = np.arange(len(z))

        # Choosing number of harmonics
        n_harm = 7

        # x-px lines
        # Take more here, since some might repeat
        spectrum_z = nafflib.harmonics(
            z, num_harmonics=2 * n_harm, window_order=2, window_type="hann"
        )
        assert len(spectrum_z[1]) == 2 * n_harm, "Too few harmonics found for z"

        r_z, _, _ = nafflib.find_linear_combinations(
            spectrum_z[1], fundamental_tunes=[spectrum_z[1][0]]
        )

        # x-only lines
        spectrum_x = nafflib.harmonics(
            x, num_harmonics=n_harm, window_order=2, window_type="hann"
        )
        assert len(spectrum_x[1]) == n_harm, "Too few harmonics found for x"

        r_x, _, _ = nafflib.find_linear_combinations(
            spectrum_x[1], fundamental_tunes=[spectrum_x[1][0]]
        )

        # Scanning x-lines and comparing with z-lines
        errors_Q = []
        errors_A = []
        for res, A, freq in zip(r_x, spectrum_x[0], spectrum_x[1]):
            spec_z_index = r_z.index(res)
            errors_Q.append(spectrum_z[1][spec_z_index] - freq)
            errors_A.append(np.abs(spectrum_z[0][spec_z_index]) - np.abs(A))

        assert np.allclose(
            errors_Q, 0, atol=1e-14, rtol=0
        ), f"Q difference too large between x-only and x-px, for particle@{label}"
        assert np.allclose(
            errors_A, 0, atol=1e-1, rtol=0
        ), f"|A| difference too large between x-only and x-px, for particle@{label}"


def test_x_px_handling():

    for label, signal in example_signals.items():
        # Extracting signal
        x, px = signal
        z = x - 1j * px
        N = np.arange(len(z))

        # Choosing number of harmonics
        n_harm = 7

        # x-px lines
        # Take more here, since some might repeat
        spectrum_x_px = nafflib.harmonics(
            x, px, num_harmonics=2 * n_harm, window_order=2, window_type="hann"
        )
        assert len(spectrum_x_px[1]) == 2 * n_harm, "Too few harmonics found for x-px"
        r_x_px, _, _ = nafflib.find_linear_combinations(
            spectrum_x_px[1], fundamental_tunes=[spectrum_x_px[1][0]]
        )

        # x-only lines
        spectrum_x = nafflib.harmonics(
            x, num_harmonics=n_harm, window_order=2, window_type="hann"
        )
        assert len(spectrum_x[1]) == n_harm, "Too few harmonics found for x"
        r_x, _, _ = nafflib.find_linear_combinations(
            spectrum_x[1], fundamental_tunes=[spectrum_x[1][0]]
        )

        # Scanning x-lines and comparing with z-lines
        errors_Q = []
        errors_A = []
        for res, A, freq in zip(r_x, spectrum_x[0], spectrum_x[1]):
            spec_x_px_index = r_x_px.index(res)
            errors_Q.append(spectrum_x_px[1][spec_x_px_index] - freq)
            errors_A.append(np.abs(spectrum_x_px[0][spec_x_px_index]) - np.abs(A))

        assert np.allclose(
            errors_Q, 0, atol=1e-14, rtol=0
        ), f"Q difference too large between x-only and x-px, for particle@{label}"
        assert np.allclose(
            errors_A, 0, atol=1e-1, rtol=0
        ), f"|A| difference too large between x-only and x-px, for particle@{label}"


def test_signal_generation():

    for (label, signal), tol in zip(example_signals.items(), [1e-11, 1e-9, 1e-4]):
        # Extracting signal
        x, px = signal
        N = np.arange(len(x))

        # Choosing number of harmonics
        n_harm = 50

        A, Q = nafflib.harmonics(
            x, px, num_harmonics=n_harm, window_order=2, window_type="hann"
        )

        # Finding linear combinations (high order for this 1D system!)
        r, _, _ = nafflib.find_linear_combinations(
            Q, fundamental_tunes=[Q[0]], max_harmonic_order=30
        )

        # Reconstructing signal 2 ways
        x_r, px_r = nafflib.generate_signal(A, Q, N)
        x_k, px_k = nafflib.generate_pure_KAM(A, r, [Q[0]], N)

        # Comparing both signals with tracking
        assert np.allclose(
            x, x_r, atol=tol, rtol=0
        ), f"X-Phasor tracking exceeded tolerance in generate_signal for particle@{label}"
        assert np.allclose(
            x, x_k, atol=tol, rtol=0
        ), f"X-Phasor tracking exceeded tolerance in generate_pure_KAM for particle@{label}"
        assert np.allclose(
            px, px_r, atol=tol, rtol=0
        ), f"PX-Phasor tracking exceeded tolerance in generate_signal for particle@{label}"
        assert np.allclose(
            px, px_k, atol=tol, rtol=0
        ), f"PX-Phasor tracking exceeded tolerance in generate_pure_KAM for particle@{label}"


def test_linear_combinations():

    for label, signal in example_signals.items():
        # Extracting signal
        x, px = signal
        N = np.arange(len(x))

        # Choosing number of harmonics
        Q0 = nafflib.tune(x, px)
        Q1 = np.pi / 3 * Q0  # second irrational tune for testing

        # Dummy decreasing amplitude and linear combination
        n_harm = 10
        A = (
            np.exp(-np.array(range(n_harm))) ** 2
            + 1j
            * (np.pi / np.arange(1, n_harm + 1))
            * np.exp(-np.array(range(n_harm))) ** 2
        )
        r = [
            (1, 0, 0),
            (2, 0, -1),
            (-2, 1, 0),
            (2, -1, 0),
            (2, 0, 0),
            (-1, 1, 0),
            (1, -1, 0),
            (-3, 1, 1),
            (2, 1, 0),
            (0, 1, 0),
        ]

        # Creating signal and adding noise to frequencies
        x_k, px_k, frequencies = nafflib.generate_pure_KAM(
            A, r, [Q0, Q1], N, return_frequencies=True
        )

        np.random.seed(0)
        tol = 1e-10
        frequencies *= 1 + np.random.uniform(tol, tol * 10, n_harm)

        # Looking for linear combinations
        r_found, err, _ = nafflib.find_linear_combinations(
            frequencies, fundamental_tunes=[Q0, Q1], max_harmonic_order=10
        )

        assert np.all(
            np.array(r) == np.array(r_found)
        ), f"Linear combinations don't match for particle@{label}"
        assert np.all(
            err < tol * 10
        ), f"Frequencies found don't match for particle@{label}"


# 4D Henon
# Henon parameters:
# ------------
num_turns = int(1000)

coupling = 0.1
Qx_list = [0.2064898024701758, (3 - np.sqrt(5)) / 2]
Qy = np.sqrt(2) - 1

x_points = np.linspace(0.1, 0.5, 10)
px_point = 0.35 * x_points
# ------------

# Generating example signal
# =====================
example_signals_4D = {}
for Qx in Qx_list:
    for _i, (x0, px0) in enumerate(zip(x_points, px_point)):
        # Tracking
        x, px, y, py = nafflib.henon_map_4D(
            x0, px0, x0, px0, Qx=Qx, Qy=Qy, coupling=coupling, num_turns=num_turns
        )

        # Saving in a dict
        data = {"x": x, "px": px, "y": y, "py": py}
        example_signals_4D[(Qx, Qy, coupling, f"part_{_i}")] = data
# =====================


def test_real_signal_tune():
    for w_order in [0, 1, 2, 3, 4]:
        for label, dct_signal in example_signals_4D.items():
            Q_vec = []
            for plane in ["x", "y"]:
                _Q = nafflib.tune(dct_signal[plane], window_order=w_order)
                Q_vec.append(_Q)

            Q_vec_z = []
            for plane in ["x", "y"]:
                _Q = nafflib.tune(
                    dct_signal[plane], dct_signal[f"p{plane}"], window_order=w_order
                )
                Q_vec_z.append(_Q)

            assert np.all(
                np.array(Q_vec) > 0
            ), f"Negative tune detected despite real signal @ {label} and window_order={w_order}"

            assert np.allclose(
                np.abs(Q_vec), np.abs(Q_vec_z), atol=1e-5, rtol=0
            ), f"Tune difference too large between x-only and x-px @ {label} and window_order={w_order}"
