use super::word::Word;

pub struct Command<'a>(Vec<Word<'a>>);

impl<'a, W: 'a + Into<Word<'a>>> From<Vec<W>> for Command<'a>
{
    fn from(value: Vec<W>) -> Self {
        Self(value.into_iter().map(|w| w.into()).collect())
    }
}