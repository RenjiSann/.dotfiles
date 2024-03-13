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
    matcher!(
        c,
        ('\u{01c3}', '!'),  //
        ('\u{2018}', '\''), //
        ('\u{2019}', '\''), //
        ('\u{201c}', '"'),  //
        ('\u{201d}', '"'),  //
        ('\u{2212}', '-'),  // −
    )
}
