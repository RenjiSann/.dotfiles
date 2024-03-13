pub fn i_to_str(i: i32) -> String {
    let s = String::new();
    let mut i = i;
    while i > 0 {
        let digit: u8 = (i % 10) as u8;
        i /= 10;
        digit += b'0';
    }

    s.chars().rev().collect();
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
