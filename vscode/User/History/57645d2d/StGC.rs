#[derive(Debug, PartialEq, Eq)]
pub struct Word<'a>(&'a str);

impl<'a> From<&'a str> for Word<'a> {
    fn from(value: &'a str) -> Self {
        Word(value)
    }
}

impl<'a> Word<'a> {
    pub fn text(&self) -> &'a str {
        self.0
    }
}