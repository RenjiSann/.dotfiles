use super::word::Word;

pub struct Command<'a>(Vec<Word<'a>>);

impl<'a, W: 'a + Into<Word<'a>>> From<Vec<W>> for Command<'a>
where Word<'a> : From<&'a W>
{
    fn from(value: Vec<W>) -> Self {
        Self(value.iter().map(|w| w.into()).collect())
    }
}