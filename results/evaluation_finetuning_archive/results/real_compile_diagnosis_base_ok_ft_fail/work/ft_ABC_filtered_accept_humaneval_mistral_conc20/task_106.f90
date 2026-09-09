program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input
  read(*,*) n

  ! Allocate result array
  allocate(result(n))

  ! Calculate result
  do i = 1, n
    if (mod(i, 2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum_to(i)
    end if
  end do

  ! Output result
  write(*,*) result

contains

  recursive function factorial(k) result(res)
    integer, intent(in) :: k
    integer :: res
    if (k == 0 .or. k == 1) then
      res = 1
    else
      res = k * factorial(k-1)
    end if
  end function factorial

  function sum_to(k) result(res)
    integer, intent(in) :: k
    integer :: res
    res = 0
    do i = 1, k
      res = res + i
    end do
  end function sum_to

end program main