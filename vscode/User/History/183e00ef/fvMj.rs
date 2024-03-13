use nom::error::ParseError;

pub enum ErrorKind {
    ReservedKeyword,
}

pub struct Error {
    kind: ErrorKind
}

impl<I> ParseError<I> for Error {
    fn from_error_kind(input: I, kind: nom::error::ErrorKind) -> Self {
        Self {kind}
    }

    fn append(input: I, kind: nom::error::ErrorKind, other: Self) -> Self {
        todo!()
    }
}