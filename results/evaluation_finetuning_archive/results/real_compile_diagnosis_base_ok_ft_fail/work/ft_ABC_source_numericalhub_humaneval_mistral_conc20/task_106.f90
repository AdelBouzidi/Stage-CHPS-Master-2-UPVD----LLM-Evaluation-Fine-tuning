program factorial_sum
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b) :: n
  integer(i4b), allocatable :: result(:)
  integer(i4b) :: i

  read(*,*) n
  allocate(result(n))
  do i = 1, n
    if (mod(i,2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum(1:i)
    end if
  end do
  print *, result
contains

  integer(i4b) function factorial(n)
    integer(i4b), intent(in) :: n
    integer(i4b) :: i
    factorial = 1
    do i = 2, n
      factorial = factorial * i
    end do
  end function factorial

end program factorial_sum