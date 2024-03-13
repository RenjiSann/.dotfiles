pub struct Word<'a>(pub &'a str);

impl<'a> From<&'a str> for Word<'a> {
    fn from(value: &'a str) -> Self {
        Word(value)
    }
}
