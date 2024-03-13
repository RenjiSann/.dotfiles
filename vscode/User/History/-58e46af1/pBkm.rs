use super::word::Word;

pub struct Command<'a>(Vec<Word<'a>>);

impl<'a, W: Into<Word<'a>>> From<Vec<&'a W>> for Command<'a>
where Word<'a> : From<&'a W>
{
    fn from(value: Vec<&'a W>) -> Self {
        Self(value.iter().map(|&w| w.into()).collect())
    }
}