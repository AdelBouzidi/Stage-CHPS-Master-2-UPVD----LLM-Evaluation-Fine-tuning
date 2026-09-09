program digits
  implicit none
  integer :: n, result
  read(*,*) n
  result = digits(n)
  print *, result
contains
  function digits(n) result(res)
    integer, intent(in) :: n
    integer :: res
    integer :: i, digit
    res = 0
    do i = 1, n
      digit = mod(i, 10)
      if (mod(digit, 2) == 1) then
        res = res * digit
      end if
    end do
  end function digits
end program digits