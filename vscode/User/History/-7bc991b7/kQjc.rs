const MAX_SIZE: usize = 100;

pub struct Stack {
    vec: [i32; MAX_SIZE],
    index: usize
}

impl Stack {
    pub fn new() -> Self {
        Stack { vec: [0; MAX_SIZE], index: 0 }
    }

    pub fn pop(&mut self) -> Option<i32> {
        if self.index > 0 {
            self.index -= 1;
            Some(self.vec[self.index])
        } else {
            None
        }
    }

    pub fn peek(&self) -> Option<i32> {
        if self.index > 0 {
            Some(self.vec[self.index - 1])
        } else {
            None
        }
    }

    pub fn push(&mut self, i: i32) -> bool {
        if self.index <= MAX_SIZE {
            self.vec[self.index] = i;
            self.index += 1;
            true
        } else {
            false
        }
    }
}




#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let mut stack = Stack::new();
        assert_eq!(stack.push(1), Ok(()));
        assert_eq!(stack.push(2), Ok(()));
        assert_eq!(stack.push(3), Ok(()));
        assert_eq!(stack.pop(), Some(3));
        assert_eq!(stack.peek(), Some(2));
        assert_eq!(stack.pop(), Some(2));
        assert_eq!(stack.pop(), Some(1));
        assert_eq!(stack.pop(), None);
    }
}
