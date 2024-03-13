use std::collections::BinaryHeap;

struct SortedList<T>
where T: PartialOrd + Ord {
    vec: BinaryHeap<T>
}

impl<T> SortedList<T> {
    pub fn new() -> Self {
        SortedList { vec: vec![] }
    }


}