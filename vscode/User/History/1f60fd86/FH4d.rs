pub trait Stack {
    fn new() -> Self;
    fn pop(&mut self) -> Option<i32>;
    fn push(&mut self, value : i32) -> bool;
    fn peek(&self) -> Option<i32>;
}
struct StackImplem {
    vec: Vec<i32>
}

impl Stack for StackImplem {
    fn new() -> Self {
        StackImplem { vec: vec![] }
    }

    fn pop(&mut self) -> Option<i32> {
        self.vec.pop()
    }

    fn peek(&self) -> Option<i32> {
        self.vec.last().copied()
    }

    fn push(&mut self, i: i32) {
        self.vec.push(i)
    }
}

pub fn new_stack() -> impl Stack {
    return Stack::new()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}