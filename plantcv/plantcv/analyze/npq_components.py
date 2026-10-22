"""Analyze additional NPQ Components"""
import numpy as np
import xarray as xr
from plantcv.plantcv._helpers import _iterate_analysis
from plantcv.plantcv._globals import outputs, fatal_error
from plantcv.plantcv.analyze.npq import _set_labels, _calc_npq


def npq_components(ps, labeled_mask, n_labels=1, label=None):
    """Analyze additional NPQ components

    Parameters
    ----------
    ps                 = plantcv.plantcv.classes.PSII_Data,
        Object containing ojip_light data or PSL/PMT/PML data.
    labeled_mask       = numpy.ndarray,
        Labeled mask of objects (32-bit).
    n_labels           = int,
        Total number expected individual objects (default = 1).
    label              = str,
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).

    Returns
    -------
    out_dict = dictionary,
        Dictionary of npq component arrays.
    """
    # Check if Pam Time frame is present
    if getattr(ps, "pmt", None) is None:
        fatal_error("PSII_data object must have pam time (pmt) data to calculate npq components.")
    # Set Labels
    labels = _set_labels(label, n_labels)
    pam_time = ps.pmt.pam_time
    # make a blank mask
    blank_shape = pam_time.shape[0:2]
    # PMT._load only fills each frame_label for the measurements in its block (zeros elsewhere):
    #   t0 = dark-adapted baseline (F0, Fm), light block (Fp, Fmp), recovery block (Fmpp),
    #   and F0p is stored only on the final measurement.
    baseline = str(pam_time.measurement.values[0])
    last = str(pam_time.measurement.values[-1])
    light_meas = _measurements_with(pam_time, "Fmp")
    recovery_meas = _measurements_with(pam_time, "Fmpp")
    if not light_meas:
        fatal_error("PMT data must contain at least one light-adapted (Fmp) measurement.")

    out_list = []
    # Loop over timepoints
    for t in light_meas:
        ps_da = _pair_frames(pam_time, F0=baseline, Fm=baseline, Fp=t, Fmp=t, F0p=last)

        qP = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_qP_components,
            **{"ps_da": ps_da, "t": t}
        )

        qN = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_qN_components,
            **{"ps_da": ps_da, "t": t}
        )

        qL = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_qL_components,
            **{"ps_da": ps_da, "qP": qP, "t": t}
        )

        phiNO = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_phiNO_components,
            **{"ps_da": ps_da, "qL": qL, "t": t}
        )

        phiNPQ = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_phiNPQ_components,
            **{"ps_da": ps_da, "phiNO": phiNO, "t": t}
        )

        out_list.append({"measurement": t, "qP": qP, "qN": qN, "qL": qL, "phiNO": phiNO, "phiNPQ": phiNPQ})
    # Recovery Components
    for t in recovery_meas:
        ps_da = _pair_frames(pam_time, Fm=baseline, Fmp=light_meas[-1], Fmpp=t)

        qI = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_qI_components,
            **{"ps_da": ps_da, "t": t}
        )
        qE = _iterate_analysis(
            img=np.zeros(blank_shape),
            labeled_mask=labeled_mask,
            n_labels=n_labels, label=labels,
            function=_calc_qE_components,
            **{"ps_da": ps_da, "t": t}
        )

        out_list.append({"measurement": t, "qI": qI, "qE": qE})

    return out_list


def _measurements_with(pam_time, frame_label):
    """Return the measurement labels where a frame_label holds data (PMT._load zero-fills the rest)"""
    if frame_label not in pam_time.frame_label:
        return []
    frames = pam_time.sel(frame_label=frame_label)
    has_data = frames.any(dim=["x", "y"]).to_numpy()
    return [str(m) for m in frames.measurement.values[has_data]]


def _pair_frames(pam_time, **sources):
    """Build a frame_label DataArray taking each frame_label from its own measurement

    e.g. _pair_frames(pam_time, Fm="t0", Fmp="t3") -> Fm from t0 and Fmp from t3
    """
    frames = [pam_time.sel(frame_label=lbl, measurement=meas).drop_vars(["frame_label", "measurement"])
              for lbl, meas in sources.items()]
    return xr.concat(frames, dim="frame_label").assign_coords(frame_label=list(sources))


def _calc_qP_components(img, mask, label, ps_da, t):
    """Calculate qP as (Fm' - Fp) / (Fm' - F0')"""
    fmp = ps_da.sel(frame_label="Fmp").astype('float').where(mask > 0, other=np.nan)
    fp = ps_da.sel(frame_label="Fp").astype('float').where(mask > 0, other=np.nan)
    f0p = ps_da.sel(frame_label="F0p").astype('float').where(mask > 0, other=np.nan)
    qp = ((fmp - fp) / (fmp - f0p)).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_qP_{t}', trait=f'mean qP {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(qp), label='none')
    # return the sum of qp and img so that iterate analysis returns complete results
    return np.where(mask > 0, qp, img)


