program factorial_sum_demo
  implicit none
  integer :: n, i
  integer, allocatable :: arr(:)

  ! Read input
  read(*,*) n

  ! Allocate array
  allocate(arr(n))

  ! Compute values
  do i = 1, n
    if (mod(i, 2) == 0) then
      ! Even: factorial
      arr(i) = factorial(i)
    else
      ! Odd: sum from 1 to i
      arr(i) = sum_to(i)
    end if
  end do

  ! Output result
  write(*,*) arr

contains

  integer function factorial(k)
    integer, intent(in) :: k
    integer :: i
    factorial = 1
    do i = 1, k
      factorial = factorial * i
    end do
  end function factorial

  integer function sum_to(k)
    integer, intent(in) :: k
    sum_to = k * (k + 1) / 2
  end function sum_to

end program factorial_sum_demo