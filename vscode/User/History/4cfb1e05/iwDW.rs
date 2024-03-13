pub fn i_to_str(i: i32) -> String {
    if i == 0 {
        return "0".to_string();
    }

    let neg = i < 0;

    let mut s = String::new();
    let mut i = i;
    while i > 0 {
        let digit: u8 = b'0' + (i % 10) as u8;
        i /= 10;
        s.push(digit as char);
    }

    if neg {
        s.push('-');
    }

    s.chars().rev().collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(i_to_str(42), "42");
        assert_eq!(i_to_str(0), "0");
        assert_eq!(i_to_str(-42), "-42");
    }
}
