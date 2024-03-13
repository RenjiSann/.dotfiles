use nom::error::ParseError;

pub enum ErrorKind {
    ReservedKeyword,
}

pub struct Error {
    kind: ErrorKind
}

impl ParseError for Error {
    fn from_error_kind(input: I, kind: nom::error::ErrorKind) -> Self {
        todo!()
    }

    fn append(input: I, kind: nom::error::ErrorKind, other: Self) -> Self {
        todo!()
    }
}