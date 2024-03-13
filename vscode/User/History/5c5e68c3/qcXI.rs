
fn digit_to_letters(digit: u8, l: (char, char, char)) -> String {
    match digit {
        0 => "".to_string(),
        1 => format!("{}", l.0),
        2 => format!("{}{}", l.0, l.0),
        3 => format!("{}{}{}", l.0, l.0, l.0),
        4 => format!("{}{}", l.0, l.1),
        5 => format!("{}", l.1),
        6 => format!("{}{}", l.1, l.0),
        7 => format!("{}{}{}", l.1, l.0, l.0),
        8 => format!("{}{}{}{}", l.1, l.0, l.0, l.0),
        9 => format!("{}{}", l.0, l.0),
        _ => panic!("{} is not a digit", digit)
    }
}

pub fn i_to_roman(i: u32) -> String {
    left + right
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
