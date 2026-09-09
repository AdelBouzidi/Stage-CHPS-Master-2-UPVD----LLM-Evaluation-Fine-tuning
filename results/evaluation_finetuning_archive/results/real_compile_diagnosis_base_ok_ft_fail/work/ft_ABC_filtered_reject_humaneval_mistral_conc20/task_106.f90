program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
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
  
  ! Print result
  do i = 1, n
    write(*,*) result(i)
  end do
  
contains

  recursive function factorial(i) result(fact)
    integer, intent(in) :: i
    integer :: fact
    if (i <= 1) then
      fact = 1
    else
      fact = i * factorial(i-1)
    end if
  end function factorial

  function sum_to(i) result(s)
    integer, intent(in) :: i
    integer :: s
    s = i * (i + 1) / 2
  end function sum_to

end program main