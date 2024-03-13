pub fn int_to_string(i: i32) -> String {
    if i == 0 {
        return "0".to_string();
    }

    let neg = i < 0;
    let mut i = if neg { -i } else { i };
    let mut s = String::new();

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
        assert_eq!(int_to_string(42), "42");
        assert_eq!(int_to_string(0), "0");
        assert_eq!(int_to_string(-42), "-42");
    }
}