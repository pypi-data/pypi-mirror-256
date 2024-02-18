use pyo3::prelude::*;
use ::pseudo_tilt::chern_character::{ChernChar, Δ};
use ::pseudo_tilt::tilt_stability::left_pseudo_semistabilizers;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn bogomolov_form(r: i64, c: i64, d: i64) -> PyResult<i64> {
    let v: ChernChar::<2> = (r, c, d).into();
    Ok(Δ(&v).raw_int_repn())
}

#[pyfunction]
fn pseudo_semistabilizers(r: i64, c: i64, d: i64) -> PyResult<Vec<(i64, i64, i64)>> {
    let v: ChernChar::<2> = (r, c, d).into();
    println!("Computing pseudo semistabilizers for {}", v);
    println!("");

    let output = left_pseudo_semistabilizers::find_all(&v)
        .map_err(|e|
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>
            (e)
        )?
        .into_iter()
        .map(|u| (u.r, u.c.into(), u.d.raw_int_repn()))
        .collect::<Vec<_>>();
    Ok(output)
}

/// A Python module implemented in Rust.
#[pymodule]
fn pseudo_tilt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(bogomolov_form, m)?)?;
    m.add_function(wrap_pyfunction!(pseudo_semistabilizers, m)?)?;
    Ok(())
}
