pub fn str_to_i(s: &str) -> i32 {
    if s.len() == 0 {
        return 0;
    }

    let mut res: i32 = 0;
    let mut chars = s.chars().peekable();
    let neg = chars.peek().unwrap() == '-';
    if neg {
        chars.next();
    }

    chars.fold(0, |cur, dig| cur + (dig as u8 - b'0') as i32);
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
