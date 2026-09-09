program f_demo
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input n
  read(*,*) n

  ! Allocate result array
  allocate(result(n))

  ! Compute result
  do i = 1, n
    if (mod(i, 2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum_to(i)
    end if
  end do

  ! Output result
  print *, result

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
    integer :: i
    sum_to = 0
    do i = 1, k
      sum_to = sum_to + i
    end do
  end function sum_to

end program f_demo