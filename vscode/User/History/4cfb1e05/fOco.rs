pub fn invert(s: &mut String){
    let x = s.chars().cloned().rev().collect();
    s.clear();
    s.push_str(x)
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
