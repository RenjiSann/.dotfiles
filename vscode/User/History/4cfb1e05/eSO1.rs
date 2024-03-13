pub fn invert(s: &mut String){
    let l = s.len();
    let mut x = unsafe { s.as_bytes_mut() };
    for i in 0..l {
        unsafe {std::mem::swap(&mut x[i], &mut x[l - i - 1])};
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut s: String = "Test".to_string();
    }
}
