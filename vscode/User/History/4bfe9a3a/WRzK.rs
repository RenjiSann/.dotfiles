pub struct Word<'a>(pub &'a str);

impl<'a> From<&'a str> for Word<'a> {

}
