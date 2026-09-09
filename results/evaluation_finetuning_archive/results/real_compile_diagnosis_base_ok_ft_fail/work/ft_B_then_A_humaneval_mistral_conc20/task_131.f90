program digits
    implicit none
    integer function digits(n)
    integer, intent(in) :: n
    digits = 0
    if (n == 0) then
    digits = 0
    else
    digits = 1
    do while (n /= 0)
    digits = digits * mod(n, 10)
    n = n / 10
    end do
    end if
    end function digits
    program main
    integer :: n
    read *, n
    print *, digits(n)
    end program main