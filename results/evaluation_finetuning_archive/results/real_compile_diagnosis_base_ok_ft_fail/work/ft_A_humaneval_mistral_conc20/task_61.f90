program correct_bracketing
    implicit none
    character(len=100) :: brackets
    logical :: result
    read *, brackets
    result = correct_bracketing(brackets)
    print *, result
contains
    logical function correct_bracketing(brackets)
        character(len=*), intent(in) :: brackets
        integer :: i, count
        count = 0
        do i = 1, len(brackets)
            if (brackets(i:i) == '(') then
                count = count + 1
            else if (brackets(i:i) == ')') then
                count = count - 1
            end if
        end do
        correct_bracketing = (count == 0)
    end function correct_bracketing
end program correct_bracketing