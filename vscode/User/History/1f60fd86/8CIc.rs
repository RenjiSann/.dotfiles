pub trait Stack {
    fn new() -> Self;
    fn pop(&mut self) -> Option<i32>;
    fn push(&mut self, value : i32) -> bool;
    fn peek(&mut self) -> Option<i32>;
}
struct StackImplem {
    vec: Vec<i32>;
}

impl Stack for StackImplem { }

pub fn new_stack() -> impl Stack { }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
