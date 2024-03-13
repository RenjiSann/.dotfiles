pub fn string_to_int(s: String) -> i32 {
    if s.len() == 0 {
        return 0;
    }

    let mut chars = s.chars().peekable();
    let neg = chars.peek().unwrap() == &'-';
    if neg {
        chars.next();
    }

    let res = chars.fold(0, |cur, dig| cur * 10 + (dig as u8 - b'0') as i32);
    res * if neg { -1 } else { 1 }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(string_to_int("0"), 0);
        assert_eq!(string_to_int(""), 0);
        assert_eq!(string_to_int("1"), 1);
        assert_eq!(string_to_int("15"), 15);
        assert_eq!(string_to_int("-1"), -1);
        assert_eq!(string_to_int("-42"), -42);
    }
}
