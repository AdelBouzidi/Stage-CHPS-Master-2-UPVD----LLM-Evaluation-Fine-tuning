program factorial_sum_demo
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input
  read(*,*) n

  ! Allocate result array
  allocate(result(n))

  ! Compute result
  do i = 1, n
    if (mod(i, 2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum(1:i)
    end if
  end do

  ! Output result
  write(*,*) result

contains

  integer function factorial(k)
    integer, intent(in) :: k
    integer :: i
    factorial = 1
    do i = 1, k
      factorial = factorial * i
    end do
  end function factorial

end program factorial_sum_demo