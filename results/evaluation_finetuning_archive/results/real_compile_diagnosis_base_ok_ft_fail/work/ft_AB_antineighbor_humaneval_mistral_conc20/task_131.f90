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
    integer :: i, digit, product, has_odd

    res = 0
    product = 1
    has_odd = 0
    i = 0
    do while (n > 0)
      digit = mod(n, 10)
      if (mod(digit, 2) == 1) then
        product = product * digit
        has_odd = 1
      end if
      n = n / 10
      i = i + 1
    end do
    if (has_odd == 1) then
      res = product
    else
      res = 0
    end if
  end function digits

end program digits