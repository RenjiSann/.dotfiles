pub fn invert(s: &mut String){
    let l = s.len();
    let x = unsafe { s.as_bytes_mut() };
    for i in 0..l {
        x.swap(i, l - i - 1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut s: String = "Test".to_string();
        invert(&mut s);
        assert_eq!(s, "tseT");
    }
}
