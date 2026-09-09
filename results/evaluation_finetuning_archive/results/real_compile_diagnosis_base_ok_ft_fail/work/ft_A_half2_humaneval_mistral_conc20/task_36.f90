program fizz_buzz
    implicit none
    integer :: n, result
    integer :: i, num, digit_count

    ! Read input n
    read(*,*) n

    result = 0
    do i = 1, n-1
        if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
            num = i
            digit_count = 0
            do while (num > 0)
                if (mod(num, 10) == 7) then
                    digit_count = digit_count + 1
                end if
                num = num / 10
            end do
            result = result + digit_count
        end if
    end do

    print *, result
end program fizz_buzz