pub fn invert(s: &mut String){
    let r = s.chars();
    s = r.rev();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut s: String = "Test".to_string();
    }
}
