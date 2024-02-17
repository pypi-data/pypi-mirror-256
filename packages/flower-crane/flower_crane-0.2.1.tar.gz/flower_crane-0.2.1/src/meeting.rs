use pyo3::prelude::*;

fn squared_dist(point1: (f32, f32), point2: (f32, f32), theta: f32) -> f32 {
    ((point1.0 - point2.0) * theta).powi(2) + (point1.1 - point2.1).powi(2)
}

// iterate over two lines and find the meeting points
#[pyfunction]
pub fn find_meeting(
    line1: Vec<(f32, f32)>,
    line2: Vec<(f32, f32)>,
    alt1: Vec<usize>,
    alt2: Vec<usize>,
    time1: Vec<usize>,
    time2: Vec<usize>,
    max_dist_degree_squared: f32,
    max_alt_dist: i32,
) -> PyResult<(Vec<usize>, f32)> {
    assert_eq!(time1.len(), line1.len());
    assert_eq!(time1.len(), alt1.len());
    assert_eq!(time2.len(), line2.len());
    assert_eq!(time2.len(), alt2.len());

    //  very simple theta calculation, but we don't need more for short distances
    let theta: f32 = (line1[0].1 * std::f32::consts::PI / 180.0).cos();

    let mut meeting = vec![];
    let mut started = false;
    let mut i = 0;
    let mut min_distance = 10000.0;
    let mut start_time = 0;
    let mut end_time;
    for j in 0..time2.len() {
        // we always expect time1 to be ahead
        while time1[i] < time2[j] && i < time1.len() - 1 {
            i += 1;
        }
        if i == time1.len() - 1 {
            break;
        }
        let dist = squared_dist(line1[i], line2[j], theta);
        let alt_dist = (alt1[i] as i32 - alt2[j] as i32).abs();
        let same_chunk = time2[(j + 1).min(time2.len() - 1)] - time2[j] < 20;
        if alt_dist < max_alt_dist && dist < max_dist_degree_squared && same_chunk {
            if dist < min_distance {
                min_distance = dist;
            }
            if !started {
                start_time = time1[i];
                started = true;
            } else {
                continue;
            }
        } else if !started {
            continue;
        } else {
            started = false;
            end_time = time1[i];
            if start_time != end_time {
                if meeting.last().map(|l| l == &start_time).unwrap_or(false) {
                    let n = meeting.len() - 1;
                    meeting[n] = end_time;
                } else {
                    meeting.push(start_time);
                    meeting.push(end_time);
                }
            }
        }
    }
    if started {
        end_time = time1[i];
        meeting.push(start_time);
        meeting.push(end_time);
    }
    Ok((meeting, min_distance))
}

#[cfg(test)]
mod test {
    use super::find_meeting;
    use serde_json;

    #[test]
    fn test_find_meeting() {
        let truth = vec![
            1660125112, 1660137176, 1660137184, 1660139832, 1660139868, 1660143536, 1660143788,
            1660147200,
        ];

        let line1_file = include_str!("../data/line1.json");
        let line1: Vec<(f32, f32)> = serde_json::from_str(line1_file).unwrap();

        let line2_file = include_str!("../data/line2.json");
        let line2: Vec<(f32, f32)> = serde_json::from_str(line2_file).unwrap();

        let alt1_file = include_str!("../data/alt1.json");
        let alt1: Vec<usize> = serde_json::from_str(alt1_file).unwrap();

        let alt2_file = include_str!("../data/alt2.json");
        let alt2: Vec<usize> = serde_json::from_str(alt2_file).unwrap();

        let time1_file = include_str!("../data/time1.json");
        let time1: Vec<usize> = serde_json::from_str(time1_file).unwrap();

        let time2_file = include_str!("../data/time2.json");
        let time2: Vec<usize> = serde_json::from_str(time2_file).unwrap();

        let (meeting, _) = find_meeting(line1, line2, alt1, alt2, time1, time2).unwrap();
        assert_eq!(meeting, truth);
    }
}
