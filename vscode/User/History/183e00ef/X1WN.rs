pub enum ErrorKind {
    ReservedKeyword,
}

pub struct Error {
    kind: ErrorKind
}