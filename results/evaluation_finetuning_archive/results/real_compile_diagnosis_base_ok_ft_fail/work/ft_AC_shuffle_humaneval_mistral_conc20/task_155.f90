program even_odd_count
    implicit none
    integer :: num
    integer :: even_count, odd_count
    character(len=10) :: num_str
    integer :: i

    ! Read input number
    read(*,*) num

    ! Convert number to string (handle negative sign)
    write(num_str, '(I0)') num

    ! Initialize counters
    even_count = 0
    odd_count = 0

    ! Count even and odd digits
    do i = 1, len(num_str)
        if (i == 1 .and. num_str(1:1) == '-') then
            ! Skip negative sign
            cycle
        end if
        if (mod(iachar(num_str(i:i)), 2) == 0) then
            even_count = even_count + 1
        else
            odd_count = odd_count + 1
        end if
    end do

    ! Output results
    print *, even_count, odd_count

end program even_odd_count