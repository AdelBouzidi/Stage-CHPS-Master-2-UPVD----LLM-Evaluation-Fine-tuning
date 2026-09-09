program digits
  implicit none
  integer :: n, result

  ! Read input
  read *, n

  ! Calculate result
  result = digits(n)

  ! Output result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i, digit, product, all_even

    res = 0
    product = 1
    all_even = .true.
    i = 0
    do while (n > 0)
      digit = mod(n, 10)
      if (mod(digit, 2) == 1) then
        product = product * digit
        all_even = .false.
      else
        all_even = .true.
      end if
      n = n / 10
      i = i + 1
    end do
    if (all_even) then
      res = 0
    else
      res = product
    end if
  end function digits

end program digits