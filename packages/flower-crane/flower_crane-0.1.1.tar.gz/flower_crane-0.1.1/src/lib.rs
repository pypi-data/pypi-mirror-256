use meeting::find_meeting;
use meeting_np::find_meeting_np;
use numpy::{PyReadonlyArray1, PyReadonlyArray2};
use pyo3::prelude::*;
mod meeting;
mod meeting_np;

#[pymodule]
fn flower_crane(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_meeting, m)?)?;

    #[pyfn(m)]
    #[pyo3(name = "find_meeting_np")]
    fn find_meeting_np_py<'py>(
        line1: PyReadonlyArray2<'py, f64>,
        line2: PyReadonlyArray2<'py, f64>,
        alt1: PyReadonlyArray1<'py, i64>,
        alt2: PyReadonlyArray1<'py, i64>,
        time1: PyReadonlyArray1<'py, i64>,
        time2: PyReadonlyArray1<'py, i64>,
    ) -> PyResult<(Vec<i64>, f64)> {
        find_meeting_np(
            line1.as_slice().unwrap(),
            line2.as_slice().unwrap(),
            alt1.as_slice().unwrap(),
            alt2.as_slice().unwrap(),
            time1.as_slice().unwrap(),
            time2.as_slice().unwrap(),
        )
    }
    Ok(())
}
