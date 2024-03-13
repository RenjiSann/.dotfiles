pub fn str_to_i(s: &str) -> i32 {
    if s.len() == 0 {
        return 0;
    }

    let mut res: i32 = 0;
    let mut chars = s.chars();
    let f = chars.next().unwrap();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
