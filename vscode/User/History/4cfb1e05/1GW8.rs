pub fn invert(s: &mut String){
    let r: Vec<_> = s.chars().collect();
    s = r.iter().rev().collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut s: String = "Test".to_string();
    }
}
