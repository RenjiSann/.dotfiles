use nom::error::{self};


pub struct Error {
    notes: Vec<String>
}

impl<I> error::ParseError<I> for Error {
    fn from_error_kind(input: I, kind: error::ErrorKind) -> Self {
        Self {kind}
    }

    fn append(input: I, kind: error::ErrorKind, other: Self) -> Self {
        todo!()
    }
}