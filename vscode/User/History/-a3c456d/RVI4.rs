use std::collections::HashMap;

use lazy_static::lazy_static;
use maplit::hashmap;

lazy_static! {
    pub static ref MAPPINGS: HashMap<char, char> = hashmap! {
       '−' => '-',
    };
}

#[inline]
pub(crate) fn match_char(c: char) -> Option<char> {
    matcher!(c,
        ('\u{2212}', '-'), // −
    )
}

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