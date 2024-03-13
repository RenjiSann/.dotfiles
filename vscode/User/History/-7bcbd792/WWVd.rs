pub fn invert(s: &String) -> String {
    s.chars().rev().collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(invert(&"Test".to_string()), "tseT");
        assert_eq!(invert(&"abcd".to_string()), "dcba");
    }
}