def _calc_qN_components(img, mask, label, ps_da, t):
    """Calculate qN as 1 - (Fm'-F0')/(Fm-F0)"""
    fmp = ps_da.sel(frame_label="Fmp").astype('float').where(mask > 0, other=np.nan)
    fm = ps_da.sel(frame_label="Fm").astype('float').where(mask > 0, other=np.nan)
    f0p = ps_da.sel(frame_label="F0p").astype('float').where(mask > 0, other=np.nan)
    f0 = ps_da.sel(frame_label="F0").astype('float').where(mask > 0, other=np.nan)
    qn = (1 - (fmp - f0p) / (fm - f0)).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_qN_{t}', trait=f'mean qN {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(qn), label='none')
    # return the sum of qn and img so that iterate analysis returns complete results
    return np.where(mask > 0, qn, img)


def _calc_qL_components(img, mask, label, ps_da, qP, t):
    """Calculate qL as qP * F0'/Fp"""
    qp_sub = np.where(mask > 0, qP, np.nan)
    f0p = ps_da.sel(frame_label="F0p").astype('float').where(mask > 0, other=np.nan)
    fp = ps_da.sel(frame_label="Fp").astype('float').where(mask > 0, other=np.nan)
    ql = ((qp_sub * f0p) / fp).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_qL_{t}', trait=f'mean qL {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(ql), label='none')
    # return the sum of ql and img so that iterate analysis returns complete results
    return np.where(mask > 0, ql, img)


def _calc_qI_components(img, mask, label, ps_da, t):
    """Calculate qI as (Fm-Fm'')/Fm''"""
    fmpp = ps_da.sel(frame_label="Fmpp").astype('float').where(mask > 0, other=np.nan)
    fm = ps_da.sel(frame_label="Fm").astype('float').where(mask > 0, other=np.nan)
    qi = ((fm - fmpp) / fmpp).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_qI_{t}', trait=f'mean qI {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(qi), label='none')
    # return the sum of qi and img so that iterate analysis returns complete results
    return np.where(mask > 0, qi, img)


def _calc_qE_components(img, mask, label, ps_da, t):
    """Calculate qE as Fm * (Fm''-Fm')/(Fm'' * Fm')"""
    fmp = ps_da.sel(frame_label="Fmp").astype('float').where(mask > 0, other=np.nan)
    fmpp = ps_da.sel(frame_label="Fmpp").astype('float').where(mask > 0, other=np.nan)
    fm = ps_da.sel(frame_label="Fm").astype('float').where(mask > 0, other=np.nan)
    qe = ((fm * (fmpp - fmp)) / (fmpp * fmp)).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_qE_{t}', trait=f'mean qE {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(qe), label='none')
    # return the sum of qe and img so that iterate analysis returns complete results
    return np.where(mask > 0, qe, img)


def _calc_phiNO_components(img, mask, label, ps_da, qL, t):
    """Calculate phiNO as 1 / (NPQ + 1 + ql * Fm / F0)"""
    ql_masked = np.where(mask > 0, qL, np.nan)
    fmp = ps_da.sel(frame_label="Fmp").astype('float').where(mask > 0, other=np.nan)
    fm = ps_da.sel(frame_label="Fm").astype('float').where(mask > 0, other=np.nan)
    npq_masked = _calc_npq(fmp, fm)
    npq_masked_validated = npq_masked.where(~((fm == fmp) & (fmp > 0)), other=0)
    f0 = ps_da.sel(frame_label="F0").astype('float').where(mask > 0, other=np.nan)
    phiNO = (1 / (npq_masked_validated + 1 + ql_masked * fm / f0)).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_phiNO_{t}', trait=f'mean phiNO {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(phiNO), label='none')
    # return the sum of phiNO and img so that iterate analysis returns complete results
    return np.where(mask > 0, phiNO, img)


def _calc_phiNPQ_components(img, mask, label, ps_da, phiNO, t):
    """Calculate phiNPQ as 1 - (Fmp - Fp)/Fmp - phiNO"""
    phiNO_masked = np.where(mask > 0, phiNO, np.nan)
    fmp = ps_da.sel(frame_label="Fmp").astype('float').where(mask > 0, other=np.nan)
    fp = ps_da.sel(frame_label="Fp").astype('float').where(mask > 0, other=np.nan)
    phiNPQ = (1 - ((fmp - fp) / fmp) - phiNO_masked).to_numpy()
    # add mean to outputs
    outputs.add_observation(sample=label,
                            variable=f'mean_phiNPQ_{t}', trait=f'mean phiNPQ {t}',
                            method='plantcv.plantcv.analyze.npq_components',
                            scale='none', datatype=float,
                            value=np.nanmean(phiNPQ), label='none')
    # return the sum of phiNPQ and img so that iterate analysis returns complete results
    return np.where(mask > 0, phiNPQ, img)
