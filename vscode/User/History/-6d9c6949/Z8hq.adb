procedure Exo4 is
    subtype RomanNumber is Natural range 1 .. 3999;
    subtype Digit is Natural range 0 .. 9;
    -- (I V X)
    -- (X L C)
    -- (C D M)
    function DigitToString(digit: in Digit; c1: Character; c2: Character; c3: Character) return String is
        ret: String(1 .. 4);
        size: Integer := 0;
    begin
        case digit is
            when 0 => ret := "";
            when 1 => ret(0) := c1;
            when 2 => ret(0) := c1; ret(1) := c1;
            when 0 => ret := "";
            when others => ret := ".";
        end case;

    end DigitToChar;
begin
   null;
end Exo4;