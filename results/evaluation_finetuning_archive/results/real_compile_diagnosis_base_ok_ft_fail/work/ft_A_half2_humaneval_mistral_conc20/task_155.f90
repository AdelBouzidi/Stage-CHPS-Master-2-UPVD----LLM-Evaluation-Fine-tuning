program even_odd_count_demo
    implicit none
    integer :: num
    integer :: even_count, odd_count
    
    ! Read input
    read(*,*) num
    
    ! Call the function
    call even_odd_count(num, even_count, odd_count)
    
    ! Print output
    print *, even_count, odd_count
    
contains

    subroutine even_odd_count(num, even_count, odd_count)
        implicit none
        integer, intent(in) :: num
        integer, intent(out) :: even_count, odd_count
        integer :: digit
        integer :: abs_num
        
        abs_num = abs(num)
        even_count = 0
        odd_count = 0
        
        do while (abs_num > 0)
            digit = mod(abs_num, 10)
            if (mod(digit, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
            abs_num = abs_num / 10
        end do
    end subroutine even_odd_count

end program even_odd_count_demo