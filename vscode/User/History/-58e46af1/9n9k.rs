use super::word::Word;

pub struct Command<'a>(Vec<Word<'a>>);

impl<'a, W: Into<Word<'a>>> From<Vec<W>> for Command<'a> {
    fn from(value: Vec<W>) -> Self {
        Self(value.into())
    }
}