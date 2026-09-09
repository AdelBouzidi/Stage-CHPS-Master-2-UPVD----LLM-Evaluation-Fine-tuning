program even_odd_count
    implicit none
    integer :: num
    integer :: even_count = 0
    integer :: odd_count = 0
    integer :: digit

    ! Read input
    read(*,*) num

    ! Handle negative numbers by taking absolute value
    if (num < 0) then
        num = -num
    end if

    ! Count even and odd digits
    do while (num > 0)
        digit = mod(num, 10)
        if (mod(digit, 2) == 0) then
            even_count = even_count + 1
        else
            odd_count = odd_count + 1
        end if
        num = num / 10
    end do

    ! Output results
    print *, even_count, odd_count

end program even_odd_count