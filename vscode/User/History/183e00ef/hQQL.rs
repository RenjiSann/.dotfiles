use nom::error::{self};


pub struct ParseError {
    notes: Vec<String>
}

impl<I> error::ParseError<I> for ParseError {
    fn from_error_kind(input: I, kind: error::ErrorKind) -> Self {
        Self {notes: vec![] }
    }

    fn append(input: I, kind: error::ErrorKind, other: Self) -> Self {
        todo!()
    }
}