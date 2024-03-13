pub enum ErrorKind {
    ReservedKeyword,
}

pub struct Error {
    kind: ErrorKind
}

impl ParseError for Error {

}