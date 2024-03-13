pub fn str_to_i(s: &str) -> i32 {
    if s.len() == 0 {
        return 0;
    }

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
