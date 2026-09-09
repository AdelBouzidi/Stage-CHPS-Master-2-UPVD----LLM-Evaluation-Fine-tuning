program digits
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Calculate result
  result = digits(n)

  ! Output result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: temp, digit
    logical :: has_odd

    res = 1
    temp = n
    has_odd = .false.
    do while (temp > 0)
      digit = mod(temp, 10)
      if (mod(digit, 2) == 1) then
        res = res * digit
        has_odd = .true.
      end if
      temp = temp / 10
    end do

    if (.not. has_odd) then
      res = 0
    end if

  end function digits

end program digits