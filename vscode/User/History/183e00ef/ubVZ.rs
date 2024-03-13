use nom::error::{self};

pub enum ErrorKind {
    ReservedKeyword,
}

pub struct Error {
    kind: ErrorKind
}

impl<I> error::ParseError<I> for Error {
    fn from_error_kind(input: I, kind: ErrorKind) -> Self {
        Self {kind}
    }

    fn append(input: I, kind: ErrorKind, other: Self) -> Self {
        todo!()
    }
}