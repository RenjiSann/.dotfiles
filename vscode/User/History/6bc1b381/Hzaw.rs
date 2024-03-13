const MAX_SIZE: usize = 100;

pub struct Stack {
    vec: [i32; MAX_SIZE],
    index: usize
}

impl Stack {
    pub fn new() -> Self {
        Stack { vec: [0; MAX_SIZE], index: 0 }
    }
}




#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
    }
}
