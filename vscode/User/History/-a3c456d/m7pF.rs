macro_rules! matcher {
    ( $c:ident, $(($x:literal, $y:literal),)*) => {
        match $c {
            $(
                $x => Some($y),
            )*
            _ => None
        }
    }
}

#[inline]
pub(crate) fn match_char(c: char) -> Option<char> {
    matcher!(c,
        ('\u{2212}', '-'), // −
    )
}