const UNITS: (char, char, char) = ('I', 'V', 'X');
const TENS: (char, char, char) = ('X', 'L', 'C');
const HUNDREDS: (char, char, char) = ('C', 'D', 'M');

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
        9 => format!("{}{}", l.0, l.2),
        _ => panic!("{} is not a digit", digit)
    }
}

pub fn i_to_roman(i: u32) -> String {
    let units = digit_to_letters((i % 10) as u8, UNITS);
    let tens = digit_to_letters((i / 10 % 10) as u8, TENS);
    let hundreds = digit_to_letters((i / 100 % 10) as u8, HUNDREDS);
    format!("{}{}{}", hundreds, tens, units)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(digit_to_letters(0, UNITS), "");
        assert_eq!(digit_to_letters(1, UNITS), "I");
        assert_eq!(digit_to_letters(2, UNITS), "II");
        assert_eq!(digit_to_letters(3, UNITS), "III");
        assert_eq!(digit_to_letters(4, UNITS), "IV");
        assert_eq!(digit_to_letters(5, UNITS), "V");
        assert_eq!(digit_to_letters(6, UNITS), "VI");
        assert_eq!(digit_to_letters(7, UNITS), "VII");
        assert_eq!(digit_to_letters(8, UNITS), "VIII");
        assert_eq!(digit_to_letters(9, UNITS), "IX");
    }

    #[test]
    fn full_test() {
        assert_eq!(i_to_roman(15), "XV");
        assert_eq!(i_to_roman(99), "XCIX")
    }
}
