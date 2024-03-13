use std::ops::Range;
use tower_lsp::lsp_types::Position;

/// Return the new values of a position if we remove a range in the file.
pub(crate) fn update_position(
    removed: Range<Position>,

    pos: Position,
) -> Option<Position> {
    let s = removed.start;
    let e = removed.end;

    // pos is before the removed range
    if pos.line < s.line || (pos.line == s.line && pos.character <= s.character)
    {
        return Some(pos);
    }

    // pos is after the lines of the removed range
    if pos.line > e.line {
        return Some(Position {
            line: pos.line - (e.line - s.line),
            character: pos.character,
        });
    }

    // pos is after the removed range
    if pos.line == e.line && pos.character < e.character {
        let char_delta = s.character as i32 - e.character as i32;
        return Some(Position {
            line: pos.line - (e.line - s.line),
            character: (pos.character as i32 + char_delta) as u32,
        });
    }

    // pos is inside te removed range
    None
}

pub(crate) fn diagnostic_message(c1: char, c2: char) -> String {
    let mut b1 = [0 as u8; 4];
    let mut b2 = [0 as u8; 4];
    let _ = c1.clone().encode_utf8(&mut b1);
    let _ = c2.clone().encode_utf8(&mut b2);
    format!("Character `{}` (U+{:#x}{:#x}{:#x}{:#x}) could be confused with the ASCII character `{}` (U+{})",
            c1, b1[0], b1[1], b1[2], b1[3],
            c2, b2[0], b2[1], b2[2], b2[3])
}
