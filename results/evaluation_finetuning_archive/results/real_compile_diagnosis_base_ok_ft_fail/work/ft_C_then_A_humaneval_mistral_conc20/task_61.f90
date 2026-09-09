program correct_bracketing
    implicit none
    character(len=100) :: brackets
    logical :: result

    ! Hardcoded input as per requirements
    brackets = "(("

    result = correct_bracketing(brackets)

    print *, result

contains

    logical function correct_bracketing(brackets)
        character(len=*), intent(in) :: brackets
        integer :: i, open_count, close_count
        character(len=1) :: char

        open_count = 0
        close_count = 0

        do i = 1, len(brackets)
            char = brackets(i:i)
            if (char == '(') then
                open_count = open_count + 1
            else if (char == ')') then
                close_count = close_count + 1
            end if
        end do

        correct_bracketing = (open_count == close_count)
    end function correct_bracketing

end program correct_bracketing