"""Helper functions used for testing word-list functions having floats."""

import pytest


def assert_wlst_eq(out_wlst, exp_wlst):
    out_wlst_w = [e[0] for e in out_wlst]
    out_wlst_n = [e[1] for e in out_wlst]
    exp_wlst_w = [e[0] for e in exp_wlst]
    exp_wlst_n = [e[1] for e in exp_wlst]
    assert out_wlst_w == exp_wlst_w
    assert out_wlst_n == pytest.approx(exp_wlst_n)


def wlst_approx_eq(out_wlst, exp_wlst):
    out_wlst_w = [e[0] for e in out_wlst]
    out_wlst_n = [e[1] for e in out_wlst]
    exp_wlst_w = [e[0] for e in exp_wlst]
    exp_wlst_n = [e[1] for e in exp_wlst]
    return (
        out_wlst_w == exp_wlst_w
        and out_wlst_n == pytest.approx(exp_wlst_n)
    )